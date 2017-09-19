# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
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
    @date 31-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    class Meta(object):
            form = UserForm
