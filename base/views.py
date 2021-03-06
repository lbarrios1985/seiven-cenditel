"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace base.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo base
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext

from usuario.forms import AutenticarForm

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


def acerca_de(request):
    """!
    Función que permite mostrar información del sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-12-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con la página de información del sistema
    """
    return render(request, 'base.acercade.template.html', {})

@login_required
def inicio(request):
    """!
    Función que permite cargar la pantalla de inicio del sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 01-06-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con la página de inicio del sistema
    """
    form = ''

    if not request.user.is_authenticated:
        form = AutenticarForm()
        return redirect('acceso')

    return render(request, 'base.template.html', {'form': form})