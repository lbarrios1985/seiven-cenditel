"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace productivo.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo productivo
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.forms import ChoiceField, CharField, Select, TextInput
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django import forms


@python_2_unicode_compatible
class UnidadEconomicaForm(forms.Form):
    """!
    Clase que contiene los campos de consulta del sector productivo para unidades económicas

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """

    ## Año de consulta
    anho = ChoiceField(
        label=_(u"Año"), choices=(('2017', '2017'),),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año de consulta")
        })
    )

    nombre = CharField(label=_(u"Nombre de U.E."), widget=TextInput(attrs={
        'class': 'form-control', 'data-toggle': 'tooltip', 'title': _(u"Indique el nombre de la Unidad Económica")
    }), required=False)

    rif = CharField(label=_(u"R.I.F. de U.E."), widget=TextInput(attrs={
        'class': 'form-control', 'data-toggle': 'tooltip', 'title': _(u"Indique el R.I.F. de la Unidad Económica")
    }), required=False)

    estado = ChoiceField(
        label=_(u"Estado"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el Estado a consultar")
        }), required=False
    )
