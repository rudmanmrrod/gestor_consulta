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
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from .serializers import ConsultaSerializer, PreguntaSerializer
from .models import Consulta, Pregunta
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class ConsultaViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos rest de la consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-06-2017
    @version 1.0.0
    """
    serializer_class = ConsultaSerializer
    http_method_names = ['get','head']
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """!
        Metodo que permite generar la consulta al modelo
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 22-06-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los datos de contexto
        """
        return Consulta.objects.filter(token=self.kwargs['token'],activa=True).all()