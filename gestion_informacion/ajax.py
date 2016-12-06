"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace gestion_informacion.ajax
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para la gestión de información
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals, absolute_import

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.conf import settings

from base.messages import MSG_NOT_AJAX, MSG_NOT_DOWNLOAD_FILE, MSG_NOT_UPLOAD_FILE, MSG_CREATED_FILE_SUCCESS, \
    MSG_CREATED_FILE_ERROR

import logging
import json
import pyexcel
import csv
import xlwt

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
    @date 03-11-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un HttpResponse con el JSON correspondiente al archivo a descargar
    """
    try:
        if not request.is_ajax():
            return HttpResponse(json.dumps({'result': False, 'message': str(MSG_NOT_AJAX)}))

        ## Nombre de la aplicación o módulo
        app = request.GET.get('app', None)

        ## Nombre del modelo en el cual se va a buscar la información a incluir en el archivo
        mod = request.GET.get('mod', None)

        filter = request.GET.get('filter', None)

        if filter:
            filter = json.loads(filter)

        if app and mod:
            modelo = apps.get_model(app, mod)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Datos")
            instance = modelo()
            datos = instance.gestion_init(**filter)
            font_bold = xlwt.easyxf('font: bold 1')

            if datos['cabecera'][0]:
                c = 0

                for cabecera in datos['cabecera'][0]:
                    style = font_bold
                    if cabecera['color'] and cabecera['text_color']:
                        style = xlwt.easyxf('pattern: pattern solid, fore_colour %s; font: color %s, bold True; align: horiz center;' % (cabecera['color'], cabecera['text_color']))
                    if cabecera['combine'] > 0:
                        count_merge = c + cabecera['combine']
                        sheet.write_merge(0, 0, c, count_merge, cabecera['tag'], style)
                        c = count_merge + 1
                    else:
                        sheet.write(0, c, cabecera['tag'], style)
                        sheet.col(c).width = 357 * (len(cabecera['tag']) + 1)
                        c += 1

            i = 0
            for cabecera in datos['cabecera'][1]:
                sheet.write(1, i, cabecera['label'], font_bold)
                sheet.col(i).width = 256 * (len(cabecera['label']) + 1)
                i += 1

            # Se obtiene la cantidad de datos
            cantidad = len(datos['data'])
            # Si existen datos se crean las filas requeridas
            if cantidad > 0:
                for i in range(1, cantidad + 1):
                    row = len(datos['cabecera'])
                    for j in range(0, row):
                        sheet.write(i, j, datos['data'][i - 1][j])

            archivo = "%s/%s.xls" % (settings.GESTION_INFORMACION_FILES, datos['output'])

            workbook.save(archivo)

            open_file = "%s.xls" % datos['output']

            return HttpResponse(json.dumps({
                'resultado': True, 'archivo': open_file, 'message': str(MSG_CREATED_FILE_SUCCESS)
            }))

        return HttpResponse(json.dumps({'resultado': False, 'error': str(MSG_NOT_DOWNLOAD_FILE)}))
    except Exception as e:
        message = MSG_CREATED_FILE_ERROR
        if settings.DEBUG:
            message = "%s. ERROR: %s" % (message, e)
    return HttpResponse(json.dumps({'result': False, 'error': str(message)}))