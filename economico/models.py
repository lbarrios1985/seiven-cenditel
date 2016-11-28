"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace economico.models
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para los modelos del área económica
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from base.constant import DOMINIO, PERIOCIDAD, TRIMESTRES, MESES, ECONOMICO_SUB_AREA

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@python_2_unicode_compatible
class SectorReal(models.Model):
    """!
    Clase que gestiona los datos del sector real

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    ## Año base del registro
    anho_base = models.CharField(max_length=4, null=True)

    ## Condición que indica si pertenece al área real
    real = models.BooleanField()

    ## Registra el dominio de los datos. Nacional o por Ciudad
    dominio = models.CharField(max_length=3, choices=DOMINIO)

    ## Periocidad en la que se registran los datos => Mensual, Trimestral, Anual
    periocidad = models.CharField(max_length=1, choices=PERIOCIDAD)

    ## Año al que pertenece el(los) registro(s)
    anho = models.CharField(max_length=4)

    ## Trimestre registrado
    trimestre = models.CharField(max_length=1, choices=TRIMESTRES[1:], null=True)

    ## Mes del registro
    mes = models.CharField(max_length=2, choices=MESES[1:], null=True)


@python_2_unicode_compatible
class AreaReal(models.Model):
    """!
    Clase que gestiona los datos del área real

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    ## Sub área a registrar
    sub_area = models.CharField(max_length=3, choices=ECONOMICO_SUB_AREA, verbose_name="Sub Area")

    ## Tipo de registro
    tipo = models.CharField(max_length=4, verbose_name="Tipo")

    ## Sub tipo de registro
    sub_tipo = models.CharField(max_length=4, verbose_name="Sub Tipo")

    ## Índice a registrar
    indice = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Índice")

    ## sector real al que pertenece
    sector_real = models.ForeignKey(SectorReal, verbose_name="Sector Real")

    def gestion_init(self):
        fields, relations, data = [], [], []

        for f in self._meta.get_fields():
            field, label, null = f.attname, f.verbose_name, f.null
            if not field == 'id':
                type, validators, error_messages = f.get_internal_type(), f.validators, f.error_messages

                if type == "ForeignKey":
                    relations.append(f.rel.to)

                fields.append({
                    'field': field, 'label': label, 'type': type, 'null': null, 'validators': validators,
                    'error_messages': error_messages
                })

        return {'cabecera': fields, 'relations': relations, 'data': data, 'output': 'area_real'}