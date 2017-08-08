"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace carga_masiva.ajax
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para los modelos del área económica
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals, absolute_import

import sys
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction
from django.apps import apps
from django.conf import settings
from pyexcel_io import get_data
from datetime import datetime

from base.constant import EMAIL_SUBJECT_CM_RESULT
from base.messages import MSG_NOT_AJAX, MSG_NOT_UPLOAD_FILE, MSG_NOT_DOWNLOAD_FILE
from gestion_informacion.tasks import cargar_datos_masivos

import logging
import json
import pyexcel
import csv
import xlwt

from base.functions import enviar_correo

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

logger = logging.getLogger("carga_masiva")


@login_required
def descargar_archivo(request):
    """!
    Función que permite construir y descargar un archivo de procesamiento de datos por lostes

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 25-05-2017
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente al archivo a descargar
    """

    ## Nombre de la aplicación o módulo
    app = request.GET.get('app', None)

    ## Nombre del modelo en el cual se va a buscar la información a incluir en el archivo
    mod = request.GET.get('mod', None)

    response = HttpResponse(content_type='application/vnd.ms-excel')

    filter = request.GET.get('filter', None)

    if filter:
        filter = json.loads(filter)

    if app and mod:
        modelo = apps.get_model(app, mod)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Datos",cell_overwrite_ok=True)
        instance = modelo()
        datos = instance.gestion_init(**filter)
        i = 0
        for con in datos['fields']:
            index_col= 0
            style='align: horiz center; align: vert center;'
            for cabecera in con:
                if 'color' in cabecera:    
                    style += 'pattern: pattern solid, fore_colour %s;' % cabecera['color']
                if 'text_color' in cabecera:
                    style += 'font: color %s, bold True;' % cabecera['text_color']
                font_bold = xlwt.easyxf(style)
                sheet.write(i, index_col, cabecera['tag'], font_bold)
                
                if 'cabecera' in cabecera:
                    sheet.col(i).width = int (250 * (len(cabecera['tag']) + 1))
                
                if 'combine' in cabecera and cabecera['combine'] > 0:
                    sheet.merge(i, i, index_col, (index_col + (cabecera['combine']-1)), font_bold)
                    index_col = cabecera['combine'] + index_col-1

                if 'dominio'in cabecera:
                    sheet.write(i, 2, cabecera['tag'], font_bold)
                if 'combine_row' in cabecera:
                    sheet.write_merge(i, i+10, 0,0, cabecera['tag'],font_bold)
                if 'combine_row1' in cabecera:
                    sheet.write_merge(i, i+10, 1,1, cabecera['tag'],font_bold)
                else:
                    index_col += 1            
            i += 1

        nombre = app + "_" + datos['output']
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % nombre
        workbook.save(response)

    return response


@login_required
@transaction.atomic
def cargar_datos(request):
    """!
    Función para cargar los datos de carga masiva

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)/ Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 11-08-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente al estado de la petición
    """
    message = ''
    try:
        if not request.is_ajax():

            return HttpResponse(json.dumps({'result': False, 'message': str(MSG_NOT_AJAX)}))

        ## Nombre de la aplicación o módulo
        app = request.POST.get('app', None)

        ## Nombre del modelo en el cual se va a buscar la información a incluir en el archivo
        mod = request.POST.get('mod', None)

        ## Archivo que se va a cargar
        archivo = request.FILES['file']

        filter = json.loads("{%s}" % request.POST.get('filter', ''))

        if app and mod and archivo:
            ## Archivo que se va a cargar
            archivo = request.FILES['file']

            ## Extensión del archivo a procesar
            extension = str(archivo).split(".")[-1]

            content = get_data(archivo.read(), extension)

            procesar_datos = cargar_datos_masivos(app=app, mod=mod, user=request.user, file_content=content,**filter)
            
            return HttpResponse(json.dumps({
                'result': True,
                'message': str(_("Los datos indicados se están cargando, será notificado mediante correo electrónico "
                               "sobre el resultado de los mismos. El tiempo estimado sobre los resultados dependerá de "
                               "la cantidad de datos suministrados en el archivo. Por favor sea paciente. "
                               "En caso de no haber recibido respuesta en más de 24 hrs., por favor intente nuevamente "
                               "o contacte al administrador del sistema."))
            }))
        return HttpResponse(json.dumps({'result': False, 'message': str(_('Faltan Párametros'))}))

    except Exception as e:
        message = _("Ocurrió un error en la carga de datos.")
        if settings.DEBUG:
            message = str(message) + str(e)
            import traceback, sys
            exc_type, exc_value, exc_traceback = sys.exc_info()

    return HttpResponse(json.dumps({'result': False, 'message': str(message)}))
