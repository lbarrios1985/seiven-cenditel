"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2016 CENDITEL nodo Mérida
"""
## @namespace productivo.templatetags.productivo_filtros
#
# Contiene filtros a utilizar en los templates del módulo productivo
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django import template

register = template.Library()

input_check = '<div class="checkbox">' \
              '    <div class="checkbox">' \
              '        <label>' \
              '            <input type="checkbox" value="%s">%s' \
              '        </label>' \
              '    </div>' \
              '</div>'

opciones = {
    'unidad_economica': {
        'ue01': str(_("Razón Social")),
        'ue02': str(_("Estado")),
        'ue03': str(_("Municipio")),
        'ue04': str(_("Parroquia")),
        'ue05': str(_("Naturaleza Juridica")),
        'ue06': str(_("Capital Suscrito")),
        'ue07': str(_("Capital Pagado")),
        'ue08': str(_("Distribucion de Capital Suscrito")),
        'ue09': str(_("Numero de trabajadores de la unidad economica")),
        'ue10': str(_("Actividad economica principal")),
        'ue11': str(_("Actividad economica secundaria")),
        'ue12': str(_("Organizacion comunal")),
        'ue13': str(_("Tipo de organizacion comunal")),
        'ue14': str(_("Franquicia")),
        'ue15': str(_("Casa Matriz")),
    },
    'sub_unidad_economica': {
        'sue01': str(_("Nombre")),
        'sue02': str(_("Uso de la sub unidad")),
        'sue03': str(_("Estado")),
        'sue04': str(_("Municipio")),
        'sue05': str(_("Parroquia")),
        'sue06': str(_("Tipo de tenencia")),
        'sue07': str(_("Metros cuadrados de construccion")),
        'sue08': str(_("Metros cuadrados de terreno")),
        'sue09': str(_("Porcentaje de autonomia electrica")),
        'sue10': str(_("Numero de trabajadores")),
        'sue11': str(_("Consumo electrico anual")),
        'sue12': str(_("Presta servicio")),
        'sue13': str(_("Actividad economica principal")),
        'sue14': str(_("Actividad economica secundaria")),
        'sue15': str(_("Capacidad instalada")),
        'sue16': str(_("Capacidad utilizada")),
    },
    'proceso_productivo': {
        'pp01': str(_("Nombre del proceso productivo")),
        'pp02': str(_("Tipo de proceso productivo")),
        'pp03': str(_("Estado del proceso productivo")),
        'pp04': str(_("Cantidad de productos asociados")),
    },
    'actividad_economica': {
        'ae01': str(_("Presta servicio de maquila")),
        'ae02': str(_("Utiliza servicio de maquila")),
        'ae03': str(_("Numero de productos asociados")),
        'ae04': str(_("Exportadora")),
    }
}

@register.simple_tag
def filtros_produccion(tipo):
    filtros = '<div id="opciones-%s">' % tipo
    for f in sorted(opciones[tipo]):
        filtros += input_check % (f, opciones[tipo][f])
    filtros += "</div>"

    return mark_safe(filtros)