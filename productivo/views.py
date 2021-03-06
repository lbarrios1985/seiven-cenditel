"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace productivo.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo productivo
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import UnidadEconomicaForm, ActividadEconomicaForm


@login_required
def consultar_datos(request):
    """!
    Función que permite cargar el menú de consulta del área productiva

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con la página del sub-menu de consulta del área productiva
    """
    return render(request, 'productivo.menu.area.html', {})


class UnidadEconomicaView(FormView):
    template_name = 'productivo.unidad.economica.html'
    form_class = UnidadEconomicaForm
    success_url = reverse_lazy('consultar_unidad_economica')


class ActividadEconomicaView(FormView):
    template_name = 'productivo.actividad.economica.html'
    form_class = ActividadEconomicaForm
    success_url = reverse_lazy('consultar_actividad_economica')