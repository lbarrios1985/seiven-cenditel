"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace gestion_informacion.urls
#
# Contiene las urls del módulo para la gestión de información
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.conf.urls import url
from . import ajax as gestion_ajax


urlpatterns = [

]


## URLs de peticiones AJAX
urlpatterns += [
    url(r'^ajax/descargar_archivo/?$', gestion_ajax.descargar_archivo, name='descargar_archivo'),
]