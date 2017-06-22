# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package consulta.views
#
# Vistas correspondientes a la aplicación consulta
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
import json
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, TemplateView, DeleteView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from base.functions import generar_token
from .models import Consulta, Pregunta, TipoPregunta, Opcion
from .forms import ConsultaForm, ConsultaPreguntaForm
 
class ConsultaIndex(LoginRequiredMixin, TemplateView):
    """!
    Clase que gestiona la vista principal de la consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-02-2017
    @version 1.0.0
    """
    template_name = "consulta.index.html"


class ConsultaCreate(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    """!
    Clase que gestiona la creación de consultas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-02-2017
    @version 1.0.0
    """
    model = Consulta
    form_class = ConsultaPreguntaForm
    template_name = "consulta.create.html"
    success_message = "Se creó la consulta con éxito"
    success_url = reverse_lazy('consulta_index')
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 16-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        if 'tipo_pregunta_modal' in self.request.POST and 'texto_pregunta_modal' in self.request.POST:
            post_data = dict(self.request.POST.lists())
            if ((len(post_data['tipo_pregunta_modal'])>0 and len(post_data['texto_pregunta_modal'])>0) and (len(post_data['texto_pregunta_modal']) == len(post_data['tipo_pregunta_modal']))):
                valores = {}
                for i in range(len(post_data['tipo_pregunta_modal'])):
                    valores[i] = {'texto_pregunta':post_data['texto_pregunta_modal'][i],'tipo_pregunta':post_data['tipo_pregunta_modal'][i]}
                kwargs['opciones'] = json.dumps(valores)
        return super(ConsultaCreate, self).get_context_data(**kwargs)
        
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 15-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        
        post_data = dict(self.request.POST.lists())
        user = User.objects.get(pk=self.request.user.id)
        
        ## Se crea el objeto de la consulta
        self.object = form.save(commit=False)
        self.object.nombre_consulta = form.cleaned_data['nombre_consulta']
        self.object.activa = form.cleaned_data['activa']
        self.object.token = generar_token(self.request.user.id)
        self.object.user = user
        self.object.save()
        
        ## Se crea la pregunta que se pide por defecto
        tipo = TipoPregunta.objects.get(pk=form.cleaned_data['tipo_pregunta'])
        pregunta = Pregunta()
        pregunta.texto_pregunta = form.cleaned_data['texto_pregunta']
        pregunta.tipo_pregunta = tipo
        pregunta.consulta = self.object
        pregunta.save()
         
        ## Si se agregaron más preguntas se crean
        if 'tipo_pregunta_modal' in self.request.POST and 'texto_pregunta_modal' in self.request.POST:
            self.create_questions(self.object,post_data)
        
        return super(ConsultaCreate, self).form_valid(form)
    
    
    def create_questions(self,objeto,data):
        """!
        Metodo para crear preguntas adicionales
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 16-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param objeto <b>{object}</b> Objeto de la consulta
        @param data <b>{dict}</b> Diccionario con los valores a guardar
        """
        if len(data['texto_pregunta_modal']) == len(data['tipo_pregunta_modal']):
            for i in range(len(data['texto_pregunta_modal'])):
                tipo = TipoPregunta.objects.get(pk=data['tipo_pregunta_modal'][i])
                pregunta = Pregunta()
                pregunta.texto_pregunta = data['texto_pregunta_modal'][i]
                pregunta.tipo_pregunta = tipo
                pregunta.consulta = objeto
                pregunta.save()
    
class ConsultaList(LoginRequiredMixin,ListView):
    """!
    Clase que gestiona la lista de consultas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-02-2017
    @version 1.0.0
    """
    model = Consulta
    template_name = "consulta.list.html"
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-06-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        kwargs['object_list'] = Consulta.objects.filter(user_id=self.request.user.id).order_by('nombre_consulta').all()
        ## Implementación del paginador
        paginator = Paginator(kwargs['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            kwargs['page_obj'] = paginator.page(page)
        except PageNotAnInteger:
            kwargs['page_obj'] = paginator.page(1)
        except EmptyPage:
            kwargs['page_obj'] = paginator.page(paginator.num_pages)
        return super(ConsultaList, self).get_context_data(**kwargs)
    
    
class ConsultaDetail(LoginRequiredMixin,DetailView):
    """!
    Clase que gestiona el detalle de una consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 17-02-2017
    @version 1.0.0
    """
    model = Consulta
    template_name = "consulta.detail.html"
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 17-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        kwargs['preguntas'] = Pregunta.objects.filter(consulta_id=kwargs['object'].id).all()
        return super(ConsultaDetail, self).get_context_data(**kwargs)
    
class ConsultaDelete(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    """!
    Clase que gestiona el borrado de consultas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-02-2017
    @version 1.0.0
    """
    model = Consulta
    template_name = "consulta.delete.html"
    success_message = "Se eliminó la consulta con éxito"
    success_url = reverse_lazy('consulta_index')
    
    
class ConsultaUpdate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    """!
    Clase que gestiona la actualización de consultas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 17-02-2017
    @version 1.0.0
    """
    model = Consulta
    form_class = ConsultaForm
    template_name = "consulta.update.html"
    success_message = "Se actualizó la consulta con éxito"
    success_url = reverse_lazy('consulta_list')
    
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 17-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        preguntas = Pregunta.objects.filter(consulta_id=self.object.id).all()
        kwargs['preguntas'] = preguntas
        return super(ConsultaUpdate, self).get_context_data(**kwargs)
    
class ConsultaGenerateToken(LoginRequiredMixin,UpdateView):
    """!
    Clase que gestiona la actualización de consultas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-06-2017
    @version 1.0.0
    """
    template_name = "consulta.update.html"
    success_url = reverse_lazy('consulta_list')
    
    def post(self, request, pk):
        """!
        Metodo que sobreescribe la acción por POST
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 22-06-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param pk <b>{int}</b> Id de la consulta
        @return Retorna los datos de la petición post
        """
        if self.request.is_ajax():
            model = Consulta.objects.filter(pk=pk)
            if(model):
                model = model.get()
                model.token = generar_token(self.request.user.id)
                model.save()
                return JsonResponse({"code":True})
            return JsonResponse({"code":False,"errors":"La Consulta solicitada no existe"})
        
           
class OpcionesCreate(LoginRequiredMixin,CreateView):
    """!
    Clase que gestiona la creación de opciones

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-02-2017
    @version 1.0.0
    """
    model = Opcion
    fields = ['texto_opcion']
    template_name = "consulta.create.html"
    success_url = reverse_lazy('consulta_index')
            
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        post_data = dict(self.request.POST.lists())
        pregunta = Pregunta.objects.get(id=int(self.kwargs['pk']))
        
        ## Se guarda la primera opcion
        self.object = form.save(commit=False)
        self.object.texto_opcion = post_data['texto_opcion'][0]
        self.object.pregunta = pregunta
        self.object.save()
        
        ## Se guardan las demás opciones si existen
        for i in range(1,len(post_data['texto_opcion'])):
            opcion = Opcion()
            opcion.texto_opcion = post_data['texto_opcion'][i]
            opcion.pregunta = pregunta
            opcion.save()
            
        if self.request.is_ajax():
            return JsonResponse({"code":True})
            
        return super(OpcionesCreate, self).form_valid(form)
    
    def form_invalid(self,form):
        """!
        Metodo que valida si el formulario es invalido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario inválido
        """
        if self.request.is_ajax():
            return JsonResponse({"code":False,'errors':form.errors})
        return super(OpcionesCreate, self).form_invalid(form)
    
    
class OpcionesUpdate(LoginRequiredMixin,UpdateView):
    """!
    Clase que gestiona la actualización de las opciones

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-02-2017
    @version 1.0.0
    """
    model = Opcion
    fields = ['texto_opcion']
    template_name = "consulta.update.html"
    success_url = reverse_lazy('consulta_list')
    
    
    def post(self, request):
        """!
        Metodo que sobreescribe la acción por POST
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna los datos de contexto
        """
        post_data = dict(self.request.POST.lists())
        for i in range(len(post_data['texto_opcion'])):
            opcion = Opcion.objects.filter(id=int(post_data['texto_opcion_id'][i]))
            if(opcion):
                opcion = opcion.get()
                opcion.texto_opcion = post_data['texto_opcion'][i]
                opcion.save()

        if self.request.is_ajax():
            return JsonResponse({"code":True})
        
class OpcionesDelete(LoginRequiredMixin,DeleteView):
    """!
    Clase que gestiona el borrado de una opción

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-02-2017
    @version 1.0.0
    """
    model = Opcion
    template_name = "consulta.update.html"
    success_url = reverse_lazy('consulta_list')
    
    def post(self, request, pk):
        """!
        Metodo que sobreescribe la acción por POST
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param pk <b>{int}</b> Recibe el id para filtrar
        @return Retorna los datos de contexto
        """
        opcion = Opcion.objects.filter(id=int(pk))
        if(opcion):
            opcion = opcion.get()
            opcion.delete()
            return JsonResponse({'success':True})
        return JsonResponse({'success':False,'mensaje':'Opción inválida'})
            
            
class PreguntaDelete(LoginRequiredMixin,DeleteView):
    """!
    Clase que gestiona el borrado de una pregunta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-02-2017
    @version 1.0.0
    """
    model = Pregunta
    template_name = "consulta.update.html"
    success_url = reverse_lazy('consulta_list')
    
    def post(self, request, pk):
        """!
        Metodo que sobreescribe la acción por POST
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param pk <b>{int}</b> Recibe el id para filtrar
        @return Retorna los datos de contexto
        """
        pregunta = Pregunta.objects.filter(id=int(pk))
        if(pregunta):
            pregunta = pregunta.get()
            ## Si tiene opciones, se buscan y se borran
            if(pregunta.tipo_pregunta_id==1):
                opciones = Opcion.objects.filter(pregunta_id=pregunta.id)
                if (opciones):
                    for item in opciones.all():
                        item.delete()                
            pregunta.delete()
            return JsonResponse({'success':True})
        return JsonResponse({'success':False,'mensaje':'Pregunta inválida'})
    
    
class PreguntaCreate(LoginRequiredMixin,CreateView):
    """!
    Clase que gestiona la creación de preguntas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-02-2017
    @version 1.0.0
    """
    model = Pregunta
    fields = ['texto_pregunta','tipo_pregunta']
    template_name = "consulta.create.html"
    success_url = reverse_lazy('consulta_index')
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 21-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        post_data = dict(self.request.POST.lists())
        consulta = Consulta.objects.get(id=int(self.kwargs['pk']))
        
        ## Se guarda la primera opcion
        self.object = form.save(commit=False)
        self.object.texto_opcion = form.cleaned_data['texto_pregunta']
        self.object.tipo_pregunta = form.cleaned_data['tipo_pregunta']
        self.object.consulta = consulta
        self.object.save()
        
        ## Se guardan las demás opciones si existen
        for i in range(len(post_data['texto_pregunta'])-1):
            tipo_pregunta = TipoPregunta.objects.get(id=int(post_data['tipo_pregunta'][i]))
            pregunta = Pregunta()
            pregunta.texto_opcion = post_data['texto_pregunta'][i]
            pregunta.tipo_pregunta = post_data['tipo_pregunta'][i]
            pregunta.consulta = consulta
            pregunta.save()
            
        if self.request.is_ajax():
            return JsonResponse({"code":True})
            
        return super(OpcionesCreate, self).form_valid(form)
    
    def form_invalid(self,form):
        """!
        Metodo que valida si el formulario es invalido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 21-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario inválido
        """
        if self.request.is_ajax():
            return JsonResponse({"code":False,'errors':form.errors})
        return super(OpcionesCreate, self).form_invalid(form)
    
class PreguntaUpdate(LoginRequiredMixin, UpdateView):
    """!
    Clase que gestiona la actualización de las preguntas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 23-02-2017
    @version 1.0.0
    """
    model = Pregunta
    fields = ['texto_pregunta','tipo_pregunta']
    template_name = "consulta.update.html"
    success_url = reverse_lazy('consulta_list')
    
    def post(self, request):
        """!
        Metodo que sobreescribe la acción por POST
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 23-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna los datos de contexto
        """
        post_data = dict(self.request.POST.lists())
        for i in range(len(post_data['texto_pregunta_modal'])):
            pregunta = Pregunta.objects.filter(id=int(post_data['texto_pregunta_id'][i]))
            if(pregunta):
                pregunta = pregunta.get()
                salvar = False
                if(pregunta.texto_pregunta != post_data['texto_pregunta_modal'][i]):
                    pregunta.texto_pregunta = post_data['texto_pregunta_modal'][i]
                    salvar = True
                if(pregunta.tipo_pregunta != post_data['tipo_pregunta_modal'][i]):
                    tipo_pregunta = TipoPregunta.objects.filter(id=int(post_data['tipo_pregunta_modal'][i])).get()
                    pregunta.tipo_pregunta = tipo_pregunta
                    salvar = True
                if(salvar):    
                    pregunta.save()

        if self.request.is_ajax():
            return JsonResponse({"code":True})
    