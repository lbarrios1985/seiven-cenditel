"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace economico.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo económico
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import logging

from django import forms
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, PasswordInput,
    Select, MultiWidget, MultiValueField, ChoiceField
)

from base.constant import (
    DOMINIO_PRECIOS, DOMINIO_PIB, TIPO_PIB, TIPO_DEMANDA_GLOBAL, TRIMESTRES
)


"""!
Contiene el objeto que registra la vitacora de eventos del módulo base.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")


class RealPreciosForm(forms.Form):
    """!
    Clase que contiene el formulario para la carga de datos de precios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    ## Dominio del registro
    dominio = ChoiceField(
        label=_(u"Dominio"), choices=DOMINIO_PRECIOS,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el dominio a registrar")
        })
    )

    ## Año base a registrar
    anho_base = ChoiceField(
        label=_(u"Año Base"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año base")
        })
    )

    ## Mes inicial
    periodo_mes_ini = ChoiceField(
        label=_(u"Desde"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el mes inicial")
        })
    )

    ## Año inicial
    periodo_anho_ini = ChoiceField(
        label='', choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año inicial")
        })
    )

    ## Mes final
    periodo_mes_fin = ChoiceField(
        label=_(u"Hasta"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el mes final")
        })
    )

    ## Año final
    periodo_anho_fin = ChoiceField(
        label='', choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año final")
        })
    )


class RealPIBForm(forms.Form):
    """!
    Clase que contiene el formulario para la carga de datos de precios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    ## Tipo de PIB
    tipo = ChoiceField(
        label=_(u"Tipo"), choices=TIPO_PIB,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el tipo de PIB a registrar")
        })
    )

    ## Dominio del registro
    dominio = ChoiceField(
        label=_(u"Dominio"), choices=DOMINIO_PIB,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el dominio a registrar")
        })
    )

    ## Año base a registrar
    anho_base = ChoiceField(
        label=_(u"Año Base"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año base")
        })
    )

    ## Año inicial
    periodo_anho_ini = ChoiceField(
        label=_("Desde"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año inicial")
        })
    )

    ## Año final
    periodo_anho_fin = ChoiceField(
        label=_("hasta"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año final")
        })
    )


class RealDemandaGlobalForm(forms.Form):
    """!
    Clase que contiene el formulario para la carga de datos de demanda global

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    ## Tipo de PIB
    tipo = ChoiceField(
        label=_(u"Tipo"), choices=TIPO_DEMANDA_GLOBAL,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el tipo de Demanda Global a registrar")
        })
    )

    ## Año base a registrar
    anho_base = ChoiceField(
        label=_(u"Año Base"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año base")
        })
    )

    ## Trimestre inicial
    periodo_trimestre_ini = ChoiceField(
        label=_(u"Desde"), choices=TRIMESTRES,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el trimestre inicial")
        })
    )

    ## Año inicial
    periodo_anho_ini = ChoiceField(
        label='', choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año inicial")
        })
    )

    ## Trimestre final
    periodo_trimestre_fin = ChoiceField(
        label=_(u"Hasta"), choices=TRIMESTRES,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el trimestre final")
        })
    )

    ## Año final
    periodo_anho_fin = ChoiceField(
        label='', choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año final")
        })
    )