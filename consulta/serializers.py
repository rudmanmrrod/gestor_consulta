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
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from .models import Consulta, Pregunta, Opcion, TipoPregunta
from rest_framework import serializers

# Serializers define the API representation.
class OpcionSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo opcion

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 22-06-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    
    class Meta:
        model = Opcion
        fields = ('texto_opcion',)

# Serializers define the API representation.
class TipoPreguntaSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo tipo de pregunta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 22-06-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    
    class Meta:
        model = TipoPregunta
        fields = ('tipo',)

# Serializers define the API representation.
class PreguntaSerializer(serializers.HyperlinkedModelSerializer):
    """!
    Metodo que permite serializar el modelo pregunta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 20-06-2017
    @param serializers.HyperlinkedModelSerializer <b>{object}</b> Objeto del serializer
    @return Retorna los datos de contexto
    """
    
    tipo_pregunta = TipoPreguntaSerializer(read_only=True)
    
    opciones = OpcionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pregunta
        fields = ('texto_pregunta','tipo_pregunta','opciones')

# Serializers define the API representation.
class ConsultaSerializer(serializers.HyperlinkedModelSerializer):
    
    preguntas = PreguntaSerializer(many=True, read_only=True)
    class Meta:
        model = Consulta
        fields = ('nombre_consulta', 'activa','preguntas')
        