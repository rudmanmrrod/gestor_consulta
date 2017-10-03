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
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from rest_framework import serializers
from .models import Entidad, Municipio, Parroquia


class EntidadSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo Entidad

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 16-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    class Meta:
        model = Entidad
        fields = ('id', 'codigo', 'nombre')


class MunicipioSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo Municipio

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 16-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    class Meta:
        model = Municipio
        fields = ('id', 'codigo', 'nombre', 'entidad')


class ParroquiaSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo Parroquia

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 17-08-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    class Meta:
        model = Parroquia
        fields = ('id', 'codigo', 'nombre', 'municipio')
