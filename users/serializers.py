# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package user.serializers
#
# Serializadores de los modelos de usuario para el rest framework
# @author Antonio Araujo (aaraujo at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from django import forms
from rest_framework import serializers
from django.contrib.auth.models import User
from drf_braces.serializers.form_serializer import FormSerializer
from base.fields import CedulaField
from base.functions import (
    cargar_entidad, cargar_municipios, cargar_parroquias,
    validate_cedula, validate_email
    )
from .forms import UserForm
from .models import Perfil
from drf_braces.serializers.form_serializer import FormSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo User

    @author Antonio Araujo (aaraujo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 31-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class PerfilSerializer(serializers.ModelSerializer):
    """!
    Metodo que permite serializar el modelo Perfil

    @author Antonio Araujo (aaraujo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 31-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Perfil
        fields = ('cedula', 'parroquia', 'user')

class RegistroSerializer(FormSerializer):
    """!
    Clase serializador de registro de usuario

    @author Antonio Araujo (aaraujo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 19-09-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    class Meta(object):
            form = UserForm
