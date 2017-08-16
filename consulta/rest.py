# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package consulta.rest
#
# ViewSet (vistas de los rest) para el rest framework
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from .serializers import ConsultaSerializer, PreguntaSerializer
from .models import Consulta, Pregunta
from rest_framework import viewsets


class ConsultaViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos rest de la consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-06-2017
    @version 1.0.0
    """
    serializer_class = ConsultaSerializer
    http_method_names = ['get','head']

    def get_queryset(self):
        """!
        Metodo que permite generar la consulta al modelo
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 22-06-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los datos de contexto
        """
        return Consulta.objects.filter(token=self.kwargs['token']).all()