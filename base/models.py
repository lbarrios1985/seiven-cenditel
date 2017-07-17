"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace base.models
#
# Contiene las clases, atributos y métodos para el modelo de datos de usuario
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Institucion(models.Model):
    """!
    Clase que gestiona los datos de las instituciones

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    ## Contiene el nombre de la institución
    nombre = models.CharField(max_length=75)

    ## Contiene una descripción sobre la institución
    descripcion = models.CharField(max_length=255)

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase Institucion

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @version 1.0.0
        """
        verbose_name = _("Institución")
        verbose_name_plural = _("Instituciones")
        ordering = ("nombre",)

    def __str__(self):
        """!
        Método que muestra la información sobre la institución

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos de la institución
        """
        return "%s" % six.text_type(self.nombre)


@python_2_unicode_compatible
class Estado(models.Model):
    """!
    Clase que contiene los Estados de un Pais

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 10-05-2016
    @version 2.0.0
    """

    ## Nombre del Estado
    nombre = models.CharField(max_length=50)

    def __str__(self):
        """!
        Método que muestra la información sobre el Estado

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 29-06-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos del Estado
        """
        return self.nombre

@python_2_unicode_compatible
class AnhoBase(models.Model):
    """!
    Clase que contiene los años base del sistema

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-07-2017
    @version 1.0.0
    """

    anho = models.CharField(max_length=4, unique=True)

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase Anho

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 14-07-2017
        @version 1.0.0
        """
        verbose_name = _("Año Base")
        verbose_name_plural = _("Años Base")
        ordering = ("anho",)

    def __str__(self):
        """!
        Método que muestra la información sobre el año base

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 14-07-2017
        @version 1.0.0
        """
        return self.anho
