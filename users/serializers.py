# -*- coding: utf-8 -*-
from django import forms
from rest_framework import serializers
from django.contrib.auth.models import User
from drf_braces.serializers.form_serializer import FormSerializer
from base.fields import CedulaField
from base.functions import (
    cargar_entidad, cargar_municipios, cargar_parroquias,
    validate_cedula, validate_email
    )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo User

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 17-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class UserForm(forms.Form):
    ## Nombre de usuario
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(),
        label="Nombre de Usuario"
        )
    
    ## Contraseña
    password = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Constraseña"
        )
    
    ## Repita la Contraseña
    password_repeat = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Repita su constraseña"
        )
    
    ## nombre
    nombre = forms.CharField(max_length=100,
        widget=forms.TextInput(),
        label="Nombre"
        )
    
    ## apellido
    apellido = forms.CharField(max_length=100,
        widget=forms.TextInput(),
        label="Apellido"
        )
    
    ## correo
    email = forms.EmailField(
        widget=forms.TextInput(),
        label="Correo"
        )
    
    ## cedula
    
    def clean_password_repeat(self):
        """!
        Método que valida si las contraseñas coinciden
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if(password_repeat!=password):
            raise forms.ValidationError("La contraseña no coincide")
        return password_repeat
    
    def clean_cedula(self):
        """!
        Método que valida si la cedula es única
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        cedula = self.cleaned_data['cedula']
        if(validate_cedula(cedula)):
            raise forms.ValidationError("La cédula ingresada ya existe")
        return cedula
    
    def clean_email(self):
        """!
        Método que valida si el correo es única
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        email = self.cleaned_data['email']
        if(validate_email(email)):
            raise forms.ValidationError("El correo ingresado ya existe")
        return email
    

class MySerializer(FormSerializer):
    class Meta(object):
        form = UserForm