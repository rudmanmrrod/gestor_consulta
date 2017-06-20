# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package consulta.forms
#
# Formulario correspondiente a la aplicación consulta
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from django import forms
from base.functions import cargar_tipo_pregunta
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    """!
    Clase del formulario que registra la consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-02-2017
    @version 1.0.0
    """
    
    ##  Nombre de la consulta
    nombre_consulta = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-md',}))
    
    ## La consulta esta activa o no
    activa = forms.BooleanField(required=False,initial=True)
      
    
    class Meta:
        model = Consulta
        exclude = ['user']

class ConsultaPreguntaForm(forms.ModelForm):
    """!
    Clase del formulario que registra la consulta y la pregunta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-02-2017
    @version 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 15-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        super(ConsultaPreguntaForm, self).__init__(*args, **kwargs)

        self.fields['tipo_pregunta'].choices = cargar_tipo_pregunta()
    
    ##  Nombre de la consulta
    nombre_consulta = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-md',}))
    
    ## La consulta esta activa o no
    activa = forms.BooleanField(required=False,initial=True)
    
    ## El texto de la pregunta
    texto_pregunta = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-md',}),
        label="Texto de la Pregunta")
    
    ## Tipo de pregunta
    tipo_pregunta = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),
        label="Tipo de Pregunta")
    
    
    class Meta:
        model = Consulta
        exclude = ['user','token']