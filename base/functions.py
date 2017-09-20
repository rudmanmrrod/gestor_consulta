# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.functions
#
# Clases genéricas de la consulta
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from __future__ import unicode_literals
from django.core import signing
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import get_random_string
from consulta.models import Consulta,TipoPregunta, Pregunta
from gestor_consulta.settings import PROCESAMIENTO_PATH
from .models import Entidad, Municipio, Parroquia
from users.models import Perfil
import copy
import os
import shutil

def cargar_tipo_pregunta():
    """!
    Función que permite cargar los tipos de preguntas que existen

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-02-2017
    @return Devuelve una tupla con los tipos de pregunta
    """

    lista = ('', 'Seleccione...'),

    try:
        for tipo_pregunta in TipoPregunta.objects.all():
            lista += (tipo_pregunta.id, tipo_pregunta.tipo),
    except Exception as e:
        pass

    return lista

def cargar_consulta():
    """!
    Función que permite cargar las consultas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-02-2017
    @return Devuelve una tupla con las consultas
    """

    lista = ('', 'Seleccione...'),

    try:
        for consulta in Consulta.objects.filter(activa=True).all():
            lista += (consulta.id, consulta.nombre_consulta),
    except Exception as e:
        pass

    return lista

def cargar_entidad():
    """!
    Función que permite cargar todas las entidades

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @return Devuelve una tupla con las entidades
    """

    lista = ('', 'Seleccione...'),

    try:
        for entidad in Entidad.objects.all():
            lista += (entidad.codigo, entidad.nombre),
    except Exception as e:
        pass

    return lista


def cargar_municipios():
    """!
    Función que permite cargar todas los municipios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @return Devuelve una tupla con los municipios
    """

    lista = ('', 'Seleccione...'),

    try:
        for municipio in Municipio.objects.all():
            lista += (municipio.codigo, municipio.nombre),
    except Exception as e:
        pass

    return lista


def cargar_parroquias():
    """!
    Función que permite cargar todas las parroquias

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @return Devuelve una tupla con las parroquias
    """

    lista = ('', 'Seleccione...'),

    try:
        for parroquia in Parroquia.objects.all():
            lista += (parroquia.codigo, parroquia.nombre),
    except Exception as e:
        pass

    return lista


def validate_cedula(cedula):
    """!
    Función que permite validar la cedula

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @param cedula {str} Recibe el número de cédula
    @return Devuelve verdadero o falso
    """
    
    cedula = Perfil.objects.filter(cedula=cedula)
    if cedula:
        return True
    else:
        return False
    
def validate_email(email):
    """!
    Función que permite validar la cedula

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @param cedula {str} Recibe el número de cédula
    @return Devuelve verdadero o falso
    """
    
    email = User.objects.filter(email=email)
    if email:
        return True
    else:
        return False
    
def validate_username(username):
    """!
    Función que permite validar el nombre de usuario

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2017
    @param username {str} Recibe el nombre de usuario
    @return Devuelve verdadero o falso
    """
    
    usr = User.objects.filter(username=username)
    if usr:
        return True
    else:
        return False
    
def generar_token(id):
    """!
    Función que genera un token en base a un id

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-06-2017
    @param id {int} Recibe el id para generar el token
    @return Devuelve el token
    """
    return get_random_string()+':'+signing.dumps(id)
