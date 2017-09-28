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
from .serializers import PerfilSerializer, RegistroSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_braces.mixins import MultipleSerializersViewMixin


class FormViewSet(MultipleSerializersViewMixin, viewsets.GenericViewSet):
    """!
    Clase que gestiona los datos rest de la consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @author Antonio Araujo (aaraujo at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU
    Public License versión 2 (GPLv2)</a>
    @date 20-06-2017
    @version 1.0.0
    """
    serializer_class = RegistroSerializer
    queryset = Perfil.objects.all()

    def create(self, request):
        """!
        Método que registra los datos del formulario

        @author Antonio Araujo (aaraujo at cenditel.gob.ve)
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 19-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna la respuesta con los datos
        """
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """!
        Método que retorna la lista de los perfiles

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 19-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los datos de los perfiles
        """
        serializer = PerfilSerializer(self.queryset, many=True)
        return Response(serializer.data)

class UserDataViewSet(viewsets.ModelViewSet):
    """!
    Clase que gestiona los datos del usuario autenticado

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU
    Public License versión 2 (GPLv2)</a>
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