"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace economico.urls
#
# Contiene las urls del módulo economico
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.conf.urls import url, patterns


urlpatterns = [
    url(r'^cargar-datos/?$', 'economico.views.cargar_datos', name='economico-cargar-datos'),
    url(r'^cargar-datos/precios/$', 'economico.views.precios', name='economico-precios'),
    url(r'^cargar-datos/pib/$', 'economico.views.pib', name='economico-pib'),
    url(r'^cargar-datos/demanda-global/$', 'economico.views.demanda_global', name='economico-demanda-global'),
    url(r'^cargar-datos/agregados-monetarios/$', 'economico.views.agregados_monetarios', name='economico-agregados-monetarios'),
    url(r'^cargar-datos/operaciones-interbancarias/$', 'economico.views.operaciones_interbancarias', name='economico-operaciones-interbancarias'),
    url(r'^cargar-datos/tasas-interes/$', 'economico.views.tasas_interes', name='economico-tasas-interes'),
    url(r'^cargar-datos/instrumentos-politica/$', 'economico.views.instrumento_politica', name='economico-instrumento-politica'),
    url(r'^cargar-datos/balanza-comercial/$', 'economico.views.balanza_comercial', name='economico-balanza-comercial'),
    url(r'^cargar-datos/reservas-tipo-cambio/$', 'economico.views.reservas_tipo_cambio', name='economico-reservas-tipo-cambio'),
    url(r'^cargar-datos/tributos/$', 'economico.views.tributos', name='economico-tributos'),
    url(r'^cargar-datos/ingresos/$', 'economico.views.ingresos', name='economico-ingresos'),
    url(r'^cargar-datos/gastos/$', 'economico.views.gastos', name='economico-gastos'),
    url(r'^cargar-datos/endeudamiento/$', 'economico.views.endeudamiento', name='economico-endeudamiento'),
]


## URLs de peticiones AJAX
urlpatterns += [
]