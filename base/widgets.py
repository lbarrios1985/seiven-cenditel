"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace base.widgets
#
# Contiene las clases, atributos y métodos para los widgets a implementar en los formularios
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import logging

from django.forms import MultiWidget, Select, TextInput
from django.utils.translation import ugettext_lazy as _

from .constant import (
    TIPO_DOCUMENTO_IDENTIFICACION
)

"""!
Contiene el objeto que registra la vitacora de eventos del módulo base.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")


class TipoDocumentoWidget(MultiWidget):
    """!
    Clase que agrupa los widgets de los campos del tipo de documento de identificación

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    def __init__(self, attrs=None, *args, **kwargs):

        self.attrs = attrs or {}

        widgets = (
            Select(
                attrs={
                    'class': 'select2 form-control', 'data-toggle': 'tooltip',
                    'title': _("Seleccione el tipo de documento (cédula o pasaporte)")
                }, choices=TIPO_DOCUMENTO_IDENTIFICACION
            ),
            TextInput(
                attrs={
                    'class': 'form-control text-center', 'placeholder': '00000000', 'data-mask': '00000000',
                    'data-toggle': 'tooltip', 'maxlength': '8', 'size': '7', 'data-rule-required': 'true',
                    'title': _("Indique el número de R.I.F., si es menor a 8 dígitos complete con ceros a la izquierda")
                }
            )
        )

        super(TipoDocumentoWidget, self).__init__(widgets, attrs, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value[0], value[1:]]
        return [None, None]


class TipoDocumentoWidgetReadOnly(MultiWidget):
    """!
    Clase que agrupa los widgets de los campos del tipo de documento de identificación para solo lectura

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    def __init__(self, attrs=None, *args, **kwargs):

        self.attrs = attrs or {}

        widgets = (
            TextInput(
                attrs={
                    'class': 'form-control text-center', 'data-toggle': 'tooltip', 'readonly': 'readonly',
                    'title': _("Tipo de Documento (Cédula o Pasaporte)"), 'size': '1',
                }
            ),
            TextInput(
                attrs={
                    'class': 'form-control text-center', 'readonly': 'readonly',
                    'data-toggle': 'tooltip', 'maxlength': '8', 'size': '7',
                    'title': _("Número del documento de identificación")
                }
            )
        )

        super(TipoDocumentoWidgetReadOnly, self).__init__(widgets, attrs, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value[0], value[1:]]
        return [None, None]