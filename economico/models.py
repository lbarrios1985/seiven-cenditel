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

    anho_base = models.IntegerField(max_length=4, null=True)

    real = models.BooleanField()

    dominio = models.CharField(max_length=3, choices=DOMINIO)

    # Periocidad => Mensual, Trimestral, Anual
    periocidad = models.CharField(max_length=1, choices=PERIOCIDAD)

    anho = models.IntegerField(max_length=4)

    trimestre = models.CharField(max_length=1, choices=TRIMESTRES[1:], null=True)

    mes = models.CharField(max_length=2, choices=MESES[1:], null=True)


@python_2_unicode_compatible
class AreaReal(models.Model):

    sub_area = models.CharField(max_length=3, choices=ECONOMICO_SUB_AREA)

    tipo = models.CharField(max_length=4)

    sub_tipo = models.CharField(max_length=4)

    indice = models.DecimalField(max_digits=18, decimal_places=2)

    sector_real = models.ForeignKey(SectorReal)