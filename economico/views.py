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
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


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
    return render_to_response('economico.menu.area.html', {}, context_instance=RequestContext(request))