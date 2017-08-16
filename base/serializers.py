# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Entidad


class EntidadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Entidad
        fields = ('id', 'codigo', 'nombre')
