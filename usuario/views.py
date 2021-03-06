"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @namespace usuario.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de usuario
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

import base64
import hashlib
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core import urlresolvers, signing
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import CreateView, UpdateView, ListView
from django.utils.translation import ugettext_lazy as _

from base.constant import REGISTRO_MESSAGE, UPDATE_MESSAGE, EMAIL_SUBJECT_REGISTRO, CADUCIDAD_LINK_REGISTRO
from base.functions import enviar_correo, calcular_diferencia_fechas
from base.models import Institucion
from .forms import AutenticarForm, RegistroForm, OlvidoClaveForm, ModificarClaveForm, PerfilForm

import logging

from .models import UserProfile

date_now = datetime.now()
logger = logging.getLogger("usuario")

def hash_user(user, is_new_user=False, is_reset=False):
    """!
    Función que permite encriptar los datos del usuario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-08-2016
    @param user <b>{object}</b> Objeto que obtiene los datos del usuario
    @param is_new_user <b>{boolean}</b> Indica si es un nuevo usuario
    @param is_reset <b>{boolean}</b> Indica si se reinician los datos del usuario
    @return Devuelve un enlace cifrado
    """

    if is_new_user or not user.last_login:
        date_to_hash = user.date_joined.isoformat()
    else:
        date_to_hash = user.last_login.isoformat()

    username = user.username
    password = user.password
    date_to_hash = date_to_hash + ("", "|reset")[is_reset]
    cadena = username + "|" + password + "|" + date_to_hash

    hash = hashlib.sha1(cadena.encode("utf-8")).hexdigest()
    return base64.urlsafe_b64encode(bytes(hash, "utf-8"))

def acceso(request):
    """!
    Funcion que gestiona el acceso al sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 23-04-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Redirecciona al usuario a la pagina correspondiente en caso de que se haya autenticado o no
    """
    form = AutenticarForm()
    alert = None

    if request.method == "POST":
        form = AutenticarForm(data=request.POST)

        if form.is_valid():
            username = "%s%s" % (
                request.POST['tipo_documento_0'], request.POST['tipo_documento_1']
            )
            if User.objects.filter(username=username, is_active=True):
                usuario = authenticate(username=username, password=str(request.POST['clave']))

                if usuario is not None:
                    login(request, usuario)
                    usr = User.objects.get(username=username)
                    usr.last_login = datetime.now()
                    usr.save()
                else:
                    logger.error(str(_("Error al autenticar el usuario [%s]") % username))

                logger.info(str(_("Acceso al sistema por el usuario [%s]") % username))
                return HttpResponseRedirect(urlresolvers.reverse("inicio"))
            else:
                alert = str(_("Su usuario se encuentra inactivo. Intente más tarde..."))


    return render(request, 'base.template.html', {'form': form, 'alert': alert})


def salir(request):
    """!
    Funcion que gestiona la salida del sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 23-04-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Redirecciona al usuario a la pagina de inicio, si fue desautenticado lo envia a la pagina de acceso
    """
    user = request.user
    if user.is_authenticated():
        logout(request)

        logger.info("El usuario [%s] salio del sistema" % user)

    return HttpResponseRedirect(urlresolvers.reverse("inicio"))


def olvido_clave(request):
    """!
    Funcion que gestiona el envío de enlace para la modificación de la contraseña

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 06-05-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Redirecciona al usuario a la pagina de acceso al sistema
    """

    form = OlvidoClaveForm()
    alert = None

    if request.method == "POST":
        form = OlvidoClaveForm(data=request.POST)

        if form.is_valid():
            username = "%s%s" % (
                request.POST['tipo_documento_0'], request.POST['tipo_documento_1']
            )

            correo = request.POST['correo']

            usr = User.objects.get(username=username)

            ## Fecha (cifrada) en la que se genero el enlace para la modificacion de contraseña
            date_link_signed = signing.dumps("%s-%s-%s" % (date_now.year, date_now.month, date_now.day))

            link = request.build_absolute_uri("%s?userid=%s&key=%s&date=%s" % (
                urlresolvers.reverse('confirmar_modificar_clave'),
                username, hash_user(usr, is_reset=True).decode(),
                date_link_signed
            ))

            administrador, admin_email = '', ''
            if settings.ADMINS:
                administrador = settings.ADMINS[0][0]
                admin_email = settings.ADMINS[0][1]

            ## Indica si el correo electrónico fue enviado
            enviado = enviar_correo(usr.email, 'usuario.olvido.clave.mail', EMAIL_SUBJECT_REGISTRO, {
                'link': link, 'emailapp': settings.EMAIL_FROM, 'administrador': administrador,
                'admin_email': admin_email
            })

            if not enviado:
                logger.warning(
                    str(_("Ocurrió un inconveniente al enviar el correo de recuperación de clave al usuario [%s]")
                        % username)
                )
            else:
                form = OlvidoClaveForm()
                alert = _("Se le ha enviado, al correo electrónico indicado, la información necesaria para la "
                          "modificación de la contraseña")
                messages.info(request, _("Se le ha enviado, al correo electrónico indicado, la información necesaria "
                                         "para la modificación de la contraseña"))

    return render(request, 'usuario.recuperar.clave.html', {'form': form, 'alert': alert})


def confirmar_modificar_clave(request):
    """!
    Función que permite confirmar el enlace enviado al usuario para la modificación de contraseña

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 06-05-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un mensje al usuario indicando el estatus de la validación del enlace
    """
    userid = request.GET.get('userid', None)
    key = request.GET.get('key', None)
    date_link_generate = request.GET.get('date', None)
    verificado = False
    mensaje = str(_("El usuario ha sido verificado"))
    modificar_clave_url = None

    if userid and key and date_link_generate and User.objects.filter(username=userid):
        user = User.objects.get(username=userid)

        ## Fecha (descifrada) en la que se genero el enlace para la modificacion de contraseña
        link_date = datetime.strptime(signing.loads(date_link_generate), "%Y-%m-%d")

        if calcular_diferencia_fechas(link_date) <= CADUCIDAD_LINK_REGISTRO:
            if key.strip() == hash_user(user, is_reset=True).decode():
                modificar_clave_url = "%s?userid=%s&key=%s" % (
                    urlresolvers.reverse('modificar_clave'), user.username, hash_user(user, is_reset=True)
                )
                verificado = True
            else:
                mensaje = str(_("El usuario no puede ser verificado"))
        else:
            mensaje = str(_("El enlace utilizado expiró. Contacte al administrador del sistema."))

    return render(request, 'usuario.validar.olvido.clave.html', {
        'verificado': verificado, 'emailapp': settings.EMAIL_FROM, 'mensaje': mensaje,
        'modificar_clave_url': modificar_clave_url
    })


def modificar_clave(request):
    """!
    Funcion que gestiona la modificación de contraseña

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 06-05-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Redirecciona al usuario a la pagina de autenticación del sistema
    """
    form = ModificarClaveForm()
    username = request.GET.get('userid', None)

    if request.method == "POST":
        form = ModificarClaveForm(data=request.POST)

        if form.is_valid():
            username = username if username else request.POST['username']
            user = User.objects.get(username=username)
            user.set_password(request.POST['clave'])
            user.save()
            if UserProfile.objects.filter(user=user):
                perfil = UserProfile.objects.get(user=user)
                perfil.fecha_modpass = datetime.now()
                perfil.save()
            messages.info(request, _("Su contraseña ha sido modificada correctamente"))
            alert = str(_("La contraseña fue modificada satisfactoriamente"))
            logger.info(str(_("El usuario [%s] modificó su contraseña por olvido") % username))
            form = AutenticarForm()
            return render(request, 'base.template.html', {'form': form, 'alert': alert})
            #return HttpResponseRedirect(urlresolvers.reverse("acceso"))

    return render(request, 'usuario.modificar.clave.html', {'form': form, 'fortaleza_clave': True, 'username': username})


def confirmar_registro(request):
    """!
    Función que permite confirmar el enlace enviado al usuario durante el registro

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-05-2016
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un mensje al usuario indicando el estatus de la validación del enlace
    """
    userid = request.GET.get('userid', None)
    key = request.GET.get('key', None)
    verificado = False
    mensaje = str(_("El usuario ha sido verificado"))
    login_url = None

    if userid and key and User.objects.filter(username=userid):
        user = User.objects.get(username=userid)
        if calcular_diferencia_fechas(user.date_joined) <= CADUCIDAD_LINK_REGISTRO:
            if key.strip() == hash_user(user, is_new_user=True).decode():
                if UserProfile.objects.filter(user=user, ocupacion='ES'):
                    # Si es estudiante el sistema activa automáticamente el usuario,
                    # en caso contrario debe esperar por la confirmación del administrador
                    user.is_active = True
                    user.save()
                    user_profile = UserProfile.objects.get(user=user)
                    user_profile.nivel_acceso = 3
                else:
                    mensaje = str(_("El enlace fue verificado y el administrador esta evaluando sus credenciales para "
                                    "otorgarle un nivel de acceso al sistema"))
                login_url = "%s?userid=%s&key=%s" % (
                    urlresolvers.reverse('acceso'), user.username, hash_user(user, is_new_user=True)
                )
                verificado = True
            else:
                mensaje = str(_("El usuario no puede ser verificado"))
        else:
            mensaje = str(_("El enlace utilizado expiró. Contacte al administrador del sistema."))

    return render(request, 'usuario.validar.cuenta.html', {
        'verificado': verificado, 'emailapp': settings.EMAIL_FROM, 'mensaje': mensaje, 'login_url': login_url
    })


class RegistroCreate(SuccessMessageMixin, CreateView):
    """!
    Clase que registra usuarios en el sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 25-04-2016
    @version 2.0.0
    """
    model = User
    form_class = RegistroForm
    template_name = 'usuario.registro.html'
    success_url = reverse_lazy('acceso')
    success_message = REGISTRO_MESSAGE

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos del usuario

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 22-08-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['tipo_documento']
        self.object.first_name = form.cleaned_data['nombre']
        self.object.last_name = form.cleaned_data['apellido']
        self.object.set_password(form.cleaned_data['password'])
        self.object.email = form.cleaned_data['correo']
        self.object.save()


        ## Crea el perfil del usuario
        UserProfile.objects.create(
            tipo_documento=form.cleaned_data['tipo_documento'],
            institucion=form.cleaned_data['institucion'],
            ocupacion=form.cleaned_data['ocupacion'],
            user=self.object
        )
        ## Asigna un enlace de verificación en el registro de usuarios
        link = self.request.build_absolute_uri("%s?userid=%s&key=%s" % (
            urlresolvers.reverse(confirmar_registro),
            self.object.username, hash_user(self.object, is_new_user=True).decode()
        ))

        administrador, admin_email = '', ''
        if settings.ADMINS:
            administrador = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        ## Indica si el correo electrónico fue enviado
        enviado = enviar_correo(self.object.email, 'usuario.bienvenida.mail', EMAIL_SUBJECT_REGISTRO, {
            'link': link, 'emailapp': settings.EMAIL_FROM, 'administrador': administrador, 'admin_email': admin_email
        })

        if not enviado:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar el correo de registro al usuario [%s]")
                    % self.object.username)
            )

        return super(RegistroCreate, self).form_valid(form)


class ModificarPerfilView(SuccessMessageMixin, UpdateView):
    """!
    Clase que muestra el formulario de modificación de datos del perfil de usuario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-12-2016
    @version 1.0.0
    """
    model = User #UserProfile
    form_class = PerfilForm
    template_name = 'usuario.update.html'
    success_url = reverse_lazy('inicio')
    success_message = UPDATE_MESSAGE

    def get_initial(self, **kwargs):
        """!
        Metodo que asigna los valores iniciales del formulario del perfil de usuario con los datos actualmente registrados

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date @date 02-12-2016
        @return Retorna los valores iniciales del formulario
        """
        usr = User.objects.get(username=self.request.user)

        return {
            'nombre': usr.first_name, 'apellido': usr.last_name, 'correo': usr.email, 'tipo_documento': usr.username,
            'institucion': self.request.user.profile.institucion.pk, 'ocupacion': self.request.user.profile.ocupacion,
        }

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a modificar los datos del perfil del usuario

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date @date 02-12-2016
        @return Retorna el formulario validado y modifica los datos de perfil del usuario
        """

        self.object = form.save(commit=False)
        usr = User.objects.get(username=self.object.username)
        self.object.password = usr.password
        if self.object.first_name != form.cleaned_data['nombre']:
            self.object.first_name = form.cleaned_data['nombre']
        if self.object.last_name != form.cleaned_data['apellido']:
            self.object.last_name = form.cleaned_data['apellido']
        if self.object.email != form.cleaned_data['correo']:
            self.object.email = form.cleaned_data['correo']
        if form.cleaned_data.get('password', None):
            self.object.set_password(form.cleaned_data['password'])

        self.object.save()

        if UserProfile.objects.filter(user__username=str(self.object.username)):
            perfil = UserProfile.objects.get(user__username=str(self.object.username))
            perfil.ocupacion = form.cleaned_data['ocupacion']
            perfil.institucion = Institucion.objects.get(nombre=form.cleaned_data['institucion'])
            perfil.save()

        messages.info(self.request, UPDATE_MESSAGE)

        return HttpResponseRedirect(self.get_success_url())
