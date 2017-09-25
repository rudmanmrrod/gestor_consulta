# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package consulta.ajax
#
# Clases basadas en ajax
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0

from django.http import JsonResponse
from .models import Pregunta, Opcion

def pregunta_list(request,pk):
    """!
    Función para listar las preguntas relacionadas a una consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 17-02-2017
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param pk <b>{int}</b> Recibe id de la consulta
    @return Retorna un Json con los datos
    """
    preguntas = Pregunta.objects.filter(consulta_id=pk)
    if(preguntas):
        datos = []
        for item in preguntas.all():
            datos.append({"texto_pregunta":item.texto_pregunta,"tipo_pregunta":item.tipo_pregunta_id,
                          "id":item.id})
        return JsonResponse({'success':True,'preguntas':datos})
    return JsonResponse({'success':False,'mensaje':'No se encontraron preguntas'})

def opciones_list(request,pk):
    """!
    Función para listar las opciones relacionadas a una pregunta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 20-02-2017
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param pk <b>{int}</b> Recibe id de la pregunta
    @return Retorna un Json con los datos
    """
    opciones = Opcion.objects.filter(pregunta_id=pk)
    if(opciones):
        datos = []
        for item in opciones.all():
            datos.append({"id":item.id, "texto_opcion":item.texto_opcion})
        return JsonResponse({'success':True,'opciones':datos})
    return JsonResponse({'success':False,'mensaje':'No se encontraron opciones'})

