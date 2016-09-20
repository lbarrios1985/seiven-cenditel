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
    DOMINIO_PRECIOS, DOMINIO_PIB, DOMINIO_AGREGADO_MONETARIO, TIPO_PIB, TIPO_DEMANDA_GLOBAL, TRIMESTRES, MESES,
    DOMINIO_COMERCIAL, DOMINIO_CAMBIO
)


"""!
Contiene el objeto que registra la vitacora de eventos del módulo económico.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("economico")


@python_2_unicode_compatible
class DominioForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del dominio

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Dominio del registro
    dominio = ChoiceField(
        label=_(u"Dominio"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el dominio a registrar")
        })
    )


@python_2_unicode_compatible
class TipoForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del tipo

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Tipo de registro
    tipo = ChoiceField(
        label=_(u"Tipo"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el tipo a registrar")
        })
    )


@python_2_unicode_compatible
class AnhoBaseForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del año base

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Año base a registrar
    anho_base = ChoiceField(
        label=_(u"Año Base"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año base")
        })
    )


@python_2_unicode_compatible
class MesIniForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del período del mes inicial

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Mes inicial
    periodo_mes_ini = ChoiceField(
        label=_(u"Desde"), choices=MESES,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el mes inicial")
        })
    )


@python_2_unicode_compatible
class MesFinForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del período del mes final

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Mes final
    periodo_mes_fin = ChoiceField(
        label=_(u"Hasta"), choices=MESES,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el mes final")
        })
    )


@python_2_unicode_compatible
class AnhoIniForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del período del año inicial

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Año inicial
    periodo_anho_ini = ChoiceField(
        label=_('Desde'), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año inicial")
        })
    )


@python_2_unicode_compatible
class AnhoFinForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del período del año final

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Año final
    periodo_anho_fin = ChoiceField(
        label=_('Hasta'), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el año final")
        })
    )


@python_2_unicode_compatible
class TrimestreIniForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del período del trimestre inicial

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Trimestre inicial
    periodo_trimestre_ini = ChoiceField(
        label=_(u"Desde"), choices=TRIMESTRES,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el trimestre inicial")
        })
    )


@python_2_unicode_compatible
class TrimestreFinForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del período del trimestre final

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Trimestre final
    periodo_trimestre_fin = ChoiceField(
        label=_(u"Hasta"), choices=TRIMESTRES,
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione el trimestre final")
        })
    )


@python_2_unicode_compatible
class SemanaIniForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del período de la semana inicial

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Semana inicial
    periodo_semana_ini = ChoiceField(
        label=_("Desde"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione la semana inicial")
        })
    )


@python_2_unicode_compatible
class SemanaFinForm(forms.Form):
    """!
    Clase que contiene el campo común para la selección del período de la semana final

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """

    ## Semana final
    periodo_semana_fin = ChoiceField(
        label=_("Hasta"), choices=(),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione la semana final")
        })
    )


@python_2_unicode_compatible
class StartDateForm(forms.Form):
    """!
    Clase que contiene el campo común para la fecha inicial de consulta

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """
    start_date = CharField(label=_('Desde'), max_length=10, widget=TextInput(attrs={
        'class': 'form-control fecha', 'data-toggle': 'tooltip', 'title': _('Indique la fecha inicial'),
    }))


@python_2_unicode_compatible
class EndDateForm(forms.Form):
    """!
    Clase que contiene el campo común para la fecha final de consulta

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @version 1.0.0
    """
    end_date = CharField(label=_('Hasta'), max_length=10, widget=TextInput(attrs={
        'class': 'form-control fecha', 'data-toggle': 'tooltip', 'title': _('Indique la fecha final')
    }))


@python_2_unicode_compatible
class RealPreciosForm(AnhoBaseForm, DominioForm, MesIniForm, MesFinForm, AnhoIniForm, AnhoFinForm):
    """!
    Clase que contiene el formulario para la carga de datos de precios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(RealPreciosForm, self).__init__(*args, **kwargs)
        self.fields['dominio'].choices = DOMINIO_PRECIOS


@python_2_unicode_compatible
class RealPIBForm(TipoForm, AnhoBaseForm, DominioForm, AnhoIniForm, AnhoFinForm):
    """!
    Clase que contiene el formulario para la carga de datos de precios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(RealPIBForm, self).__init__(*args, **kwargs)
        self.fields['dominio'].choices = DOMINIO_PIB
        self.fields['tipo'].choices = TIPO_PIB


@python_2_unicode_compatible
class RealDemandaGlobalForm(AnhoBaseForm, AnhoIniForm, AnhoFinForm, TrimestreIniForm, TrimestreFinForm, TipoForm):
    """!
    Clase que contiene el formulario para la carga de datos de demanda global

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(RealDemandaGlobalForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].choices = TIPO_DEMANDA_GLOBAL


@python_2_unicode_compatible
class MonetarioAgregadosForm(
    DominioForm, MesIniForm, MesFinForm, AnhoIniForm, AnhoFinForm, SemanaIniForm, SemanaFinForm, StartDateForm, EndDateForm
):
    """!
    Clase que contiene el formulario para la carga de datos de Agregados Monetarios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(MonetarioAgregadosForm, self).__init__(*args, **kwargs)
        self.fields['dominio'].choices = DOMINIO_AGREGADO_MONETARIO


@python_2_unicode_compatible
class MonetarioOperacionesInterbancariasForm(StartDateForm, EndDateForm):
    """!
    Clase que contiene el formulario para la carga de datos de Operaciones Interbancarias

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """


@python_2_unicode_compatible
class MonetarioTasasInteresForm(SemanaIniForm, SemanaFinForm, MesIniForm, MesFinForm, AnhoIniForm, AnhoFinForm):
    """!
    Clase que contiene el formulario para la carga de datos de Tasas de Interés

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """


@python_2_unicode_compatible
class MonetarioInstrumentoPoliticaForm(MesIniForm, MesFinForm, AnhoIniForm, AnhoFinForm):
    """!
    Clase que contiene el formulario para la carga de datos de Instrumentos de Políticas

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """


@python_2_unicode_compatible
class ExternoBalanzaComercialForm(TipoForm, DominioForm, AnhoBaseForm, TrimestreIniForm, TrimestreFinForm, AnhoIniForm, AnhoFinForm):
    """!
    Clase que contiene el formulario para la carga de datos de Balanza Comercial

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(ExternoBalanzaComercialForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].choices = TIPO_PIB
        self.fields['dominio'].choices = DOMINIO_COMERCIAL


@python_2_unicode_compatible
class ExternoCuentaCapitalForm(forms.Form):
    """!
    Clase que contiene el formulario para la carga de datos de Cuentas de Capital

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """
    pass


@python_2_unicode_compatible
class ExternoReservaCambioForm(
    DominioForm, StartDateForm, EndDateForm, SemanaIniForm, SemanaFinForm, MesIniForm, MesFinForm, AnhoIniForm, AnhoFinForm
):
    """!
    Clase que contiene el formulario para la carga de datos de Reservas - Tipo de Cambio

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(ExternoReservaCambioForm, self).__init__(*args, **kwargs)
        self.fields['dominio'].choices = DOMINIO_CAMBIO


@python_2_unicode_compatible
class FiscalForm(AnhoIniForm, AnhoFinForm):
    """!
    Clase que contiene el formulario para la carga de datos de Registros Fiscales

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @version 1.0.0
    """
