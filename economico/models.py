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
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from datetime import datetime

from base.constant import (
    DOMINIO, PERIOCIDAD, TRIMESTRES, MESES, ECONOMICO_SUB_AREA, CONVERT_MES, EMAIL_SUBJECT_LOAD_DATA
)
from base.functions import enviar_correo, check_val_data

import pyexcel

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

administrador, admin_email = '', ''
if settings.ADMINS:
    administrador = settings.ADMINS[0][0]
    admin_email = settings.ADMINS[0][1]


@python_2_unicode_compatible
class Precios(models.Model):
    ## Año base del registro
    anho_base = models.CharField(max_length=4, null=True)

    ## Año al que pertenece el(los) registro(s)
    anho = models.CharField(max_length=4, verbose_name=_("Año"))

    ## Mes del registro
    mes = models.CharField(max_length=2, choices=MESES[1:], verbose_name=_("Mes"))

    ## Índice total a registrar
    inpc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_("INPC"))

    ## Ciudad del registro. La información registrada es solo para el tipo de dominio por ciudad
    ciudad = models.CharField(max_length=3, choices=DOMINIO[1:], null=True, default=None, verbose_name=_("Ciudad"))

    ## Registro del mes y año
    fecha = models.DateField(null=True, verbose_name=_("Fecha"))

    class Meta:
        unique_together = ("anho", "mes")

    def gestion_init(self, *args, **kwargs):
        """!
        Método que permite descargar un archivo con los datos a gestionar

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 05-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve los datos a incluír en el archivo
        """

        fields = [
            [
                {'tag': '', 'cabecera': True},
                {'tag': '', 'cabecera': True},
                {'tag': '', 'cabecera': True},
                {'tag': str(_("Índice por Grupo")), 'color': 'indigo', 'text_color': 'white', 'combine': 13, 'cabecera': True},
                {'tag': str(_("Índice por Sector de Origen")), 'color': 'orange', 'text_color': 'white', 'combine': 3, 'cabecera': True},
                {'tag': str(_("Índice por Naturaleza y Durabilidad")), 'color': 'gray25', 'text_color': 'black', 'combine': 5, 'cabecera': True},
                {'tag': str(_("Índice de Servicios")), 'color': 'green', 'text_color': 'white', 'combine': 3, 'cabecera': True},
                {'tag': str(_("Índice del Núcleo Inflacionario")), 'color': 'red', 'text_color': 'white', 'combine': 5, 'cabecera': True},
                {'tag': str(_("Índice de Productos Controlados y no Controlados")), 'color': 'aqua', 'text_color': 'black', 'combine': 2, 'cabecera': True},
            ],
            [
                {'tag': str(_('Año')), 'cabecera': True}, {'tag': str(_('Mes')), 'cabecera': True}, {'tag': str(_('INPC')), 'cabecera': True},
                {'tag': str(_('(1) Alimentos y Bebidas no Alcoholicas')), 'cabecera': True},
                {'tag': str(_('(2) Bebidas Alcoholicas y Tabaco')), 'cabecera': True},
                {'tag': str(_('(3) Vestido y Calzado')), 'cabecera': True},
                {'tag': str(_('(4) Alquiler de Vivienda')), 'cabecera': True},
                {'tag': str(_('(5) Servicios de Vivienda Excepto Teléfono')), 'cabecera': True},
                {'tag': str(_('(6) Equipamiento de Hogar')), 'cabecera': True},
                {'tag': str(_('(7) Salud')), 'cabecera': True},
                {'tag': str(_('(8) Transporte')), 'cabecera': True},
                {'tag': str(_('(9) Comunicaciones')), 'cabecera': True},
                {'tag': str(_('(10) Esparcimiento y Cultura')), 'cabecera': True},
                {'tag': str(_('(11) Servicios de Educación')), 'cabecera': True},
                {'tag': str(_('(12) Restaurant y Hotel')), 'cabecera': True},
                {'tag': str(_('(13) Bienes y Servicios Diversos')), 'cabecera': True},
                {'tag': str(_('Bienes durables')), 'cabecera': True},
                {'tag': str(_('Bienes semidurables')), 'cabecera': True},
                {'tag': str(_('Bienes no durables')), 'cabecera': True},
                {'tag': str(_('Bienes')), 'cabecera': True},
                {'tag': str(_('Agrícolas')), 'cabecera': True},
                {'tag': str(_('Productos pesqueros')), 'cabecera': True},
                {'tag': str(_('Agroindustrial')), 'cabecera': True},
                {'tag': str(_('Otros manufacturados')), 'cabecera': True},
                {'tag': str(_('Total Servicios')), 'cabecera': True},
                {'tag': str(_('Servicios Básicos')), 'cabecera': True},
                {'tag': str(_('Otros Servicios')), 'cabecera': True},
                {'tag': str(_('Núcleo Inflacionario (NI)')), 'cabecera': True},
                {'tag': str(_('Alimentos Elaborados')), 'cabecera': True},
                {'tag': str(_('Textiles y Prendas de Vestir')), 'cabecera': True},
                {'tag': str(_('Bienes industriales excepto alimentos y textiles')), 'cabecera': True},
                {'tag': str(_('Servicios no administrados')), 'cabecera': True},
                {'tag': str(_('Controlados')), 'cabecera': True},
                {'tag': str(_('No Controlados')), 'cabecera': True}
            ]
        ]
        exclude_fields = ['id', 'anho_base', 'real_precios_id', 'base']

        dominio, data_type = str(_('INPC')), 'N'

        # Condición para filtrar y mostrar la información según la selección del usuario
        if 'dominio' in kwargs:
            if kwargs['dominio'] == 'N':
                kwargs['dominio'] = None
                kwargs['ciudad'] = kwargs.pop('dominio')
            else:
                dominio, data_type = str(_('Ciudad')), 'C'
                kwargs['ciudad__in'] = kwargs.pop('dominio')
                kwargs['ciudad__in'] = [d for d in DOMINIO[1:][0]]
                # Agrega la columna correspondiente a las ciudades
                fields[0].insert(2, {'tag': '', 'cabecera': True})
                fields[1].insert(2, {'tag': dominio, 'cabecera': True})

        elif not 'dominio' in kwargs or not kwargs['dominio'] == 'C':
            exclude_fields.append('ciudad')

        if 'anho_base' in kwargs:
            precios_base = {'anho': kwargs['anho_base']}
            if 'ciudad__in' in kwargs:
                precios_base.update({'ciudad__in': kwargs['ciudad__in']})
        else:
            precios_base = {}

        ## Estrae los registros asociados a descargar en archivo
        for p in Precios.objects.filter(Q(**kwargs) | Q(**precios_base)):
            mes = str(_("Enero"))
            for m in CONVERT_MES:
                if CONVERT_MES[m] == p.mes:
                    mes = str(m)

            # Registros de Año y Mes
            registros = [{'tag': p.anho}, {'tag': mes}]

            # Registros por ciudad si es solicitado
            if data_type == 'C':
                for d in DOMINIO[1:]:
                    if d[0] == p.ciudad:
                        registros.append({'tag': str(d[1])})

            # Índice Nacional de Precios al Consumidor
            registros.append({'tag': str(p.inpc)})

            #Asigna los índices por grupo
            grp = p.preciosgrupo_set.get()
            for g in grp._meta.get_fields():
                if not g.attname in exclude_fields:
                    registros.append({'tag': str(grp.__getattribute__(g.attname))})

            # Asigna los indices por sector de origen
            sec = p.preciossector_set.get()
            for s in sec._meta.get_fields():
                if not s.attname in exclude_fields:
                    registros.append({'tag': str(sec.__getattribute__(s.attname))})

            # Asigna los indices por naturaleza y durabilidad
            nat = p.preciosnaturaleza_set.get()
            for n in nat._meta.get_fields():
                if not n.attname in exclude_fields:
                    registros.append({'tag': str(nat.__getattribute__(n.attname))})

            # Asigna los ínidces por servicio
            ser = p.preciosservicios_set.get()
            for sv in ser._meta.get_fields():
                if not sv.attname in exclude_fields:
                    registros.append({'tag': str(ser.__getattribute__(sv.attname))})

            # Asigna los ínidces por núcleo inflacionario
            inf = p.preciosinflacionario_set.get()
            for ni in inf._meta.get_fields():
                if not ni.attname in exclude_fields:
                    registros.append({'tag': str(inf.__getattribute__(ni.attname))})


            # Asigna los ínidces por productos controlados y no controlados
            prd = p.preciosproductos_set.get()
            for pr in prd._meta.get_fields():
                if not pr.attname in exclude_fields:
                    registros.append({'tag': str(prd.__getattribute__(pr.attname))})

            # Agrega los datos a la nueva fila del archivo a generar
            fields.append(registros)

        return {'fields': fields, 'output': 'precios'}

    def gestion_process(self, file, user, *args, **kwargs):
        """!
        Método que permite cargar y gestionar datos

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 05-12-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param file <b>{string}</b> Ruta y nombre del archivo a gestionar
        @param user <b>{object}</b> Objeto que contiene los datos del usuario que realiza la acción
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve el resultado de la acción con su correspondiente mensaje
        """
        load_file = pyexcel.get_sheet(file_name=file)
        anho_base, i, col_ini, errors, result, message = '', 0, 2, '', True, ''
        load_data_msg = str(_("Datos Cargados"))

        if 'dominio' in kwargs:
            if (kwargs['dominio'] == 'C' and load_file.row[1][2] == 'INPC') or (kwargs['dominio'] == 'N' and load_file.row[1][2] != 'INPC'):
                result = False
        if 'anho_base' in kwargs and kwargs['anho_base'] != load_file.row[2][0]:
            result = False
        if not result:
            return {'result': False, 'message': str(_("El documento a cargar no es válido o no corresponde a los parámetros seleccionados"))}

        for row in load_file.row[2:]:
            try:
                # Asigna el año base del registro
                anho_b = anho_base = row[0] if i == 0 else anho_base

                # Asigna el año de la fila que se esta procesando
                anho = row[0]

                # Asigna el número de mes
                mes = [CONVERT_MES[m] for m in CONVERT_MES if m.find(row[1]) >= 0][0]

                # Asigna la ciudad si el dominio no es nacional
                ciudad = row[2] if 'dominio' in kwargs and kwargs['dominio'] == 'C' else None

                # Asigna el INPC total para el año base
                inpc = row[3] if ciudad else row[2]

                # Condición que indica si el registro corresponde al año base
                base = True if i == 0 else False

                # Registro de año y mes para los filtros
                fecha = datetime(int(anho), int(mes), 1)

                # Condiciones para filtrar la información a cargar según las especificaciones del usuario
                if 'anho_base' in kwargs and kwargs['anho_base'] != load_file.row[2][0]:
                    continue
                if 'fecha__month__gte' in kwargs and 'fecha__month__lte' in kwargs and kwargs[
                    'fecha__month__lte'] < mes < kwargs['fecha__month__gte']:
                    continue
                elif 'fecha__month__gte' in kwargs and mes < kwargs['fecha__month__gte']:
                    continue
                elif 'fecha__month__lte' in kwargs and mes > kwargs['fecha__month__lte']:
                    continue
                if 'fecha__year__gte' in kwargs and 'fecha__year__lte' in kwargs and kwargs[
                    'fecha__year__lte'] < anho < kwargs['fecha__year__gte']:
                    continue
                elif 'fecha__year__gte' in kwargs and anho < kwargs['fecha__year__gte']:
                    continue
                elif 'fecha__year__lte' in kwargs and anho > kwargs['fecha__year__lte']:
                    continue

                # Gestión para los datos básicos de precios
                real_p, created = Precios.objects.update_or_create(
                    anho=anho, mes=mes, ciudad=ciudad, fecha=fecha,
                    defaults={ 'anho_base': anho_b, 'inpc': inpc }
                )


                # Gestión de datos para el Índice por Grupos
                PreciosGrupo.objects.update_or_create(real_precios=real_p, defaults={
                    'base': base,
                    'alimento_bebida': check_val_data(row[4] if self.ciudad else row[3]),
                    'bebida_tabaco': check_val_data(row[5] if self.ciudad else row[4]),
                    'vestido_calzado': check_val_data(row[6] if self.ciudad else row[5]),
                    'alquiler_vivienda': check_val_data(row[7] if self.ciudad else row[6]),
                    'servicio_vivienda': check_val_data(row[8] if self.ciudad else row[7]),
                    'equipamiento_hogar': check_val_data(row[9] if self.ciudad else row[8]),
                    'salud': check_val_data(row[10] if self.ciudad else row[9]),
                    'transporte': check_val_data(row[11] if self.ciudad else row[10]),
                    'comunicaciones': check_val_data(row[12] if self.ciudad else row[11]),
                    'esparcimiento': check_val_data(row[13] if self.ciudad else row[12]),
                    'educacion': check_val_data(row[14] if self.ciudad else row[13]),
                    'restaurant_hotel': check_val_data(row[15] if self.ciudad else row[14]),
                    'bienes_servicios': check_val_data(row[16] if self.ciudad else row[15])
                })

                # Gestión de datos para el Índice por Sector de Origen
                PreciosSector.objects.update_or_create(real_precios=real_p, defaults={
                    'base': base,
                    'durables': check_val_data(row[17] if self.ciudad else row[16]),
                    'semi_durables': check_val_data(row[18] if self.ciudad else row[17]),
                    'no_durables': check_val_data(row[19] if self.ciudad else row[18])
                })

                # Gestión de datos para el Índice por Naturaleza y Durabilidad
                PreciosNaturaleza.objects.update_or_create(real_precios=real_p, defaults={
                    'base': base,
                    'bienes': check_val_data(row[20] if self.ciudad else row[19]),
                    'agricolas': check_val_data(row[21] if self.ciudad else row[20]),
                    'pesquero': check_val_data(row[22] if self.ciudad else row[21]),
                    'agroindustrial': check_val_data(row[23] if self.ciudad else row[22]),
                    'otros': check_val_data(row[24] if self.ciudad else row[23])
                })

                # Gestión de datos para el Índice por Servicios
                PreciosServicios.objects.update_or_create(real_precios=real_p, defaults={
                    'base': base,
                    'total': check_val_data(row[25] if self.ciudad else row[24]),
                    'basicos': check_val_data(row[26] if self.ciudad else row[25]),
                    'otros': check_val_data(row[27] if self.ciudad else row[26])
                })

                # Gestion de datos para el Índice por Núcleo Inflacionario
                PreciosInflacionario.objects.update_or_create(real_precios=real_p, defaults={
                    'base': base,
                    'nucleo': check_val_data(row[28] if self.ciudad else row[27]),
                    'alimentos': check_val_data(row[29] if self.ciudad else row[28]),
                    'textiles': check_val_data(row[30] if self.ciudad else row[29]),
                    'bienes': check_val_data(row[31] if self.ciudad else row[30]),
                    'servicios': check_val_data(row[32] if self.ciudad else row[31])
                })

                # Gestión de datos para el Índice de Productos Controlados y No Controlados
                PreciosProductos.objects.update_or_create(real_precios=real_p, defaults={
                    'base': base,
                    'controlados': check_val_data(row[33] if self.ciudad else row[32]),
                    'no_controlados': check_val_data(row[34] if self.ciudad else row[33])
                })

            except Exception as e:
                errors += "- %s\n" % str(e)

            i += 1

        if errors:
            message = str(_("Error procesando datos. Verifique su correo para detalles del error"))
            load_data_msg = str(_("Error al procesar datos del área Económica - Real"))


        ## Envia correo electronico al usuario indicando el estatus de la carga de datos
        enviar_correo(user.email, 'gestion.informacion.load.mail', EMAIL_SUBJECT_LOAD_DATA, {
            'load_data_msg': load_data_msg, 'administrador': administrador, 'admin_email': admin_email,
            'errors': errors
        })

        return {'result': result, 'message': message}


@python_2_unicode_compatible
class PreciosGrupo(models.Model):

    alimento_bebida = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(1) Alimentos y Bebidas no Alcohólicas")
    )

    bebida_tabaco = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(2) Bebidas Alcohólicas y Tabaco")
    )

    vestido_calzado = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(3) Vestido y Calzado")
    )

    alquiler_vivienda = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(4) Alquiler de Vivienda")
    )

    servicio_vivienda = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(5) Servicios de Vivienda Excepto Teléfono")
    )

    equipamiento_hogar = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(6) Equipamiento de Hogar")
    )

    salud = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(7) Salud")
    )

    transporte = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(8) Transporte")
    )

    comunicaciones = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(9) Comunicaciones")
    )

    esparcimiento = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(10) Esparcimiento y Cultura")
    )

    educacion = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(11) Servicios de Educación")
    )

    retaurant_hotel = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(12) Restaurant y Hotel")
    )

    bienes_servicios = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("(13) Bienes y Servicios Diversos")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    real_precios = models.ForeignKey(Precios, verbose_name=_("Sector Real"))

    class Meta:
        verbose_name = _("Índice por Grupo")


@python_2_unicode_compatible
class PreciosSector(models.Model):

    durables = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Bienes durables")
    )

    semi_durables = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Bienes semidurables")
    )

    no_durables = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Bienes no durables")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    real_precios = models.ForeignKey(Precios, verbose_name=_("Sector Real"))

    class Meta:
        verbose_name = _("Índice por Sector de Origen")


@python_2_unicode_compatible
class PreciosNaturaleza(models.Model):

    bienes = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Bienes")
    )

    agricolas = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Agrícolas")
    )

    pesquero = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Productos Pesqueros")
    )

    agroindustrial = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Agroindustrial")
    )

    otros = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Otros manufacturados")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    real_precios = models.ForeignKey(Precios, verbose_name=_("Sector Real"))

    class Meta:
        verbose_name = _("Índice por Naturaleza y Durabilidad")


@python_2_unicode_compatible
class PreciosServicios(models.Model):
    total = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Total Servicios")
    )

    basicos = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Servicios Básicos")
    )

    otros = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Otros servicios")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    real_precios = models.ForeignKey(Precios, verbose_name=_("Sector Real"))

    class Meta:
        verbose_name = _("Índice de Servicios")

@python_2_unicode_compatible
class PreciosInflacionario(models.Model):
    nucleo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Núcleo Inflacionario (NI)")
    )

    alimentos = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Alimentos Elaborados")
    )

    textiles = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Textiles y Prendas de Vestir")
    )

    bienes = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Bienes Industriales excepto alimentos y textiles")
    )

    servicios = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Servicios no administrados")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    real_precios = models.ForeignKey(Precios, verbose_name=_("Sector Real"))

    class Meta:
        verbose_name = _("Índice del Núcleo Inflacionario")

@python_2_unicode_compatible
class PreciosProductos(models.Model):
    controlados = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Controlados")
    )

    no_controlados = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("No Controlados")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    real_precios = models.ForeignKey(Precios, verbose_name=_("Sector Real"))

    class Meta:
        verbose_name = _("Índice de Productos Controlados y no Controlados")


# ------------ Económico Real - PIB --------------------
@python_2_unicode_compatible
class PIB(models.Model):
    # Año base del registro
    anho_base =  models.CharField(max_length=4, null=True)

    anho = models.CharField(max_length=4, verbose_name=_("Año"))

    nominal = models.DecimalField(
        max_digits=18, decimal_places=2, default=None, null=True, blank=True, verbose_name=_("PIB Nominal")
    )

    class Meta:
        verbose_name = _('Producto Interno Bruto (PIB)')

    def gestion_init(self, *args, **kwargs):
        fields = [
            [
                {'tag': '', 'cabecera': True},
                {'tag': str(PIBDemanda._meta.verbose_name), 'color': 'orange', 'text_color': 'white', 'combine': 4,'cabecera': True},
                {'tag': str(PIBProduccion._meta.verbose_name), 'color': 'green', 'text_color': 'white', 'combine': 3, 'cabecera': True},
            ],
            [
                {'tag': str(_('Año')), 'cabecera': True}
            ]
        ]
        exclude_fields = ['id', 'anho', 'pib_id', 'base']
        is_nominal, is_demanda, is_produccion = True, True, True

        if any('nominal' in index for index in kwargs):
            if kwargs['nominal__isnull'] == "true":
                kwargs['nominal__isnull'] = True
                is_nominal = False
            else:
                kwargs['nominal__isnull'] = False


        if is_nominal:
            fields[0].insert(1, {'tag': '', 'cabecera': True})
            fields[1].extend([{'tag': str(_("PIB Nominal")), 'cabecera': True}])

        demanda = [
            {'tag': str(PIBDemanda._meta.get_field('gasto_consumo').verbose_name), 'cabecera': True},
            {'tag': str(PIBDemanda._meta.get_field('formacion_capital').verbose_name), 'cabecera': True},
            {'tag': str(PIBDemanda._meta.get_field('exportacion_bienes').verbose_name), 'cabecera': True},
            {'tag': str(PIBDemanda._meta.get_field('importacion_bienes').verbose_name), 'cabecera': True}
        ]

        produccion = [
            {'tag': str(PIBProduccion._meta.get_field('valor_agregado').verbose_name), 'cabecera': True},
            {'tag': str(PIBProduccion._meta.get_field('impuesto_producto').verbose_name), 'cabecera': True},
            {'tag': str(PIBProduccion._meta.get_field('subvencion_productos').verbose_name), 'cabecera': True}
        ]

        if any('pibdemanda' in index for index in kwargs):
            kwargs['pibdemanda__isnull'] = False
            kwargs['pibproduccion__isnull'] = True
            fields[1].extend(demanda)
            is_produccion = False
        elif any('pibproduccion' in index for index in kwargs):
            kwargs['pibdemanda__isnull'] = True
            kwargs['pibproduccion__isnull'] = False
            fields[1].extend(produccion)
            is_demanda = False
        else:
            fields[1].extend(demanda)
            fields[1].extend(produccion)

        if 'anho_base' in kwargs:
            pib_base = {'anho_base': kwargs['anho_base']}
            kwargs.pop('anho_base')
        else:
            pib_base = {}

        for pib in PIB.objects.filter(Q(**kwargs) | Q(**pib_base)).order_by('anho'):
            # Registros por año
            registros = [{'tag': pib.anho}]

            if is_nominal:
                registros.append({'tag': str(pib.nominal) if pib.nominal else str(0.0)})

            if is_demanda and pib.pibdemanda_set.all():
                # Asigna los índices por demanda
                dem = pib.pibdemanda_set.get()
                for d in dem._meta.get_fields():
                    if not d.attname in exclude_fields:
                        registros.append({'tag': str(dem.__getattribute__(d.attname))})

            if is_produccion and pib.pibproduccion_set.all():
                # Asigna los índices por oferta
                prod = pib.pibproduccion_set.get()
                for p in prod._meta.get_fields():
                    if not p.attname in exclude_fields:
                        registros.append({'tag': str(prod.__getattribute__(p.attname))})

            # Agrega los datos a la nueva fila del archivo a generar
            fields.append(registros)

        return {'fields': fields, 'output': 'pib'}

    def gestion_process(self, file, user, *args, **kwargs):
        load_file = pyexcel.get_sheet(file_name=file)
        anho_base, i, col_ini, errors, result, message, is_nominal = '', 0, 2, '', True, '', False
        is_demanda, is_produccion = True, True
        load_data_msg = str(_("Datos Cargados"))

        if any('nominal' in index for index in kwargs):
            is_nominal = True
            if load_file.row[1][1] != str(_("PIB Nominal")):
                result = False

        if any('pibdemanda' in index for index in kwargs):
            is_produccion =  False
        if any('pibproduccion' in index for index in kwargs):
            is_demanda = False

        if not result:
            return {
                'result': False,
                'message': str(_("El documento a cargar no es válido o no corresponde a los parámetros seleccionados"))
            }

        for row in load_file.row[2:]:
            try:
                # Asigna el año base del registro
                anho_b = anho_base = row[0] if i == 0 else anho_base

                # Posición inicial desde la cual se van a comenzar a registrar los datos en los modelos asociados
                anho = row[0]

                # Condición que indica si el registro corresponde al año base
                base = True if i == 0 else False

                nominal = row[1] if is_nominal else None

                # Gestión para los datos básicos de pib
                real_pib, created = PIB.objects.update_or_create(anho=anho, anho_base=anho_b, nominal=nominal)

                defaults_demanda = {
                    'base': base,
                    'gasto_consumo': check_val_data(row[2] if is_nominal else row[1]),
                    'formacion_capital': check_val_data(row[3] if is_nominal else row[2]),
                    'exportacion_bienes': check_val_data(row[4] if is_nominal else row[3]),
                    'importacion_bienes': check_val_data(row[5] if is_nominal else row[4])
                }

                if is_demanda:
                    # Gestión de datos para el Índice por Demanda
                    PIBDemanda.objects.update_or_create(pib=real_pib, defaults=defaults_demanda)
                else:
                    # Gestión de datos para el Índice por Producción
                    PIBProduccion.objects.update_or_create(pib=real_pib, defaults={
                        'base': base,
                        'valor_agregado': check_val_data(row[2] if is_nominal else row[1]),
                        'impuesto_producto': check_val_data(row[3] if is_nominal else row[2]),
                        'subvencion_productos': check_val_data(row[4] if is_nominal else row[3]),
                    })
                    continue

                if is_produccion:
                    # Gestión de datos para el Índice por Producción
                    PIBProduccion.objects.update_or_create(pib=real_pib, defaults={
                        'base': base,
                        'valor_agregado': check_val_data(row[6] if is_nominal else row[5]),
                        'impuesto_producto': check_val_data(row[7] if is_nominal else row[6]),
                        'subvencion_productos': check_val_data(row[8] if is_nominal else row[7]),
                    })
                else:
                    # Gestión de datos para el Índice por Demanda
                    PIBDemanda.objects.update_or_create(pib=real_pib, defaults=defaults_demanda)
                    continue

            except Exception as e:
                errors += "- %s\n" % str(e)
            i += 1

        if errors:
            message = str(_("Error procesando datos. Verifique su correo para detalles del error"))
            load_data_msg = str(_("Error al procesar datos del área Económica - PIB"))

        ## Envia correo electronico al usuario indicando el estatus de la carga de datos
        enviar_correo(user.email, 'gestion.informacion.load.mail', EMAIL_SUBJECT_LOAD_DATA, {
            'load_data_msg': load_data_msg, 'administrador': administrador, 'admin_email': admin_email,
            'errors': errors
        })

        return {'result': result, 'message': message}


@python_2_unicode_compatible
class PIBDemanda(models.Model):
    gasto_consumo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Gasto de consumo final")
    )

    formacion_capital = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Formación Bruta de Capital")
    )

    exportacion_bienes = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Exportación de bienes y servicios")
    )

    importacion_bienes = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Menos importaciones de bienes y servicios")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    pib = models.ForeignKey(PIB, verbose_name=_('Producto Interno Bruto'))

    class Meta:
        verbose_name = _('PIB sobre demanda')


@python_2_unicode_compatible
class PIBProduccion(models.Model):
    valor_agregado = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Valor agregado a precios básicos")
    )

    impuesto_producto = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Impuestos sobre los productos")
    )

    subvencion_productos = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Subvenciones sobre los productos")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    pib = models.ForeignKey(PIB, verbose_name=_('Producto Interno Bruto'))

    class Meta:
        verbose_name = _('PIB sobre oferta')


@python_2_unicode_compatible
class PIBActividad(models.Model):
    trimestre = models.CharField(max_length=1, null=True, blank=True, verbose_name=_('Trimestre'))

    total_consolidado = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("PIB Consolidado")
    )

    total_petrolera = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Actividad Petrolera")
    )

    total_no_petrolera = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Actividad No Petrolera")
    )

    mineria = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Mineria")
    )

    manufactura = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Manufactura")
    )

    electricidad_agua = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Electricidad y Agua")
    )

    construccion = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Construcción")
    )

    comercio_servicios = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Comercio y Servicios de Reparación")
    )

    transporte_almacenamiento = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Transporte y almacenamiento")
    )

    comunicaciones = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Comunicaciones")
    )

    instituciones_seguros = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Instituciones Financieras y Seguros")
    )

    servicios_alquiler = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0,
        verbose_name=_("Servicios Inmobiliarios Empresariales y de Alquiler")
    )

    servicios_comunitarios = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0,
        verbose_name=_("Serv. Comunitarios, Soc. Y Personales y Produc. de serv. Priv. no Lucrativos")
    )

    produccion_servicios = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Producción servicios del Gobierno General")
    )

    resto = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Resto")
    )

    sifmi = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Menos Sifmi")
    )

    neto_producto = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Neto Sobre los Productos")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    pib = models.ForeignKey(PIB, verbose_name=_('Producto Interno Bruto'))

    class Meta:
        verbose_name = _('PIB sobre la Actividad')

    def save(self, *args, **kwargs):
        self.total_no_petrolera = self.mineria + self.manufactura + self.electricidad_agua + self.construccion + \
                                  self.comercio_servicios + self.transporte_almacenamiento + self.comunicaciones + \
                                  self.instituciones_seguros + self.servicios_alquiler + self.servicios_comunitarios + \
                                  self.produccion_servicios + self.resto + self.sifmi + self.neto_producto
        self.total_consolidado = self.total_petrolera + self.total_no_petrolera
        super(PIBActividad, self).save(*args, **kwargs)