"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace economico.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo economico
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .forms import (
    RealPreciosForm, PIBForm, RealDemandaGlobalForm, RealOfertaGlobalForm, MonetarioAgregadosForm, MonetarioOperacionesInterbancariasForm,
    MonetarioTasasInteresForm, MonetarioInstrumentoPoliticaForm, ExternoBalanzaComercialForm, ExternoReservaCambioForm,
    ExternoCuentaCapitalForm, FiscalForm, CapitalForm
)


@login_required
def cargar_datos(request):
    """!
    Función que permite cargar el menú del área económica para el registro de datos

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con la página del sub-menu de carga de datos para el área económica
    """
    return render(request, 'economico.menu.area.html', {})


@login_required
def precios(request):
    """!
    Función que permite mostrar el furmulario para el registro de precios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de precios
    """
    form = RealPreciosForm()

    return render(request, 'economico.precios.html', {
        'form': form, 'url_down': reverse('descargar_archivo'), 'url_up': reverse('cargar_archivo')
    })


@login_required
def pib(request):
    """!
    Función que permite mostrar el furmulario para el registro de PIB

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author Edgar A. Linares (elinares at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @date 05-04-2017
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de PIB
    """
    form = PIBForm()

    return render(request, 'economico.pib.html', {
        'form': form, 'url_down': reverse('descargar_archivo'), 'url_up': reverse('cargar_archivo')
    })


@login_required
def demanda_global(request):
    """!
    Función que permite mostrar el furmulario para el registro de Demanda Global

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Demanda Global
    """
    form = RealDemandaGlobalForm()

    return render(request, 'economico.demanda.global.html', {
        'form': form, 'url_down': reverse('descargar_archivo'), 'url_up': reverse('cargar_archivo')
    })
    
@login_required
def oferta_global(request):
    """!
    Función que permite mostrar el furmulario para el registro de Oferta Global

    @author Ing. Luis Barrios (lbarrios at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-03-2017
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Oferta Global
    """
    form = RealOfertaGlobalForm()

    return render(request, 'economico.oferta.global.html', {
        'form': form, 'url_down': reverse('descargar_archivo'), 'url_up': reverse('cargar_archivo')
    })


@login_required
def agregados_monetarios(request):
    """!
    Función que permite mostrar el furmulario para el registro de Agregados Monetarios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Agregados Monetarios
    """
    form = MonetarioAgregadosForm()

    return render(request, 'economico.agregados.monetarios.html', {'form': form})


@login_required
def operaciones_interbancarias(request):
    """!
    Función que permite mostrar el furmulario para el registro de Operaciones Interbancarias

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Operaciones Interbancarias
    """
    form = MonetarioOperacionesInterbancariasForm()

    return render(request, 'economico.operaciones.interbancarias.html', {'form': form})


@login_required
def tasas_interes(request):
    """!
    Función que permite mostrar el furmulario para el registro de Tasas de Interés

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Tasas de Interés
    """
    form = MonetarioTasasInteresForm()

    return render(request, 'economico.tasas.interes.html', {'form': form})


@login_required
def instrumento_politica(request):
    """!
    Función que permite mostrar el furmulario para el registro de Instrumentos de Políticas

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Instrumentos de Política
    """
    form = MonetarioInstrumentoPoliticaForm()

    return render(request, 'economico.instrumento.politicas.html', {'form': form})


@login_required
def balanza_comercial(request):
    """!
    Función que permite mostrar el furmulario para el registro de Balanza Comercial

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Balanza Comercial
    """
    form = ExternoBalanzaComercialForm()

    return render(request, 'economico.balanza.comercial.html', {'form': form})


@login_required
def reservas_tipo_cambio(request):
    """!
    Función que permite mostrar el furmulario para el registro de Reservas - Tipo de Cambio

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Reservas - Tipo de Cambio
    """
    form = ExternoReservaCambioForm()

    return render(request, 'economico.reservas.tipo.cambio.html', {
        'form': form, 'url_down': reverse('descargar_archivo'), 'url_up': reverse('cargar_archivo')
    })


@login_required
def tributos(request):
    """!
    Función que permite mostrar el furmulario para el registro de Tributos Fiscales

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Tributos Fiscales
    """
    form = FiscalForm()

    return render(request, 'economico.fiscal.html', {'form': form, 'title': _('Tributos')})


@login_required
def ingresos(request):
    """!
    Función que permite mostrar el furmulario para el registro de Ingresos Fiscales

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Ingresos Fiscales
    """
    form = FiscalForm()

    return render(request, 'economico.fiscal.html', {'form': form, 'title': _('Ingresos')})


@login_required
def gastos(request):
    """!
    Función que permite mostrar el furmulario para el registro de Gastos Fiscales

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Gastos Fiscales
    """
    form = FiscalForm()

    return render(request, 'economico.fiscal.html', {'form': form, 'title': _('Gastos')})


@login_required
def endeudamiento(request):
    """!
    Función que permite mostrar el furmulario para el registro de Endeudamiento Fiscal

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-09-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de Endeudamiento Fiscal
    """
    form = FiscalForm()

    return render(request, 'economico.fiscal.html', {'form': form, 'title': _('Endeudamiento')})


@login_required
def capital(request):
    """!
    Función que permite mostrar el furmulario para el registro de Cuenta Capital

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 23-03-2017
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con el formulario de datos para el registro de la Cuenta Capital
    """
    form = CapitalForm()

    return render(request, 'economico.cuenta.capital.html', {'form': form, 'title': _('Cuenta Capital')})