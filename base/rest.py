# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.rest
#
# ViewSet (vistas de los rest) para el rest framework
# @author Argenis Osorio (aosorio at cenditel.gob.ve)
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
    filter_fields = ('id', 'codigo', 'nombre',)
    http_method_names = ['get','head']


class MunicipioViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos rest de los Municipios

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @param estado Puede recibir el id del estado por GET
    @date 16-08-2017
    @version 1.0.0
    """
    serializer_class = MunicipioSerializer
    filter_fields = ('id', 'codigo', 'nombre',)
    http_method_names = ['get','head']
    
    def get_queryset(self):
        """!
        Función organizar la consulta
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-09-17
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un la consulta
        """
        queryset = Municipio.objects.all()
        estado = self.request.query_params.get('estado', None)
        if estado is not None:
            queryset = queryset.filter(entidad_id=estado)
        return queryset
    
    
class ParroquiaViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos rest de las Parroquias

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @param municipio Puede recibir el id del municipio por GET
    @date 17-08-2017
    @version 1.0.0
    """
    serializer_class = ParroquiaSerializer
    filter_fields = ('id', 'codigo', 'nombre',)
    http_method_names = ['get','head']
    
    def get_queryset(self):
        """!
        Función organizar la consulta
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-09-17
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un la consulta
        """
        queryset = Parroquia.objects.all()
        municipio = self.request.query_params.get('municipio', None)
        if municipio is not None:
            queryset = queryset.filter(municipio_id=municipio)
        return queryset