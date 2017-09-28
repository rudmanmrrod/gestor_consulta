# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.models
#
# Modelos correspondientes a la aplicación base
# @author Argenis Osorio (aosorio at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from __future__ import unicode_literals

from django.db import models

class Entidad(models.Model):
    """!
    Clase que gestiona el modelo de las entidades o estados

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 18-04-2017
    @version 1.0.0
    """
    ## Código de la entidad
    codigo = models.CharField(max_length=50)
    
    ## Nombre de la entidad
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre


class Municipio(models.Model):
    """!
    Clase que gestiona el modelo de los municipios

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 18-04-2017
    @version 1.0.0
    """
    ## Código del municipio
    codigo = models.CharField(max_length=50)
    
    ##  Nombre del municipio
    nombre = models.CharField(max_length=50)
    
    ## Relación con la entidad
    entidad = models.ForeignKey(Entidad)

    def __unicode__(self):
        return self.nombre


class Parroquia(models.Model):
    """!
    Clase que gestiona el modelo de las parriquias

    @author Argenis Osorio (aosorio at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 18-04-2017
    @version 1.0.0
    """
    ## Código de la parroquia
    codigo = models.CharField(max_length=50)
    
    ## Nombre de la parroquia
    nombre = models.CharField(max_length=50)
    
    ## Relación con el municipio
    municipio = models.ForeignKey(Municipio)

    def __unicode__(self):
        return self.nombre
