# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package consulta.paths
#
# paths de la aplicación consulta
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from django.urls import path
from django.contrib import admin
from .views import *
from .ajax import *

pathpatterns = [
    ## paths de la consulta
    path('', ConsultaIndex.as_view(), name = "consulta_index"),
    path('create', ConsultaCreate.as_view(), name = "consulta_create"),
    path('list', ConsultaList.as_view(), name = "consulta_list"),
    path('delete/<int:pk>', ConsultaDelete.as_view(), name = "consulta_delete"),
    path('detail/<int:pk>', ConsultaDetail.as_view(), name = "consulta_detail"),
    path('update/<int:pk>', ConsultaUpdate.as_view(), name = "consulta_update"),
    path('generate-token/<int:pk>', ConsultaGenerateToken.as_view(), name = "consulta_token"),
    ## paths de las preguntas
    path('create-question/<int:pk>', PreguntaCreate.as_view(), name = "question_create"),
    path('delete-question/<int:pk>', PreguntaDelete.as_view(), name = "question_delete"),
    path('update-question', PreguntaUpdate.as_view(), name = "question_update"),
    ## paths de las opciones
    path('create-option/<int:pk>', OpcionesCreate.as_view(), name = "option_create"),
    path('update-option', OpcionesUpdate.as_view(), name = "option_update"),
    path('delete-option/<int:pk>', OpcionesDelete.as_view(), name = "opciones_delete"),
    ## paths especiales sin argumentos
    path('create-question/', PreguntaCreate.as_view(), name = "question_create_nk"),
    path('delete-question/', PreguntaDelete.as_view(), name = "question_delete_nk"),
    path('create-option/', OpcionesCreate.as_view(), name = "option_create_nk"),
    path('delete-option/', OpcionesDelete.as_view(), name = "opciones_delete_nk"),
]

## paths por ajax
pathpatterns += [
    path('ajax/pregunta-list/<int:pk>', pregunta_list, name = "ajax_pregunta_list"),
    path('ajax/opciones-list/<int:pk>', opciones_list, name = "ajax_opciones_list"),
    ## paths especiales sin argumentos
    path('ajax/pregunta-list/', pregunta_list, name = "ajax_pregunta_list_nk"),
    path('ajax/opciones-list/', opciones_list, name = "ajax_opciones_list_nk"),
    path('generate-token/', ConsultaGenerateToken.as_view(), name = "consulta_token_nk"),
]
