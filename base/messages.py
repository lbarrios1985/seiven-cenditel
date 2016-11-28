"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace base.messages
#
# Contiene los mensajes del sistema
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

## Mensaje de error para peticiones AJAX
MSG_NOT_AJAX = _("No se puede procesar la petición. "
                 "Verifique que posea las opciones javascript habilitadas e intente nuevamente.")

## Mensaje de error al descargar archivos
MSG_NOT_DOWNLOAD_FILE = _("No ha proporcionado los datos para la descarga del archivo. Verifique!!!")

## Mensaje de error al cargar archivos
MSG_NOT_UPLOAD_FILE = _("No ha proporcionado los datos para cargar la información. Verifique!!!")

## Mensaje que indica que el archivo fue generado correctamente
MSG_CREATED_FILE_SUCCESS = _("El archivo fue generado correctamente")

## Mensaje que indica un error en caso de no haber podido generar el archivo
MSG_CREATED_FILE_ERROR = _("Error creando el archivo, intente nuevamente. Si el error persiste por favor contacte "
                           "al administrador")