# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package participacion.views
#
# Vistas correspondientes a la aplicación participacion
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, CreateView, UpdateView
from .forms import LoginForm, UserRegisterForm, PerfilForm
from .models import Perfil
from base.models import Parroquia
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics


class LoginView(FormView):
    """!
    Clase que gestiona la vista principal del logeo de usuario

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 01-03-2017
    @version 1.0.0
    """
    form_class = LoginForm
    template_name = 'user.login.html'
    success_url = reverse_lazy('consulta_index')

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es valido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        usuario = form.cleaned_data['usuario']
        contrasena = form.cleaned_data['contrasena']
        usuario = authenticate(username=usuario, password=contrasena)
        login(self.request, usuario)
        if self.request.POST.get('remember_me') is not None:
            # Session expira a los dos meses si no se deslogea
            self.request.session.set_expiry(1209600)
        return super(LoginView, self).form_valid(form)
    
    
class LogoutView(RedirectView):
    """!
    Clase que gestiona la vista principal del deslogeo de usuario

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 01-03-2017
    @version 1.0.0
    """
    permanent = False
    query_string = True

    def get_redirect_url(self):
        """!
        Metodo que permite definir la url de dirección al ser válido el formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna la url
        """
        logout(self.request)
        return reverse_lazy('login')


class RegisterView(SuccessMessageMixin,FormView):
    """!
    Muestra el formulario de registro de usuarios

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 09-01-2017
    @version 1.0.0
    """
    template_name = "user.register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    success_message = "Se registró con éxito"
    model = User

    def form_valid(self, form, **kwargs):
        """!
        Metodo que valida si el formulario es valido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        self.object = form.save()
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['nombre']
        self.object.last_name = form.cleaned_data['apellido']
        self.object.set_password(form.cleaned_data['password'])
        self.object.email = form.cleaned_data['email']
        self.object.save()
              
        parroquia = Parroquia.objects.get(id=form.cleaned_data['parroquia'])
        
        perfil = Perfil()
        perfil.cedula = form.cleaned_data['cedula']
        perfil.parroquia = parroquia
        perfil.user = self.object
        perfil.save() 
        
        return super(RegisterView, self).form_valid(form)
    
class PerfilUpdate(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    """!
    Clase que gestiona la actualización del perfil

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 24-04-2017
    @version 1.0.0
    """
    model = Perfil
    template_name = "perfil.update.html"
    form_class = PerfilForm
    success_message = "Se actualizó el perfil con éxito"
    
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo que redirecciona al usuario si no cuenta con los permisos
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param args <b>{object}</b> Objeto que contiene los argumentos
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return: Direcciona al 403 si no es su perfil
        """
        if int(self.request.user.id) != int(self.kwargs['pk']):
            return redirect('base_403')
        return super(PerfilUpdate, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        """
        Metodo para obtener el objeto del perfil
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-05-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param queryset <b>{object}</b> Objeto que contiene una consulta
        @return El objeto del perfil
        """
        try:
            obj = Perfil.objects.get(user_id=self.kwargs['pk'])
        except Exception as e:
            obj = None
        return obj
    
    def get_success_url(self):
        """!
        Metodo que permite definir la url de dirección al ser válido el formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna la url
        """
        return reverse_lazy('update',
                            kwargs={'pk': self.kwargs['pk']})
    
    def get_initial(self):
        """!
        Metodo para agregar valores de inicio al formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los valores iniciales
        """
        initial = super(PerfilUpdate, self).get_initial()
        try:
            perfil = Perfil.objects.get(user_id=self.kwargs['pk'])
            initial['parroquia'] = perfil.parroquia_id
            initial['municipio'] = perfil.parroquia.municipio_id
            initial['estado'] = perfil.parroquia.municipio.entidad_id
        except Exception as e:
            pass 
    
        return initial
    
    def form_valid(self,form):
        """!
        Metodo que valida si el formulario es valido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        parroquia = Parroquia.objects.get(id=form.cleaned_data['parroquia'])
        
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.cedula = form.cleaned_data['cedula']
        self.object.parroquia = parroquia
        self.object.save()
        
        return super(PerfilUpdate, self).form_valid(form)

