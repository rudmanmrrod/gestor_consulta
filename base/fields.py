# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.fields
#
# Contiene las clases, atributos y métodos para los campos personalizados a implementar en los formularios
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0


from django.forms import MultiValueField, ChoiceField, CharField

from rest_framework import serializers

from .constant import SHORT_NACIONALIDAD
from .widgets import CedulaWidget

class CedulaField(MultiValueField):
    """!
    Clase que agrupa los campos de la nacionalidad y número de cédula de identidad en un solo campo del formulario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 26-04-2016
    @version 2.0.0
    """
    widget = CedulaWidget
    default_error_messages = {
        'invalid_choices': "Debe seleccionar una nacionalidad válida"
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': "Debe indicar un número de Cédula",
            'invalid': "El valor indicado no es válido",
            'incomplete': "El número de Cédula esta incompleto"
        }

        fields = (
            ChoiceField(choices=SHORT_NACIONALIDAD),
            CharField(max_length=8)
        )

        label = "Cedula de Identidad:"

        super(CedulaField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return ''.join(data_list)
        return ''
    
class CedulaRestField(serializers.Field):
    def to_representation(self, obj):
        return "some here"

    def to_representation(self, obj):
        """
        Serialize the object's class name.
        """
        return obj.__class__.__name__