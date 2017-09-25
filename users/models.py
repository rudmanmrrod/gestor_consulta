# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package users.models
#
# Modelos correspondientes a los usuarios
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from base.models import Parroquia

class Perfil(models.Model):
    """!
    Clase que gestiona los datos de los perfiles

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @version 1.0.0
    """    
    ## Número de Cédula
    cedula = models.CharField(max_length=10,unique=True)
    
    ## Relación con la parroquía
    parroquia = models.ForeignKey(Parroquia)
    
    ## Relación con el user de django
    user = models.ForeignKey(User)