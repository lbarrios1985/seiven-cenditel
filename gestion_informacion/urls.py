"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace carga_masiva.urls
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para los modelos del área económica
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.conf.urls import url

from .ajax import descargar_archivo, cargar_datos

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

## URLs de peticiones AJAX
urlpatterns = [
    url(r'^ajax/descargar_archivo/?$', descargar_archivo, name='cm_descargar_archivo'),
    url(r'^ajax/cargar_datos/?$', cargar_datos, name='cm_cargar_datos'),
]
