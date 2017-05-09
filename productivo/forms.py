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

from django.forms import (
    ChoiceField, CharField, Select, TextInput, ModelChoiceField, SelectMultiple, CheckboxInput, RadioSelect
)
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django import forms

from base.constant import ANHOS_CONSULTA, TIPOS_ACTIVIDAD_ECONOMICA, TIPOS_UNIDAD
from base.models import Estado

@python_2_unicode_compatible
class AnhoForm(forms.Form):
    ## Año de consulta
    anho = ChoiceField(
        label=_(u"Año"), choices=ANHOS_CONSULTA,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control select-anho', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año de consulta")
        })
    )


@python_2_unicode_compatible
class EstadoForm(forms.Form):
    ## Estado en el que se encuentra ubicada la Unidad Economica
    estado = ModelChoiceField(
        label=_(u"Estado"), queryset=Estado.objects.all(), empty_label=_("Seleccione"),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el Estado a consultar")
        }), required=False
    )


@python_2_unicode_compatible
class UnidadEconomicaForm(AnhoForm, EstadoForm):
    """!
    Clase que contiene los campos de consulta del sector productivo para unidades económicas

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """

    ## Nombre de la Unidad Economica
    nombre = CharField(label=_(u"Nombre de U.E."), widget=TextInput(attrs={
        'class': 'form-control', 'data-toggle': 'tooltip', 'title': _(u"Indique el nombre de la Unidad Económica")
    }), required=False)

    ## R.I.F. de la Unidad Economica
    rif = CharField(label=_(u"R.I.F. de U.E."), widget=TextInput(attrs={
        'class': 'form-control', 'data-toggle': 'tooltip', 'title': _(u"Indique el R.I.F. de la Unidad Económica")
    }), required=False)


@python_2_unicode_compatible
class ActividadEconomicaForm(AnhoForm, EstadoForm):

    ## Determina si la consulta a realizar es mediante todos los codigos CIIU
    ciiu = forms.BooleanField(label=_("Todos los CIIU"), widget=CheckboxInput(attrs={
        'class': '', 'data-toggle': 'tooltip',
        'title': _("Indique si la consulta es de todos los codigo CIIU")
    }), required=False)

    ## Actividad economica de la Unidad
    actividad_economica = forms.ChoiceField(label=_("Actividad Economica"), widget=Select(attrs={
        'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
        'title': _("Seleccione la actividad economica")
    }), required=False)

    tipo_actividad = forms.ChoiceField(label=_("Tipo de Actividad Economica"), widget=RadioSelect(attrs={
        'class': '', 'data-toggle': 'tooltip', 'title': _("Seleccione el tipo de actividad economica")
    }), choices=TIPOS_ACTIVIDAD_ECONOMICA, required=False)

    tipo_unidad = forms.ChoiceField(label=_("Tipo de Unidad"), widget=RadioSelect(attrs={
        'class': '', 'data-toggle': 'tooltip', 'title': _("Seleccione el tipo de unidad economica")
    }), choices=TIPOS_UNIDAD, required=False)
