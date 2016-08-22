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

## Nombre del Sitio
APP_NAME = "SEIVEN"

## Asunto del mensaje de bienvenida
EMAIL_SUBJECT_REGISTRO = "Bienvenido a %s" % APP_NAME

admin_email = ''
if settings.ADMINS:
    ## Contiene el correo electrónico del administrador del sistema
    admin_email = settings.ADMINS[0][1]

## Mensaje de bienvenida utilizado en el registro de usuarios
REGISTRO_MESSAGE = '%s %s %s (spam) %s %s' % \
                   (str(_("Hemos enviado un mensaje de bienvenida con un enlace de activación a la dirección de correo "
                          "suministrada.")),
                    str(_("Por favor confirme el registro haciendo click en el enlace enviado por correo (si lo "
                          "prefiere también puede copiar y pegar el enlace en su navegador).")),
                    str(_("En caso de no recibir el correo enviado por el sistema en su bandeja de entrada, "
                          "se le recomienda revisar la carpeta de correos no deseados")),
                    str(_("y verificar si existe, en caso afirmativo le recomendamos agregar la dirección de correo de "
                          "la aplicación en la libreta de direcciones de su cuenta de correo para que en futuras "
                          "ocasiones no sea filtrado. En caso contrario contacte al administrador del sistema")),
                    str(admin_email))