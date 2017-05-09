"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace productivo.urls
#
# Contiene las urls del módulo productivo
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import consultar_datos, UnidadEconomicaView, ActividadEconomicaView


urlpatterns = [
    url(r'^consultar-datos/?$', consultar_datos, name='productivo-consultar-datos'),
    url(r'^consultar-datos/unidad-economica/$', login_required(UnidadEconomicaView.as_view()),
        name="consultar_unidad_economica"),
    url(r'^consultar-datos/actividad-economica/$', login_required(ActividadEconomicaView.as_view()),
        name="consultar_actividad_economica"),
]

## URLs de peticiones AJAX
urlpatterns += [
]