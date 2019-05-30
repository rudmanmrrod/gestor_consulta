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
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from django import forms
from rest_framework import serializers
from django.contrib.auth.models import User
from base.fields import CedulaField
from base.functions import (
    cargar_entidad, cargar_municipios, cargar_parroquias,
    validate_cedula, validate_email
    )
from base.models import Parroquia
from .forms import UserForm
from .models import Perfil


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo User

    @author Antonio Araujo (aaraujo at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 31-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    user = UserSerializer()

    class Meta:
        model = Perfil
        fields = ('cedula', 'parroquia', 'user')

    def create(self, validated_data):
        """!
        Metodo que guarda el serializer
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 30-05-2019
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna verdadero si se guarda
        """
        user = validated_data.pop("user")
        with transaction.atomic():
            user_created = User()
            user_created.username = user['username']
            user_created.first_name = user['nombre']
            user_created.last_name = user['apellido']
            user_created.email = user['email']
            user_created.set_password(user['password'])
            user_created.save()
            profile = Perfil.objects.create(**validated_data,user=user_created)
        return profile