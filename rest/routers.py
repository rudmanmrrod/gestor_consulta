# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package rest.routers
#
# Routers de los viewset de la aplicaciones rest
# @author Antonio Araujo (aaraujo at cenditel.gob.ve)
# @author Argenis Osorio (aosorio at cenditel.gob.ve)
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from rest_framework.routers import DefaultRouter
from consulta.rest import ConsultaViewSet
from base.rest import (
    EntidadViewSet, MunicipioViewSet, ParroquiaViewSet,
    )
from users.rest import FormViewSet

router = DefaultRouter()
# ------------------------------------------
router.register(r'consulta/(?P<token>.+)', ConsultaViewSet, 'consulta')
router.register(r'entidad', EntidadViewSet, 'entidad')
router.register(r'municipio', MunicipioViewSet, 'municipio')
router.register(r'parroquia', ParroquiaViewSet, 'parroquia')
router.register(r'registro', FormViewSet, 'registro')
