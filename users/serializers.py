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
from drf_braces.serializers.form_serializer import FormSerializer


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
    user = UserSerializer(read_only=True)

    class Meta:
        model = Perfil
        fields = ('cedula', 'parroquia', 'user')

class RegistroSerializer(FormSerializer):
    """!
    Clase serializador de registro de usuario

    @author Antonio Araujo (aaraujo at cenditel.gob.ve)
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 19-09-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    def save(self):
        """!
        Metodo que guarda lols registros del formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 20-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna verdadero si se guarda
        """
        user = User()
        user.username = self.validated_data['username']
        user.first_name = self.validated_data['nombre']
        user.last_name = self.validated_data['apellido']
        user.set_password(self.validated_data['password'])
        user.email = self.validated_data['email']
        user.save()
               
        parroquia = Parroquia.objects.get(id=self.validated_data['parroquia'])
        
        perfil = Perfil()
        perfil.cedula = self.validated_data['cedula']
        perfil.parroquia = parroquia
        perfil.user = user
        perfil.save()
        return True
    
    class Meta(object):
        form = UserForm
