"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace usuario.urls
#
# Contiene las urls del módulo de usuarios
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from usuario.views import RegistroCreate

urlpatterns = [
    url(r'^login/?$', 'usuario.views.acceso', name='acceso'),
    url(r'^logout/?$', 'usuario.views.salir', name='salir'),
    url(r'^registro/$', RegistroCreate.as_view(), name='registro'),
    url(r'^olvido-clave/$', 'usuario.views.olvido_clave', name='olvido_clave'),
    url(r'^confirm/?$', 'usuario.views.confirmar_registro', name='confirmar_registro'),
    url(r'^confirm-modificar-clave/?$', 'usuario.views.confirmar_modificar_clave', name='confirmar_modificar_clave'),
    url(r'^modificar-clave/?$', 'usuario.views.modificar_clave', name='modificar_clave'),
]