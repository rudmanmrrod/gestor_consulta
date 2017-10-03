# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package consulta.serializers
#
# Serializadores de los modelos de consulta para el rest framework
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from .models import Consulta, Pregunta, Opcion, TipoPregunta
from rest_framework import serializers

class OpcionSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo opcion

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 22-06-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    
    class Meta:
        model = Opcion
        fields = ('texto_opcion','id')

class TipoPreguntaSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo tipo de pregunta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 22-06-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    
    class Meta:
        model = TipoPregunta
        fields = ('tipo',)

class PreguntaSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo pregunta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-06-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    
    tipo_pregunta = TipoPreguntaSerializer(read_only=True)
    
    opciones = OpcionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pregunta
        fields = ('id','texto_pregunta','tipo_pregunta','opciones')

class ConsultaSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-06-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """

    preguntas = PreguntaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Consulta
        fields = ('id','nombre_consulta', 'activa','preguntas')
