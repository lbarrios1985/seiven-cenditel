"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace usuario.models
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

from base.constant import TIPO_DOCUMENTO_IDENTIFICACION, OCUPACION, NIVELES_ACCESO
from base.models import Institucion


@python_2_unicode_compatible
class UserProfile(models.Model):
    """!
    Clase que gestiona los datos de los usuarios que tendrán acceso al sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    ## Contiene datos sobre el documento de identificación (cédula o pasaporte)
    tipo_documento = models.CharField(
        max_length=9, help_text=_("Cédula o pasaporte del usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d]{7,8}+$',
                _("Introduzca un número de documento válido. Sólo se permite una letra y números con una longitud de "
                  "8 carácteres.")
            ),
        ]
    )

    ## Contiene datos de la ocupación, oficio o profesión del usuario
    ocupacion = models.CharField(max_length=2, choices=OCUPACION[1:])

    ## Establece la última fecha de modificación de la contraseña, lo cual permite establecer la caducidad de la misma
    fecha_modpass = models.DateTimeField(null=True, help_text=_("Fecha en la que se modificó la contraseña"))

    ## Contiene datos sobre la institucion a la cual pertenece el usuario
    institucion = models.ForeignKey(Institucion, help_text=_("Institucion de la cual proviene el usuario"))

    ## Indica el nivel de acceso que tiene el usuario
    nivel_acceso = models.PositiveSmallIntegerField(choices=NIVELES_ACCESO, null=True)


    ## Establece la relación entre el usuario y el perfil
    user = models.OneToOneField(
        User, related_name="profile",
        help_text=_("Relación entre el perfil y el usuario con acceso al sistema")
    )

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase UserProfile

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @version 1.0.0
        """
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfiles")
        ordering = ("tipo_documento",)

    def __str__(self):
        """!
        Método que muestra la información sobre el perfil del usuario

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos del perfil del usuario
        """
        return "%s, %s" % (six.text_type(self.user.first_name), six.text_type(self.user.last_name))