"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace base.constant
#
# Contiene constantes de uso general en la aplicación
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


## Tipo de documento de identificación
TIPO_DOCUMENTO_IDENTIFICACION = (
    ('V', 'V'), ('E', 'E'), ('P', 'P')
)

## Lista de tipos de persona
TIPO_DOCUMENTO_IDENTIFICACION_LIST = [tp[0] for tp in TIPO_DOCUMENTO_IDENTIFICACION]

## Determina el nivel mínimo de validación para la fortaleza de la contraseña. Los valores permitidos son del 0 al 5
FORTALEZA_CONTRASENHA = 3