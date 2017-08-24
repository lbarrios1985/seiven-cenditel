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
from django.conf.urls import url
from . import views as economico_views


urlpatterns = [
    url(r'^cargar-datos/?$', economico_views.cargar_datos, name='economico-cargar-datos'),
    url(r'^cargar-datos/precios/$', economico_views.precios, name='economico-precios'),
    url(r'^cargar-datos/pib/$', economico_views.pib, name='economico-pib'),
    url(r'^cargar-datos/demanda-global/$', economico_views.demanda_global, name='economico-demanda-global'),
    url(r'^cargar-datos/agregados-monetarios/$', economico_views.agregados_monetarios, name='economico-agregados-monetarios'),
    url(r'^cargar-datos/operaciones-interbancarias/$', economico_views.operaciones_interbancarias, name='economico-operaciones-interbancarias'),
    url(r'^cargar-datos/tasas-interes/$', economico_views.tasas_interes, name='economico-tasas-interes'),
    url(r'^cargar-datos/instrumentos-politica/$', economico_views.instrumento_politica, name='economico-instrumento-politica'),
    url(r'^cargar-datos/balanza-comercial/$', economico_views.balanza_comercial, name='economico-balanza-comercial'),
    url(r'^cargar-datos/reservas-tipo-cambio/$', economico_views.reservas_tipo_cambio, name='economico-reservas-tipo-cambio'),
    url(r'^cargar-datos/tributos/$', economico_views.tributos, name='economico-tributos'),
    url(r'^cargar-datos/ingresos/$', economico_views.ingresos, name='economico-ingresos'),
    url(r'^cargar-datos/gastos/$', economico_views.gastos, name='economico-gastos'),
    url(r'^cargar-datos/endeudamiento/$', economico_views.endeudamiento, name='economico-endeudamiento'),
    url(r'^cargar-datos/oferta-global/$', economico_views.oferta_global, name='economico-oferta-global'),
    url(r'^cargar-datos/cuenta-capital/$', economico_views.capital, name='economico-cuenta-capital'),

    # URL para las consultas
    url(r'^consultar-datos/?$', economico_views.consultar_datos, name='economico-consultar-datos'),
    url(r'^consultar-datos/precios/$', economico_views.consultar_precios, name='economico-consultar-precios'),
    url(r'^consultar-datos/pib/$', economico_views.consultar_pib, name='economico-consultar-pib'),
    url(r'^consultar-datos/demanda-global/$', economico_views.consultar_demanda_global, name='economico-consultar-demanda-global'),
    url(r'^consultar-datos/agregados-monetarios/$', economico_views.consultar_agregados_monetarios, name='economico-consultar-agregados-monetarios'),
    url(r'^consultar-datos/operaciones-interbancarias/$', economico_views.consultar_operaciones_interbancarias, name='economico-consultar-operaciones-interbancarias'),
    url(r'^consultar-datos/tasas-interes/$', economico_views.consultar_tasas_interes, name='economico-consultar-tasas-interes'),
    url(r'^consultar-datos/instrumentos-politica/$', economico_views.consultar_instrumento_politica, name='economico-consultar-instrumento-politica'),
    url(r'^consultar-datos/balanza-comercial/$', economico_views.consultar_balanza_comercial, name='economico-consultar-balanza-comercial'),
    url(r'^consultar-datos/reservas-tipo-cambio/$', economico_views.consultar_reservas_tipo_cambio, name='economico-consultar-reservas-tipo-cambio'),
    url(r'^consultar-datos/tributos/$', economico_views.consultar_tributos, name='economico-consultar-tributos'),
    url(r'^consultar-datos/ingresos/$', economico_views.consultar_ingresos, name='economico-consultar-ingresos'),
    url(r'^consultar-datos/gastos/$', economico_views.consultar_gastos, name='economico-consultar-gastos'),
    url(r'^consultar-datos/endeudamiento/$', economico_views.consultar_endeudamiento, name='economico-consultar-endeudamiento'),
    url(r'^consultar-datos/oferta-global/$', economico_views.consultar_oferta_global, name='economico-consultar-oferta-global'),
    url(r'^consultar-datos/cuenta-capital/$', economico_views.consultar_capital, name='economico-consultar-cuenta-capital'),
]

## URLs de peticiones AJAX
urlpatterns += [
]