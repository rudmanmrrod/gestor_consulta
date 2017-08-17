# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User


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
