# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""

## @package user.rest
#
# ViewSet (vistas de los rest) para el rest framework
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author Antonio Araujo (aaraujo at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from users.models import Perfil
from .serializers import PerfilSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class UserDataViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos del usuario autenticado

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 28-09-2017
    @version 1.0.0
    """
    serializer_class = PerfilSerializer
    http_method_names = ['get','head']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """!
        Metodo que permite tomar los datos de la consulta
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los datos de contexto
        """
        return Perfil.objects.filter(user_id=self.request.user.id).all()
    
class PerfilViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos del perfil de los usuarios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 28-09-2017
    @version 1.0.0
    """
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    filter_fields = ('cedula','user__username','user__email')
    http_method_names = ['get','head']
