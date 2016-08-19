"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace base.fields
#
# Contiene las clases, atributos y métodos para los campos personalizados a implementar en los formularios
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import logging

from django.forms import MultiValueField, ChoiceField, CharField, TextInput
from django.utils.translation import ugettext_lazy as _

from .constant import (
    TIPO_DOCUMENTO_IDENTIFICACION
)
from .widgets import (
    TipoDocumentoWidget, TipoDocumentoWidgetReadOnly
)

"""!
Contiene el objeto que registra la vitacora de eventos del módulo base.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")


class TipoDocumentoField(MultiValueField):
    """!
    Clase que agrupa los campos del tipo de rif, número de rif y dígito validador del rif en un solo campo del
    formulario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 26-04-2016
    @version 2.0.0
    """
    widget = TipoDocumentoWidget
    default_error_messages = {
        'invalid_choices': _("Debe seleccionar un tipo de documento válido")
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': _("Debe indicar un numero de documento"),
            'invalid': _("El valor indicado no es válido"),
            'incomplete': _("El número del documento está incompleto")
        }

        fields = (
            ChoiceField(choices=TIPO_DOCUMENTO_IDENTIFICACION),
            CharField(max_length=8, min_length=8)
        )

        label = _("Cedula o Pasaporte:")

        super(TipoDocumentoField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):

        if data_list:
            return ''.join(data_list)
        return ''
