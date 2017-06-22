# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package consulta.urls
#
# Urls de la aplicación consulta
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from django.conf.urls import url
from django.contrib import admin
from .views import *
from .ajax import *

urlpatterns = [
    ## Urls de la consulta
    url(r'^$', ConsultaIndex.as_view(), name = "consulta_index"),
    url(r'^create$', ConsultaCreate.as_view(), name = "consulta_create"),
    url(r'^list$', ConsultaList.as_view(), name = "consulta_list"),
    url(r'^delete/(?P<pk>\d+)$', ConsultaDelete.as_view(), name = "consulta_delete"),
    url(r'^detail/(?P<pk>\d+)$', ConsultaDetail.as_view(), name = "consulta_detail"),
    url(r'^update/(?P<pk>\d+)$', ConsultaUpdate.as_view(), name = "consulta_update"),
    url(r'^generate-token/(?P<pk>\d+)$', ConsultaGenerateToken.as_view(), name = "consulta_token"),
    ## Urls de las preguntas
    url(r'^create-question/(?P<pk>\d+)$', PreguntaCreate.as_view(), name = "question_create"),
    url(r'^delete-question/(?P<pk>\d+)$', PreguntaDelete.as_view(), name = "question_delete"),
    url(r'^update-question$', PreguntaUpdate.as_view(), name = "question_update"),
    ## Urls de las opciones
    url(r'^create-option/(?P<pk>\d+)$', OpcionesCreate.as_view(), name = "option_create"),
    url(r'^update-option$', OpcionesUpdate.as_view(), name = "option_update"),
    url(r'^delete-option/(?P<pk>\d+)$', OpcionesDelete.as_view(), name = "opciones_delete"),
    ## Urls especiales sin argumentos
    url(r'^create-question/$', PreguntaCreate.as_view(), name = "question_create_nk"),
    url(r'^delete-question/$', PreguntaDelete.as_view(), name = "question_delete_nk"),
    url(r'^create-option/$', OpcionesCreate.as_view(), name = "option_create_nk"),
    url(r'^delete-option/$', OpcionesDelete.as_view(), name = "opciones_delete_nk"),
]

## Urls por ajax
urlpatterns += [
    url(r'^ajax/pregunta-list/(?P<pk>\d+)$', pregunta_list, name = "ajax_pregunta_list"),
    url(r'^ajax/opciones-list/(?P<pk>\d+)$', opciones_list, name = "ajax_opciones_list"),
    ## Urls especiales sin argumentos
    url(r'^ajax/pregunta-list/$', pregunta_list, name = "ajax_pregunta_list_nk"),
    url(r'^ajax/opciones-list/$', opciones_list, name = "ajax_opciones_list_nk"),
    url(r'^generate-token/$', ConsultaGenerateToken.as_view(), name = "consulta_token_nk"),
]
