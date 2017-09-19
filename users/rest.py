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
from users.models import Perfil
from base.serializers import EntidadSerializer, MunicipioSerializer, ParroquiaSerializer
from .serializers import UserSerializer, PerfilSerializer, RegistroSerializer
from rest_framework import viewsets
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_braces.mixins import MultipleSerializersViewMixin




class FormViewSet(MultipleSerializersViewMixin, viewsets.GenericViewSet):
    """!
    Clase que gestiona los datos rest de la consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU
    Public License versión 2 (GPLv2)</a>
    @date 20-06-2017
    @version 1.0.0
    """
    serializer_class = RegistroSerializer

    def create(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
