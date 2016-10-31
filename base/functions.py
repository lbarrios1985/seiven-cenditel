"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace base.functions
#
# Contiene las funcionas básicas de la aplicación
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import logging
import smtplib

from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger('base')

date_now = datetime.now()


def enviar_correo(email, template, subject, vars = None):
    """!
    Función que envía correos electrónicos

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-08-2016
    @param email    <b>{string}</b> Dirección de correo electrónico del destinatario.
    @param template <b>{string}</b> Nombre de la plantilla de correo electrónico a utilizar.
    @param subject  <b>{string}</b> Texto del asunto que contendrá el correo electrónico.
    @param vars     <b>{object}</b> Diccionario de variables que serán pasadas a la plantilla de correo. El valor por defecto es Ninguno.
    @return Devuelve verdadero si el correo fue enviado, en caso contrario, devuelve falso
    """
    if not vars:
        vars = {}

    try:
        ## Obtiene la plantilla de correo a implementar
        t = get_template(template)
        c = Context(vars)
        send_mail(subject, t.render(c), settings.EMAIL_FROM, [email], fail_silently=False)
        logger.info("Correo enviado a %s usando la plantilla %s" % (email, template))
        return True
    except smtplib.SMTPException as e:
        logger.error("Ocurrió un error al enviar el correo a [%(correo)s]. Detalles del error: %(error)s" % {
            'correo': email, 'error': e
        }, exc_info=True)
        return False


def calcular_diferencia_fechas(fecha_inicial, fecha_final=date_now):
    """!
    Función que permite calcular la diferencia de días entre dos fechas

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-05-2016
    @param fecha_inicial <b>{object}</b> Objeto que contiene el datetime de la fecha inicial
    @param fecha_final <b>{object}</b> Objeto que contiene el datetime de la fecha final. Su valor por defecto,
            si no se especifica, es la fecha actual del sistema
    @return Devuelve la diferencia del número de días entre las dos fechas
    """
    date_format = "%d/%m/%Y"
    fecha_inicial = datetime.strptime(fecha_inicial.strftime(date_format), date_format)
    fecha_final = datetime.strptime(fecha_final.strftime(date_format), date_format)
    diff_dates = fecha_final - fecha_inicial

    return diff_dates.days


def cargar_anho_base(anho_inicial=None, anho_final=None):
    """!
    Función que permite cargar una lista de años para la selección del año base

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 17-10-2016
    @param anho_inicial <b>{object}</b> Objeto que contiene el año inicial.
    @param anho_final <b>{object}</b> Objeto que contiene el año final.
    @return Devuelve un listado de años
    """

    anho_final = anho_inicial if anho_inicial else '1950'

    anho_final = anho_final if anho_final else datetime.now()

    lista = ('', _('Seleccione...')),

    try:
        for year in range(anho_inicial, anho_final):
            lista += (year, year),
    except Exception as e:
        pass

    return list