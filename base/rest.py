# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.rest
#
# ViewSet (vistas de los rest) para el rest framework
# @author Argenis Osorio (aosorio at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from base.models import Entidad, Municipio, Parroquia
from .serializers import EntidadSerializer, MunicipioSerializer, ParroquiaSerializer
from rest_framework import viewsets


class EntidadViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos rest de las Entidades

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-08-2017
    @version 1.0.0
    """
    queryset = Entidad.objects.all()
    serializer_class = EntidadSerializer
    http_method_names = ['get','head']


class MunicipioViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos rest de los Municipios

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-08-2017
    @version 1.0.0
    """
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    http_method_names = ['get','head']


class ParroquiaViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos rest de las Parroquias

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 17-08-2017
    @version 1.0.0
    """
    queryset = Parroquia.objects.all()
    serializer_class = ParroquiaSerializer
    http_method_names = ['get','head']
