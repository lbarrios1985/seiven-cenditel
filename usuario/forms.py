"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace forms.models
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de usuario
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals, absolute_import

import logging

from base.constant import (
    TIPO_DOCUMENTO_IDENTIFICACION, TIPO_DOCUMENTO_IDENTIFICACION_LIST, FORTALEZA_CONTRASENHA
)
from base.fields import TipoDocumentoField
from base.forms import TipoDocumentoForm, ClaveForm, CaptchaForm, CorreoForm
from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth.models import User
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, PasswordInput,
    Select, ModelChoiceField)
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from base.models import Institucion, Ocupacion
from base.widgets import TipoDocumentoWidgetReadOnly
from .models import UserProfile

"""!
Contiene el objeto que registra la vitacora de eventos del módulo usuario.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("usuario")


@python_2_unicode_compatible
class AutenticarForm(TipoDocumentoForm, ClaveForm, CaptchaForm):
    """!
    Clase que muestra el formulario de registro de usuarios. Extiende de las clases RifForm, ClaveForm y CaptchaForm

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    class Meta:
        fields = ['tipo_documento', 'clave', 'captcha']

@python_2_unicode_compatible
class OlvidoClaveForm(TipoDocumentoForm, CorreoForm, CaptchaForm):
    """!
    Clase que muestra el formulario para envío de correo electrónico con enlace para la modificación de clave

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    def clean_correo(self):
        correo = self.cleaned_data['correo']

        if not User.objects.filter(email=correo):
            raise forms.ValidationError(_("El correo indicado no existe"))

        return correo


class ModificarClaveForm(ClaveForm, CaptchaForm, forms.Form):
    """!
    Clase que muestra el formulario para la modificación de claves

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-08-2016
    @version 1.0.0
    """

    ## Confirmación de contraseña de acceso
    verificar_contrasenha = CharField(
        label=_("Verificar Contraseña"),
        max_length=128,
        widget=PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Contraseña de acceso"),
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '50',
                'title': _("Indique nuevamente la contraseña de aceso al sistema")
            }
        )
    )

    def clean_clave(self):
        """!
        Método que permite validar el campo de password

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la fortaleza de la contraseña sea inferior al minimo
                establecido
        """
        password_meter = self.data['passwordMeterId']
        if int(password_meter) < FORTALEZA_CONTRASENHA:
            raise forms.ValidationError(_("La contraseña es débil"))
        return self.cleaned_data['clave']

    def clean_verificar_contrasenha(self):
        """!
        Método que permite validar el campo de verificar_contrasenha

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la contrasenha no pueda ser verificada
        """
        verificar_contrasenha = self.cleaned_data['verificar_contrasenha']
        contrasenha = self.data['clave']
        if contrasenha != verificar_contrasenha:
            raise forms.ValidationError(_("La contraseña no es la misma"))

        return verificar_contrasenha


@python_2_unicode_compatible
class RegistroForm(ModelForm):
    """!
    Clase que muestra el formulario de registro de usuarios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-04-2016
    @version 2.0.0
    """

    ## Tipo de documento de identificación
    tipo_documento = TipoDocumentoField()

    ## Nombre del usuario
    nombre = CharField(
        label=_("Nombre"),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Nombres del usuario"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el Nombre"), 'size': '50'
            }
        )
    )

    ## Apellido del usuario
    apellido = CharField(
        label=_("Apellido"),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Apellidos del usuario"),
                'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el Apellido"), 'size': '50'
            }
        )
    )

    ## Correo electrónico de contacto con el usuario
    correo = EmailField(
        label=_("Correo Electrónico"),
        max_length=75,
        widget=EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'placeholder': _("Correo electronico"),
                'data-toggle': 'tooltip', 'size': '50', 'data-rule-required': 'true',
                'title': _("Indique el correo electrónico de contacto con el usuario. "
                           "No se permiten correos de hotmail")
            }
        )
    )

    ## Listado de instituciones registradas en el sistema
    institucion = ModelChoiceField(
        label=_(u"Institución"), queryset=Institucion.objects.all(), empty_label=_(u"Seleccione..."),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione la institución del usuario a registrar")
        })
    )

    ## Listado de instituciones registradas en el sistema
    ocupacion = ModelChoiceField(
        label=_(u"Ocupacion"), queryset=Ocupacion.objects.all(), empty_label=_(u"Seleccione..."),
        widget=Select(attrs={
            'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
            'title': _(u"Seleccione la ocupación o profesión del usuario a registrar")
        })
    )

    ## Contraseña del usuario
    password = CharField(
        label=_("Contraseña"),
        max_length=128,
        widget=PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Contraseña de acceso"),
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '50',
                'title': _("Indique una contraseña de aceso al sistema"), 'onkeyup': 'passwordStrength(this.value)'
            }
        )
    )

    ## Confirmación de contraseña de acceso
    verificar_contrasenha = CharField(
        label=_("Verifique Contraseña"),
        max_length=128,
        widget=PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Contraseña de acceso"),
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '50',
                'title': _("Indique nuevamente la contraseña de aceso al sistema")
            }
        )
    )

    ## Campo para la validación del captcha
    captcha = CaptchaField(
        label=_(u"Captcha"), widget=CaptchaTextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Texto de la imagen"),
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _(u"Indique el texto de la imagen")
        })
    )

    class Meta:
        model = User
        exclude = ['fecha_modpass', 'username', 'first_name', 'last_name', 'email', 'date_joined']


    def clean_tipo_documento(self):
        """!
        Método que permite validar el campo del tipo de documento de identificacion del usuario

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que el tipo de documento no sea válido,
                en caso contrario devuelve el valor actual del campo
        """
        tipo_documento = self.cleaned_data['tipo_documento']

        if tipo_documento[0] not in TIPO_DOCUMENTO_IDENTIFICACION_LIST:
            raise forms.ValidationError(_("Tipo de Documento de Identificación incorrecto"))
        elif User.objects.filter(username=tipo_documento):
            raise forms.ValidationError(_("El Documento de Identificación ya se encuentra registrado"))
        elif not tipo_documento[1:].isdigit():
            raise  forms.ValidationError(_("El Documento de Identificación no es correcto"))

        return tipo_documento

    def clean_correo(self):
        """!
        Método que permite validar el campo de correo electronico

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que el correo electronico ya se encuentre registrado
        """
        correo = self.cleaned_data['correo']

        if User.objects.filter(email=correo):
            raise forms.ValidationError(_("El correo ya esta registrado"))

        return correo

    def clean_password(self):
        """!
        Método que permite validar el campo de password

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la fortaleza de la contraseña sea inferior al minimo
                establecido
        """
        password_meter = self.data['passwordMeterId']
        if int(password_meter) < FORTALEZA_CONTRASENHA:
            raise forms.ValidationError(_("La contraseña es débil"))
        return self.cleaned_data['password']

    def clean_verificar_contrasenha(self):
        """!
        Método que permite validar el campo de verificar_contrasenha

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la contrasenha no pueda ser verificada
        """
        verificar_contrasenha = self.cleaned_data['verificar_contrasenha']
        contrasenha = self.data['password']
        if contrasenha != verificar_contrasenha:
            raise forms.ValidationError(_("La contraseña no es la misma"))

        return verificar_contrasenha


@python_2_unicode_compatible
class PerfilForm(RegistroForm):
    """!
    Clase que muestra el formulario del perfil del usuario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 07-05-2016
    @version 2.0.0
    """

    class Meta:
        model = User
        fields = [
            'tipo_documento', 'institucion', 'ocupacion', 'nombre', 'apellido', 'correo', 'password',
            'verificar_contrasenha', 'captcha'
        ]


    def __init__(self, *args, **kwargs):
        """!
        Método que inicializa la clase del formulario PerfilForm

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param *kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        """
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        if self.data.__contains__('password') and self.data['password'] != '':
            self.fields['password'].required = True
            self.fields['verificar_contrasenha'].required = True
        self.fields['tipo_documento'].required = False
        self.fields['tipo_documento'].widget = TipoDocumentoWidgetReadOnly()
        self.fields['password'].help_text = 'passwordMeterId'


    def clean_tipo_documento(self):
        """!
        Método que permite validar el campo de tipo de documento de identificacion

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos del campo sin validacion, ya que es de solo lectura a nivel informativo
        """
        return self.cleaned_data['tipo_documento']

    def clean_correo(self):
        """!
        Método que permite validar el campo de correo electronico

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que el correo electronico ya se encuentre registrado
        """
        correo = self.cleaned_data['correo']
        tipo_documento = self.cleaned_data['tipo_documento']

        if User.objects.filter(email=correo).exclude(username=tipo_documento):
            raise forms.ValidationError(_("El correo ya esta registrado"))

        return correo

    def clean_password(self):
        """!
        Método que permite validar el campo de contraseña

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 19-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la fortaleza de la contraseña no sea la adecuada
        """
        if self.cleaned_data['password'] != '':
            password_meter = self.data['passwordMeterId']
            if int(password_meter) < FORTALEZA_CONTRASENHA:
                raise forms.ValidationError(_("La contraseña es débil"))

        return self.cleaned_data['password']
