# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.serializers
#
# Serializadores de los modelos de las Entidades para el rest framework
# @author Argenis Osorio (aosorio at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from rest_framework import serializers
from .models import Entidad, Municipio, Parroquia


class EntidadSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo Entidad

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 16-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    class Meta:
        model = Entidad
        fields = ('url', 'id', 'codigo', 'nombre')


class MunicipioSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo Municipio

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 16-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    class Meta:
        model = Municipio
        fields = ('url', 'codigo', 'nombre', 'entidad')


class ParroquiaSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo Parroquia

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 17-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    class Meta:
        model = Parroquia
        fields = ('url', 'codigo', 'nombre', 'municipio')
