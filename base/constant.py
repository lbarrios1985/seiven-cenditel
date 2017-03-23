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

## Asunto del mensaje de información sobre la carga de datos
EMAIL_SUBJECT_LOAD_DATA = "Gestión de Datos - SEIVEN"

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

## Mensaje a mostrar cuando los datos hayan sido actualizados correctamente
UPDATE_MESSAGE = _("Los datos fueron actualizados con exito.")

## Días de caducidad para el enlace de registro de usuarios
CADUCIDAD_LINK_REGISTRO = 1

## Listado de ocupaciones
OCUPACION = (
    ("", _("Seleccione...")),
    ("EP", _("Empleado Público")),
    ("PR", _("Profesor")),
    ("ES", _("Estudiante")),
    ("OT", _("Otros"))
)

## Niveles de acceso al sistema
NIVELES_ACCESO = (
    (1, _("Nivel I")),
    (2, _("Nivel II")),
    (3, _("Nivel III"))
)

## Dominio sobre los registros
DOMINIO = [
    (("NAC"), _("Nacional")),
    (("CAR"), _("Caracas")),
    (("MAR"), _("Maracay")),
    (("CGY"), _("Ciudad Guayana")),
    (("BPC"), _("Barcelona - Puerto La Cruz")),
    (("VAL"), _("Valencia")),
    (("BAR"), _("Barquisimeto")),
    (("MCB"), _("Maracaibo")),
    (("MRD"), _("Mérida")),
    (("MAT"), _("Maturín")),
    (("SCR"), _("San Cristóbal")),
    (("RNC"), _("Resto Nacional")),
]

## Selección de Dominio de Precios
DOMINIO_PRECIOS = (
    ("", _("Seleccione...")),
    ('N', _("Nacional")),
    ("C", _("Ciudad"))
)

## Selección de Dominio de PIB
DOMINIO_PIB = (
    ("", _("Seleccione...")),
    ('ED', _('Enfoque Demanda')),
    ('EO', _('Enfoque Oferta'))
)

## Selección de Dominio de Agregados Monetarios
DOMINIO_AGREGADO_MONETARIO = (
    ("", _("Seleccione...")),
    ('RB', _('Reservas Bancarias')),
    ('LM', _('Liquidez Monetaria')),
    ('BMU', _('Base Monetaria Uso')),
    ('BMF', _('Base Monetaria Fuente'))
)

## Selección de Dominio Comercial
DOMINIO_COMERCIAL = (
    ("", _("Seleccione...")),
    ('I', _('Importaciones')),
    ('E', _('Exportaciones'))
)

## Selección de dominio de tipo de cambio
DOMINIO_CAMBIO = (
    ("", _("Seleccione...")),
    ('TC', _('Tipo de Cambio')),
    ('RI', _('Reservas Internacionales'))
)

## Selección de dominio de cuenta capital
DOMINIO_CUENTA_CAPITAL = (
    ("", _("Seleccione...")),
    ('BP', _('Balanza de Pagos')),
    ('DE', _('Deuda Externa'))
)

## Selección de Tipo de PIB
TIPO_PIB = (
    ('', _('Seleccione...')),
    ('N', _('Nominal')),
    ('R', _('Real'))
)

## Selección de Tipo de Demanda Global
TIPO_DEMANDA_GLOBAL = (
    ('', _('Seleccione...')),
    ('DG', _('Demanda Global')),
    ('FB', _('Formación Bruta'))
)

## Selección de Trimestres
TRIMESTRES = (
    ('', _('Seleccione...')),
    ('1', _('I')),
    ('2', _('II')),
    ('3', _('III')),
    ('4', _('IV'))
)

## Selección de meses
MESES = (
    ('', _('Seleccione...')),
    ('01', _('Enero')),
    ('02', _('Febrero')),
    ('03', _('Marzo')),
    ('04', _('Abril')),
    ('05', _('Mayo')),
    ('06', _('Junio')),
    ('07', _('Julio')),
    ('08', _('Agosto')),
    ('09', _('Septiembre')),
    ('10', _('Octubre')),
    ('11', _('Noviembre')),
    ('12', _('Diciembre')),
)

## Periocidad en el registro
PERIOCIDAD = (
    ('D', _('Diaria')),
    ('S', _('Semanal')),
    ('M', _('Mensual')),
    ('T', _('Trimestral')),
    ('A', _('Anual')),
)

## Sub área de registro
ECONOMICO_SUB_AREA = [
    (('PRE'), _('Precios')),
    (('PIB'), _('PIB')),
    (('DEM'), _('Demanda')),
    (('OFE'), _('Oferta')),
]


CONVERT_MES = {
    _('Enero') : '01', _('Febrero') : '02', _('Marzo') : '03', _('Abril') : '04', _('Mayo') : '05', _('Junio') : '06',
    _('Julio') : '07', _('Agosto') : '08', _('Septiembre') : '09', _('Octubre') : '10', _('Noviembre') : '11',
    _('Diciembre') : '12',
}
