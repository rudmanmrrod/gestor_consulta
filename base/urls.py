# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package participacion.urls
#
# Urls de la aplicación participacion
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from django.conf.urls import url
from .views import *
from base import views

urlpatterns = [
    url(r'^$', Inicio.as_view(), name = "inicio"),
    url(r'^403$', Error403.as_view(), name = "base_403"),
]

## Ajax
urlpatterns +=[
    url(r'^ajax/actualizar-combo/?$', actualizar_combo, name='actualizar_combo'),
]
