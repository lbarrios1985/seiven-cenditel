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
from itertools import islice , cycle

from base.constant import (
    DOMINIO, PERIOCIDAD, TRIMESTRES, MESES, ECONOMICO_SUB_AREA, CONVERT_MES, EMAIL_SUBJECT_LOAD_DATA,
    TIPO_BALANZA_COMERCIAL, DOMINIO_BALANZA_COMERCIAL, BALANZA_DATOS, INVERSION_CARTERA, SECTOR_DEUDA
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
    """!
    Clase que contiene los registros comunes de los modelos relacionados con el Producto Interno Bruto

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author Edgar A. Linares (elinares at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-12-2016
    @date 05-04-2017
    @version 1.0.0
    """

    ## Año base del registro
    anho_base =  models.CharField(max_length=4, null=True)

    ## Año al que pertenece el(los) registro(s)
    anho = models.CharField(max_length=4, verbose_name=_("Año"))

    ## Valor de los registros si son nominales, en caso contrario almacena False
    nominal = models.DecimalField(
        max_digits=18, decimal_places=2, default=None, null=True, blank=True, verbose_name=_("PIB Nominal")
    )

    class Meta:
        verbose_name = _('Producto Interno Bruto (PIB)')

    def gestion_init(self, *args, **kwargs):
        """!
        Método que permite descargar un archivo con los datos a gestionar en base a los parámetros
        provenientes del template economico.pib.html

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @author Edgar A. Linares (elinares at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 05-12-2016
        @date 05-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve los datos a incluír en el archivo correspondiente
        """

        """!
        Sección para la selección de los datos del dominio Enfoque Demanda y Enfoque Oferta
        tanto del tipo Real como Nominal
        """
        if any('pibdemanda' in index for index in kwargs) or any('pibproduccion' in index for index in kwargs):
            fields = [
                [
                    {'tag': '', 'cabecera': True}
                ],
                [
                    {'tag': str(_('Año')), 'cabecera': True}
                ]
            ]
            exclude_fields = ['id', 'anho', 'pib_id', 'base']

            ## Comprobación del tipo de datos a cargar en el archivo
            if any('nominal' in index for index in kwargs):
                is_nominal = True
            else:
                is_nominal = False

            ## Cabecera para el archivo del dominio Enfoque Demanda
            demanda = [
                {'tag': str(PIBDemanda._meta.get_field('gasto_consumo').verbose_name), 'cabecera': True},
                {'tag': str(PIBDemanda._meta.get_field('formacion_capital').verbose_name), 'cabecera': True},
                {'tag': str(PIBDemanda._meta.get_field('exportacion_bienes').verbose_name), 'cabecera': True},
                {'tag': str(PIBDemanda._meta.get_field('importacion_bienes').verbose_name), 'cabecera': True}
            ]

            ## Cabecera para el archivo del dominio Enfoque Oferta
            produccion = [
                {'tag': str(PIBProduccion._meta.get_field('valor_agregado').verbose_name), 'cabecera': True},
                {'tag': str(PIBProduccion._meta.get_field('impuesto_producto').verbose_name), 'cabecera': True},
                {'tag': str(PIBProduccion._meta.get_field('subvencion_productos').verbose_name), 'cabecera': True}
            ]
            """!
            Se incluyen los registros en el archivo a descargar
            y el nombre del archivo correspondiente
            """
            if any('pibdemanda' in index for index in kwargs):
                fields[0].insert(1, {'tag': str(PIBDemanda._meta.verbose_name), 'color': 'orange', 'text_color': 'white', 'combine': 4,'cabecera': True})
                fields[1].extend(demanda)
                if is_nominal:
                    fields[0].insert(1, {'tag': '', 'cabecera': True})
                    fields[1].insert(1, {'tag': str(_("PIB Nominal")), 'cabecera': True})
                    nombre_archivo = 'PIB-Nominal_demanda'
                else:
                    nombre_archivo = 'PIB-Real_demanda'
            elif any('pibproduccion' in index for index in kwargs):
                fields[0].insert(1, {'tag': str(PIBProduccion._meta.verbose_name), 'color': 'green', 'text_color': 'white', 'combine': 3, 'cabecera': True})
                fields[1].extend(produccion)
                if is_nominal:                    
                    nombre_archivo = 'PIB-Nominal_produccion'
                else:
                    nombre_archivo = 'PIB-Real_produccion'

        ## Sección para la selección de los datos del dominio Actividad Económica
        if any('pibactividad' in index for index in kwargs):
            fields = [
                [
                    {'tag': '', 'cabecera': True},
                    {'tag': '', 'cabecera': True},
                    {'tag': str(PIBActividad._meta.verbose_name), 'color': 'orange', 'text_color': 'white', 'combine': 18, 'cabecera': True}
                ],
                [
                    {'tag': str(_('Año')), 'cabecera': True},                    
                    {'tag': str(PIBActividad._meta.get_field('total_consolidado').verbose_name), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('total_petrolera').verbose_name), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('total_no_petrolera').verbose_name), 'color': 'ocean_blue', 'text_color': 'white', 'combine': 2, 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('mineria').verbose_name), 'color': 'gray25', 'text_color': 'white', 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('manufactura').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('electricidad_agua').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('construccion').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('comercio_servicios').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('transporte_almacenamiento').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('comunicaciones').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('instituciones_seguros').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('servicios_alquiler').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('servicios_comunitarios').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('produccion_servicios').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('resto').verbose_name), 'color': 'red', 'text': 'white', 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('sifmi').verbose_name), 'cabecera': True},
                    {'tag': str(PIBActividad._meta.get_field('neto_producto').verbose_name), 'color': 'aqua', 'text_color': 'black', 'cabecera': True}
                ]
            ]
            # Asigna el nombre del archivo a descargar
            nombre_archivo = 'PIB-Actividad_economica'

        ## Sección para la selección de los datos del dominio Actividad Económica
        if any('pibsector' in index for index in kwargs):
            fields = [
                [
                    {'tag': '', 'cabecera': True},
                    {'tag': '', 'cabecera': True},
                    {'tag': str(PIBInstitucion._meta.verbose_name), 'color': 'orange', 'text_color': 'white', 'combine': 2, 'cabecera': True}
                ],
                [
                    {'tag': str(_('Año')), 'cabecera': True},                    
                    {'tag': str(PIBInstitucion._meta.get_field('publico').verbose_name), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                    {'tag': str(PIBInstitucion._meta.get_field('privado').verbose_name), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                ]
            ]
            # Asigna el nombre del archivo a descargar
            nombre_archivo = 'PIB-Institucional'

        """!
        Verifica si se deben cargar los registros de trimestre, de ser afirmativo:
            Carga la cabecera de la columna
            Carga cada uno de los valores de las columnas año y trimestre en base 
            a los parámetros del formulario
        En caso contrario
            Carga cada uno de los valores de la columna año
        """
        diff_anhos = int(kwargs['anho__lte']) - int(kwargs['anho__gte']) + 1        
        if any('trimestre' in index for index in kwargs):
            fields[1].insert(1, {'tag': str(PIBActividad._meta.get_field('trimestre').verbose_name), 'cabecera': True})
            # Almacena los datos de año y trimestre inicial provenientes del formulario
            anho_ini = int(kwargs['anho__gte'])
            trimestre_ini = int(kwargs['trimestre__gte'])

            # Genera los años y trimestres correspondientes a los parámetros del formulario
            registros = []
            while True:
                registros = [({'tag': anho_ini})]
                registros.append({'tag': trimestre_ini})
                # Agrega los datos a la nueva fila del archivo a generar
                fields.append(registros)
                if (anho_ini == int(kwargs['anho__lte']) and trimestre_ini == int(kwargs['trimestre__lte'])):
                    break
                if (trimestre_ini == 4):
                    trimestre_ini = 0
                    anho_ini += 1
                trimestre_ini += 1
        else:
            # Almacena los años de los registros a descargar
            for i in range(diff_anhos):
                registros = [({'tag': int(kwargs['anho__gte']) + i})]
                # Agrega los datos a la nueva fila del archivo a generar
                fields.append(registros)
        ## Devuelve los datos correspondientes al archivo a descargar y el nombre de ese archivo
        return {'fields': fields, 'output': nombre_archivo}

    def gestion_process(self, file, user, *args, **kwargs):
        """!
        Método que permite cargar y gestionar datos

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @author Edgar A. Linares (elinares at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 05-12-2016
        @date 20-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param file <b>{string}</b> Ruta y nombre del archivo a gestionar
        @param user <b>{object}</b> Objeto que contiene los datos del usuario que realiza la acción
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve el resultado de la acción con su correspondiente mensaje
        """

        load_file = pyexcel.get_sheet(file_name=file)
        anho_base, i, col_ini, errors, result, message, is_nominal = '', 0, 2, '', False, '', False
        is_demanda, is_produccion, is_actividad, is_sector = False, False, False, False
        load_data_msg = str(_("Datos Cargados"))

        """!
        Verifica cuál es el archivo que se está cargando en base a los parámetros provenientes
        del template economico.pib.html
        """
        if any('nominal' in index for index in kwargs):
            is_nominal = True
        if any('pibdemanda' in index for index in kwargs):
            is_demanda = True
        elif any('pibproduccion' in index for index in kwargs):
            is_produccion = True
        elif any('pibactividad' in index for index in kwargs):
            is_actividad = True
        elif any('pibsector' in index for index in kwargs):
            is_sector = True

        ## Valida que el archivo corresponde a lo indicado en los parámetros del formulario
        if is_demanda:
            if is_nominal and (load_file.row[1][1] == str(_("PIB Nominal"))):
                result = True
            elif load_file.row[1][1] == str(PIBDemanda._meta.get_field('gasto_consumo').verbose_name):
                result = True
        elif is_produccion:
            if load_file.row[1][1] == str(PIBProduccion._meta.get_field('valor_agregado').verbose_name):
                    result = True
        elif is_actividad:
            if load_file.row[1][2] == str(PIBActividad._meta.get_field('total_consolidado').verbose_name):
                result = True
        elif is_sector:
            if load_file.row[1][2] == str(PIBInstitucion._meta.get_field('publico').verbose_name):
                result = True
        ## Si el archivo no pasa las validaciones, devuelve False y un mensaje indicando el problema
        if not result:
            return {
                'result': False,
                'message': str(_("El documento a cargar no es válido o no corresponde a los parámetros seleccionados"))
            }

        
        ## En base al archivo cargado, se validan y cargan a la base de datos los valores contenidos en el archivo
        for row in load_file.row[2:]:
            try:
                # Asigna el año base del registro
                anho_b = int(kwargs['anho_base'])

                # Posición inicial desde la cual se van a comenzar a registrar los datos en los modelos asociados
                anho = row[0]

                # Condición que indica si el registro corresponde al año base
                base = True if i == 0 else False

                # Almacena el valor en caso de tratarse del archivo PIB-Nominal_demanda o False en caso contrario
                nominal = row[1] if (is_nominal and is_demanda) else None

                # Gestión para los datos básicos de pib
                real_pib, created = PIB.objects.update_or_create(anho=anho, anho_base=anho_b, nominal=nominal)

                if is_demanda:
                    # Gestión de datos para el Índice por Demanda
                    PIBDemanda.objects.update_or_create(pib=real_pib, defaults={
                        'base': base,
                        'gasto_consumo': check_val_data(row[2] if is_nominal else row[1]),
                        'formacion_capital': check_val_data(row[3] if is_nominal else row[2]),
                        'exportacion_bienes': check_val_data(row[4] if is_nominal else row[3]),
                        'importacion_bienes': check_val_data(row[5] if is_nominal else row[4])
                    })
                elif is_produccion:
                    # Gestión de datos para el Índice por Producción
                    PIBProduccion.objects.update_or_create(pib=real_pib, defaults={
                        'base': base,
                        'valor_agregado': check_val_data(row[1]),
                        'impuesto_producto': check_val_data(row[2]),
                        'subvencion_productos': check_val_data(row[3]),
                    })
                elif is_actividad:
                    # Gestión de datos para el ïndice por Actividad Económica
                    PIBActividad.objects.update_or_create(pib=real_pib, defaults={
                        'base': base,
                        'trimestre': check_val_data(row[1]),
                        'total_consolidado': check_val_data(row[2]),
                        'total_petrolera': check_val_data(row[3]),
                        'total_no_petrolera': check_val_data(row[4]),
                        'mineria': check_val_data(row[5]),
                        'manufactura': check_val_data(row[6]),
                        'electricidad_agua': check_val_data(row[7]),
                        'construccion': check_val_data(row[8]),
                        'comercio_servicios': check_val_data(row[9]),
                        'transporte_almacenamiento': check_val_data(row[10]),
                        'comunicaciones': check_val_data(row[11]),
                        'instituciones_seguros': check_val_data(row[12]),
                        'servicios_alquiler': check_val_data(row[13]),
                        'servicios_comunitarios': check_val_data(row[14]),
                        'produccion_servicios': check_val_data(row[15]),
                        'resto': check_val_data(row[16]),
                        'sifmi': check_val_data(row[17]),
                        'neto_producto': check_val_data(row[18])
                    })
                elif is_sector:
                    # Gestión de datos para el Índice por Sector Institucional
                    PIBInstitucion.objects.update_or_create(pib=real_pib, defaults={
                        'base': base,
                        'trimestre': check_val_data(row[1]),
                        'publico': check_val_data(row[2]),
                        'privado': check_val_data(row[3])
                        })

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
    """!
    Clase que contiene los registros del PIB correspondientes al dominio Enfoque Demanda tanto 
    del tipo Real como Nominal

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author Edgar A. Linares (elinares at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-12-2016
    @date 05-04-2017
    @version 1.0.0
    """

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
    """!
    Clase que contiene los registros del PIB correspondientes al dominio Enfoque Oferta tanto 
    del tipo Real como Nominal
    
    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author Edgar A. Linares (elinares at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-12-2016
    @date 05-04-2017
    @version 1.0.0
    """

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
    """!
    Clase que contiene los registros del PIB correspondientes al dominio Actividad Económica
    
    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author Edgar A. Linares (elinares at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-12-2016
    @date 05-04-2017
    @version 1.0.0
    """

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

@python_2_unicode_compatible
class PIBInstitucion(models.Model):
    """!
    Clase que contiene los registros del PIB correspondientes al dominio Sector Institucional
    
    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author Edgar A. Linares (elinares at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-12-2016
    @date 05-04-2017
    @version 1.0.0
    """
    
    trimestre = models.CharField(max_length=1, null=True, blank=True, verbose_name=_('Trimestre'))

    publico = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Publico")
    )

    privado = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Privado")
    )

    base = models.BooleanField(default=False, verbose_name=_("Indicador base"))

    pib = models.ForeignKey(PIB, verbose_name=_('Producto Interno Bruto'))

    class Meta:
        verbose_name = _('PIB sobre las Instituciones')

#-----------------------------Económico Real - Demanda Global

@python_2_unicode_compatible
class DemandaGlobal(models.Model):
    
    ## Año base del registro
    anho_base = models.CharField(max_length=4, null=True)

    ## Año al que pertenece el(los) registro(s)
    anho = models.CharField(max_length=4, verbose_name=_("Año"))

    ## Trimestre seleccionado
    trimestre = models.CharField(max_length=2, choices=TRIMESTRES[1:], verbose_name=_("Trimestre"))

    ## Demanda Global
    demanda_global = models.DecimalField(max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Demanda Global")
    )

    def gestion_init(self, *args, **kwargs):
        """!
        Método que permite descargar un archivo con los datos a gestionar

        @author Ing. Luis Barrios (lbarrios at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve los datos a incluír en el archivo
        """

        fields = [
            [
                {'tag': str(_("Año")), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Trimestre")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Demanda Agregada Interna")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Gasto de consumo final del gobierno")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Gasto de consumo final privado")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Formación bruta de capital fijo")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Variación de existencias")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Exportaciones de bienes y servicios")), 'color': 'black', 'text_color': 'white', 'cabecera': True}
            ]
        ]

        """
        colocar los trimestres y años correspondientes en el archivo de salida segun la seleccion realizada        
        """
        
        x = int (kwargs['trimestre_fin']) - int (kwargs['trimestre_ini']) + 1 +  4 * (int (kwargs['anho_fin']) - int (kwargs['anho_ini'] ))
        lst=['1','2','3','4']

        for i, val in enumerate(lst):
            if kwargs['trimestre_ini'] in val:
                desired = list( islice( cycle( lst), i, i+x)) 
                tmp=0
                lolo=int (kwargs['anho_ini'])
                for a in desired:
                    aux=int(a)
                    aux1=''
                    if aux == 4:
                        aux1=lolo+tmp
                        tmp=tmp+1
                    else:
                        aux1=lolo+tmp
                    fields.append([ {'tag': str(_(str(aux1)))}, {'tag': str(_(str(a)))}]) 


        return {'fields': fields, 'output': 'demanda'}

    def gestion_process(self, file, user, *args, **kwargs):
        """!
        Método que permite cargar y gestionar datos

        @author Ing. Luis Barrios (lbarrios at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param file <b>{string}</b> Ruta y nombre del archivo a gestionar
        @param user <b>{object}</b> Objeto que contiene los datos del usuario que realiza la acción
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve el resultado de la acción con su correspondiente mensaje
        """
        
        ## aqui debo recorrer todo el archivo excel y verificar las celdas
        load_file = pyexcel.get_sheet(file_name=file)
        anho_base, errors, result, message = '', '', True, ''
        load_data_msg = str(_("Datos Cargados"))

        
        for row in load_file.row[1:]:
            try:

                real_demanda , created = DemandaGlobal.objects.update_or_create(anho=row[0], anho_base=kwargs['anho_base'], trimestre=row[1], demanda_global= row[2]+row[7])
                
                ## Se crea  o actualiza el objeto de Demanda Agregada Interna luego de validar el valor en la hoja de calculo

                DemandaAgregadaInterna.objects.update_or_create(demanda_global=real_demanda, defaults={
                    'demanda_agregada_interna': check_val_data(row[2]),
                    'gasto_consumo_final_gobierno': check_val_data(row[3]),
                    'gasto_consumo_final_privado': check_val_data(row[4]),
                    'formacion_bruta_capital_fijo': check_val_data(row[5]),
                    'variación_existencias': check_val_data(row[6]),
                })
                
                #Se crea  o actualiza el objeto de Demanda Agregada Externa luego de validar el valor en la hoja de calculo

                DemandaAgregadaExterna.objects.update_or_create(demanda_global=real_demanda, defaults={
                    'exportacion_bienes_servicios':check_val_data(row[7])
                })
               
            except Exception as e:
                errors += "- %s\n" % str(e)

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
class DemandaAgregadaInterna(models.Model):
    
    demanda_agregada_interna = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Demanda Agragada Interna")
    )

    gasto_consumo_final_gobierno = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Gasto de Consumo Final del Gobierno")
    )

    gasto_consumo_final_privado = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Gasto de Consumo Final Privado")
    )

    formacion_bruta_capital_fijo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Formacion Bruta de Capital Fijo")
    )

    variación_existencias = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Variacion de Existencias")
    )

    demanda_global = models.ForeignKey(DemandaGlobal, verbose_name=_('Demanda Global'))

    class Meta:
        verbose_name = _('Demanda Agragada Interna')

    def save(self, *args, **kwargs):
        self.demanda_agregada_interna = self.gasto_consumo_final_gobierno + self.gasto_consumo_final_privado + \
                                        self.formacion_bruta_capital_fijo + self.variación_existencias
        super(DemandaAgregadaInterna, self).save(*args, **kwargs)

class DemandaAgregadaExterna(models.Model):
    exportacion_bienes_servicios = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Exportación de bienes y servicios")
    )

    demanda_global = models.ForeignKey(DemandaGlobal, verbose_name=_('Demanda GLobal'))

    class Meta:
        verbose_name = _('Demanda Agragada Externa')

#-----------------------------Económico Real - Oferta Global

@python_2_unicode_compatible
class OfertaGlobal(models.Model):
    
    ## Año base del registro
    anho_base = models.CharField(max_length=4, null=True)

    ## Año al que pertenece el(los) registro(s)
    anho = models.CharField(max_length=4, verbose_name=_("Año"))

    ## Trimestre seleccionado
    trimestre = models.CharField(max_length=2, choices=TRIMESTRES[1:], verbose_name=_("Trimestre"))

   
    def gestion_init(self, *args, **kwargs):
        """!
        Método que permite descargar un archivo con los datos a gestionar

        @author Ing. Luis Barrios (lbarrios at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve los datos a incluír en el archivo
        """

        fields = [
            [
                {'tag': str(_("Año")), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Trimestre")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Oferta Global")), 'color': 'blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("PIB")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Petróleo")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("No Petróleo")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Derechos de Importación")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Impuestos netos sobre los productos")), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Importaciones y servicios")), 'color': 'black', 'text_color': 'white', 'cabecera': True}

            ]
        ]

        return {'fields': fields, 'output': 'oferta'}

    def gestion_process(self, file, user, *args, **kwargs):
        """!
        Método que permite cargar y gestionar datos

        @author Ing. Luis Barrios (lbarrios at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-03-2017
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
class OfertaInterna(models.Model):
    
    oferta_interna = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Oferta Interna")
    )

    petroleo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Petróleo")
    )

    no_petroleo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("No Petróleo")
    )

    derechos_importacion = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Derechos de Importación")
    )

    impuestos_netos_productos = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Impuestos Netos sobre los Productos")
    )

    oferta_global = models.ForeignKey(OfertaGlobal, verbose_name=_('Oferta Global'))

    class Meta:
        verbose_name = _('Oferta Interna')

    def save(self, *args, **kwargs):
        self.oferta_interna = self.petroleo + self.no_petroleo + \
                              self.derechos_importacion + self.impuestos_netos_productos
        super(OfertaInterna, self).save(*args, **kwargs)

class OfertaExterna(models.Model):
    importaciones_bienes_servicios = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Importaciones de bienes y servicios")
    )

    oferta_externa = models.ForeignKey(OfertaGlobal, verbose_name=_('Oferta GLobal'))

    class Meta:
        verbose_name = _('Oferta Externa')
        
        
# ------------ Económico Externo - Balanza Comercial  --------------------
        
@python_2_unicode_compatible
class BalanzaComercialBase(models.Model):
    """!
    Clase que contiene los registros base de la Balanza Comercial
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-05-2017
    @version 1.0.0
    """
    
    ## Año base del registro
    anho_base = models.CharField(max_length=4, null=True)

    ## Año al que pertenece el(los) registro(s)
    anho = models.CharField(max_length=4, verbose_name=_("Año"))

    ## Trimestre del registro
    trimestre = models.CharField(max_length=2, choices=TRIMESTRES[1:], verbose_name=_("Trimestre"))
    
    ## Tipo del registro
    tipo = models.CharField(max_length=2, choices=TIPO_BALANZA_COMERCIAL[1:])
    
    ## Dominio del registro
    dominio = models.CharField(max_length=2, choices=DOMINIO_BALANZA_COMERCIAL[1:])
    
    def gestion_init(self, *args, **kwargs):
        """!
        Método que permite descargar un archivo con los datos a gestionar

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 02-05-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve los datos a incluír en el archivo
        """
        nombre_archivo = 'balanza_comercial'
        fields = []
        ## Cabecera para precios corrientes en bs y precios constantes
        if(kwargs['dominio']!='BD' and kwargs['tipo']!='PI'):
            header = [
                {'tag': '', 'cabecera': True},
                {'tag': '', 'cabecera': True},
                {'tag': str(_("Exportaciones de bienes FOB")), 'color': 'ocean_blue', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': '', 'color': 'gray25', 'cabecera': True},
                {'tag': str(_("Importaciones de Bienes CIF")), 'color': 'aqua', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': '', 'color': 'gray25', 'cabecera': True},
            ]
            sub_header = [
                {'tag': str(_("Trimestre")), 'color': 'white', 'text_color': 'black','cabecera': True},
                {'tag': str(_("Año")), 'color': 'white', 'text_color': 'black', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_petroleo').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_no_petroleo').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_petroleo').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_no_petroleo').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialServicios._meta.get_field('exportacion_servicio').verbose_name)), 'color': 'gray25', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_petroleo').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_no_petroleo').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_petroleo').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_no_petroleo').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialServicios._meta.get_field('importacion_servicio').verbose_name)), 'color': 'gray25', 'cabecera': True},
            ]
        ## Cabecera para el índice de precios implícitos
        elif(kwargs['tipo']=='PI'):
            header = [
                {'tag': '', 'cabecera': True},
                {'tag': '', 'cabecera': True},
                {'tag': str(_("Exportaciones de bienes FOB")), 'color': 'ocean_blue', 'text_color': 'white', 'combine': 7, 'cabecera': True},
                {'tag': '', 'color': 'gray25', 'cabecera': True},
                {'tag': str(_("Importaciones de Bienes CIF")), 'color': 'aqua', 'text_color': 'white', 'combine': 7, 'cabecera': True},
                {'tag': '', 'color': 'gray25', 'cabecera': True},
            ]
            sub_header = [
                {'tag': str(_("Trimestre")), 'color': 'white', 'text_color': 'black','cabecera': True},
                {'tag': str(_("Año")), 'color': 'white', 'text_color': 'black', 'cabecera': True},
                {'tag': str(_(BalanzaComercialPrecioImplicito._meta.get_field('exportacion_bien').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialPrecioImplicito._meta.get_field('exportacion_publica').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_petroleo').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_no_petroleo').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialPrecioImplicito._meta.get_field('exportacion_privada').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_petroleo').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_no_petroleo').verbose_name)), 'color': 'ocean_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialServicios._meta.get_field('exportacion_servicio').verbose_name)), 'color': 'gray25', 'cabecera': True},
                {'tag': str(_(BalanzaComercialPrecioImplicito._meta.get_field('importacion_bien').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialPrecioImplicito._meta.get_field('importacion_publica').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_petroleo').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_no_petroleo').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialPrecioImplicito._meta.get_field('importacion_privada').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_petroleo').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_no_petroleo').verbose_name)), 'color': 'aqua', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(BalanzaComercialServicios._meta.get_field('importacion_servicio').verbose_name)), 'color': 'gray25', 'cabecera': True},
            ]
        ## Cabecera para precios corrientes en usd
        else:
            header = [
                {'tag': '', 'color': 'white', 'text_color': 'black','cabecera': True},
                {'tag': '', 'color': 'white', 'text_color': 'black','cabecera': True},
                {'tag': str(_("Exportaciones de bienes FOB")), 'color': 'ocean_blue', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': str(_("Exportaciones de Servicios")), 'color': 'orange', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': str(_("Importaciones de Bienes CIF")), 'color': 'indigo', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': str(_("Fletes y Seguros")), 'color': 'green', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': str(_("Importaciones de Servicios")), 'color': 'aqua', 'text_color': 'white', 'combine': 4, 'cabecera': True},
            ]
            sub_header = [
                {'tag': str(_("Trimestre")), 'cabecera': True},
                {'tag': str(_("Año")), 'cabecera': True},
            ]
            colors = ['ocean_blue','orange','indigo','green','aqua']
            for item in colors:
                sub_header.append({'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_petroleo').verbose_name)), 'color': item, 'text_color': 'white', 'cabecera': True})
                sub_header.append({'tag': str(_(BalanzaComercialDatos._meta.get_field('publico_no_petroleo').verbose_name)), 'color': item, 'text_color': 'white', 'cabecera': True})
                sub_header.append({'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_petroleo').verbose_name)), 'color': item, 'text_color': 'white', 'cabecera': True})
                sub_header.append({'tag': str(_(BalanzaComercialDatos._meta.get_field('privado_no_petroleo').verbose_name)), 'color': item, 'text_color': 'white', 'cabecera': True})
        ## Se añade la cabecera
        fields.append(header);
        ## Se añade la subcabecera
        fields.append(sub_header);
        
        ## Se asigna el año base (si existe)
        anho_base = kwargs['anho_base'] if 'anho_base' in kwargs else ''
        
        # Almacena los datos de año y trimestre inicial provenientes del formulario
        anho_ini = int(kwargs['anho__gte'])
        trimestre_ini = int(kwargs['trimestre__gte'])

        # Genera los años y trimestres correspondientes a los parámetros del formulario
        registros = []
        while True:
            registros = [({'tag': trimestre_ini})]
            registros.append({'tag': anho_ini})
            ## Se intenta búscar el registro base
            balanza_base = BalanzaComercialBase.objects.filter(
                    anho_base=anho_base,
                    anho=anho_ini,
                    trimestre=trimestre_ini,
                    tipo=kwargs['tipo'],
                    dominio=kwargs['dominio']
                )
            ## Si el registro existe se obtiene
            if(balanza_base):
                balanza_base = balanza_base.get()
                ## Si el registro base corresponde a balanza comercial corriente (bs) o constante
                if balanza_base.dominio!='BD' and balanza_base.tipo!='PI':
                    ## Se busca el registro para Exportaciones de bienes FOB
                    balanza_datos_eb = BalanzaComercialDatos.objects.filter(
                        balanza_id=balanza_base.id,
                        tipo="EB"
                    ).get()
                    ## Se busca el registro para Importaciones de Bienes CIF
                    balanza_datos_ib = BalanzaComercialDatos.objects.filter(
                        balanza_id=balanza_base.id,
                        tipo="IB"
                    ).get()
                    ## Se busca el registro de las exportaciones/importaciones de servicios
                    balanza_servicios = BalanzaComercialServicios.objects.filter(balanza_id=balanza_base.id,).get()
                    ## Se añaden los registros a la lista
                    registros.append({'tag':balanza_datos_eb.publico_petroleo})
                    registros.append({'tag':balanza_datos_eb.publico_no_petroleo})
                    registros.append({'tag':balanza_datos_eb.privado_petroleo})
                    registros.append({'tag':balanza_datos_eb.privado_no_petroleo})
                    registros.append({'tag':balanza_servicios.exportacion_servicio})
                    registros.append({'tag':balanza_datos_ib.publico_petroleo})
                    registros.append({'tag':balanza_datos_ib.publico_no_petroleo})
                    registros.append({'tag':balanza_datos_ib.privado_petroleo})
                    registros.append({'tag':balanza_datos_ib.privado_no_petroleo})
                    registros.append({'tag':balanza_servicios.importacion_servicio})
                ## Si el registro corresponde a balanza comercial índice de precios implícitos
                elif(kwargs['tipo']=='PI'):
                    ## Se busca el registro para Exportaciones de bienes FOB
                    balanza_datos_eb = BalanzaComercialDatos.objects.filter(
                        balanza_id=balanza_base.id,
                        tipo="EB"
                    ).get()
                    ## Se busca el registro para Importaciones de Bienes CIF
                    balanza_datos_ib = BalanzaComercialDatos.objects.filter(
                        balanza_id=balanza_base.id,
                        tipo="IB"
                    ).get()
                    ## Se busca el registro de las exportaciones/importaciones de servicios
                    balanza_servicios = BalanzaComercialServicios.objects.filter(balanza_id=balanza_base.id,).get()
                    ## Se buscar el registro para los precios implícitos
                    balanza_implicito = BalanzaComercialPrecioImplicito.objects.filter(balanza = balanza_base.id).get()
                    ## Se añaden los registros a la lista
                    registros.append({'tag':balanza_implicito.exportacion_bien})
                    registros.append({'tag':balanza_implicito.exportacion_publica})
                    registros.append({'tag':balanza_datos_eb.publico_petroleo})
                    registros.append({'tag':balanza_datos_eb.publico_no_petroleo})
                    registros.append({'tag':balanza_implicito.exportacion_privada})
                    registros.append({'tag':balanza_datos_eb.privado_petroleo})
                    registros.append({'tag':balanza_datos_eb.privado_no_petroleo})
                    registros.append({'tag':balanza_servicios.exportacion_servicio})
                    registros.append({'tag':balanza_implicito.importacion_bien})
                    registros.append({'tag':balanza_implicito.importacion_publica})
                    registros.append({'tag':balanza_datos_ib.publico_petroleo})
                    registros.append({'tag':balanza_datos_ib.publico_no_petroleo})
                    registros.append({'tag':balanza_implicito.importacion_privada})
                    registros.append({'tag':balanza_datos_ib.privado_petroleo})
                    registros.append({'tag':balanza_datos_ib.privado_no_petroleo})
                    registros.append({'tag':balanza_servicios.importacion_servicio})
                ## Si el registro corresponde a precios corrientes (usd)
                else:
                    ## Se busca el registro para Exportaciones de bienes FOB
                    balanza_datos_eb = BalanzaComercialDatos.objects.filter(balanza = balanza_base, tipo="EB").get()
                    ## Se busca el registro para Exportaciones de Servicios
                    balanza_datos_es = BalanzaComercialDatos.objects.filter(balanza = balanza_base, tipo="ES").get()
                    ## Se busca el registro para Importaciones de Bienes CIF
                    balanza_datos_ib = BalanzaComercialDatos.objects.filter(balanza = balanza_base, tipo="IB").get()
                    ## Se busca el registro para Fletes y Seguros
                    balanza_datos_fs = BalanzaComercialDatos.objects.filter(balanza = balanza_base, tipo="FS").get()
                    ## Se busca el registro para Importaciones de Servicios
                    balanza_datos_is = BalanzaComercialDatos.objects.filter(balanza = balanza_base, tipo="IS").get()
                    ## Se añaden los registros a la lista
                    registros.append({'tag':balanza_datos_eb.publico_petroleo})
                    registros.append({'tag':balanza_datos_eb.publico_no_petroleo})
                    registros.append({'tag':balanza_datos_eb.privado_petroleo})
                    registros.append({'tag':balanza_datos_eb.privado_no_petroleo})
                    registros.append({'tag':balanza_datos_es.publico_petroleo})
                    registros.append({'tag':balanza_datos_es.publico_no_petroleo})
                    registros.append({'tag':balanza_datos_es.privado_petroleo})
                    registros.append({'tag':balanza_datos_es.privado_no_petroleo})
                    registros.append({'tag':balanza_datos_ib.publico_petroleo})
                    registros.append({'tag':balanza_datos_ib.publico_no_petroleo})
                    registros.append({'tag':balanza_datos_ib.privado_petroleo})
                    registros.append({'tag':balanza_datos_ib.privado_no_petroleo})
                    registros.append({'tag':balanza_datos_fs.publico_petroleo})
                    registros.append({'tag':balanza_datos_fs.publico_no_petroleo})
                    registros.append({'tag':balanza_datos_fs.privado_petroleo})
                    registros.append({'tag':balanza_datos_fs.privado_no_petroleo})
                    registros.append({'tag':balanza_datos_is.publico_petroleo})
                    registros.append({'tag':balanza_datos_is.publico_no_petroleo})
                    registros.append({'tag':balanza_datos_is.privado_petroleo})
                    registros.append({'tag':balanza_datos_is.privado_no_petroleo})
            # Agrega los datos a la nueva fila del archivo a generar
            fields.append(registros)
            if (anho_ini == int(kwargs['anho__lte']) and trimestre_ini == int(kwargs['trimestre__lte'])):
                break
            if (trimestre_ini == 4):
                trimestre_ini = 0
                anho_ini += 1
            trimestre_ini += 1
        
        if(kwargs['tipo']=='PR' and kwargs['dominio']=='BB'):
            nombre_archivo+= '_bolivares_corriente'
        elif(kwargs['tipo']=='PR' and kwargs['dominio']=='BD'):
            nombre_archivo+= '_dolares'
        elif(kwargs['tipo']=='PC'):
            nombre_archivo+= '_bolivares_constante'
        elif(kwargs['tipo']=='PI'):
            nombre_archivo+= '_bolivales_preciosimplicitos'
        ## Devuelve los datos correspondientes al archivo a descargar y el nombre de ese archivo
        return {'fields': fields, 'output': nombre_archivo}
    
    def gestion_process(self, file, user, *args, **kwargs):
        """!
        Método que permite cargar y gestionar datos

        @author Rodrigo boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 02-05-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param file <b>{string}</b> Ruta y nombre del archivo a gestionar
        @param user <b>{object}</b> Objeto que contiene los datos del usuario que realiza la acción
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve el resultado de la acción con su correspondiente mensaje
        """
        
        load_file = pyexcel.get_sheet(file_name=file)
        anho_base, errors, result, message = '', '', True, ''
        load_data_msg = str(_("Datos Cargados"))

        ## Se asigna un valor al año base
        anho_base = kwargs['anho_base'] if 'anho_base' in kwargs else ''
        
        for row in load_file.row[2:]:
            try:
                ## Se crea el registro base
                balanza_base, created = BalanzaComercialBase.objects.update_or_create(
                    anho_base=anho_base,
                    anho=row[1],
                    trimestre=row[0],
                    tipo=kwargs['tipo'],
                    dominio=kwargs['dominio'])
                
                ## Se crean las balanzas para precios corrientes (bs) y precios constantes
                if(kwargs['dominio']!='BD' and kwargs['tipo']!='PI'):
                    ## Se crea el registro para Exportaciones de bienes FOB
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="EB", defaults={
                        'publico_petroleo':check_val_data(row[2]),
                        'publico_no_petroleo':check_val_data(row[3]),
                        'privado_petroleo':check_val_data(row[4]),
                        'privado_no_petroleo':check_val_data(row[5]),
                    })
                    
                    ## Se crea el registro para Importaciones de Bienes CIF
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="IB", defaults={
                        'publico_petroleo':check_val_data(row[7]),
                        'publico_no_petroleo':check_val_data(row[8]),
                        'privado_petroleo':check_val_data(row[9]),
                        'privado_no_petroleo':check_val_data(row[10]),
                    })
                    
                    ## Se crea el registro de las exportaciones/importaciones de servicios
                    BalanzaComercialServicios.objects.update_or_create(balanza = balanza_base, defaults={
                        'exportacion_servicio': check_val_data(row[6]),
                        'importacion_servicio': check_val_data(row[11]),
                    })
                ## Se crea la balanza para el índice de precios implícitos
                elif(kwargs['tipo']=='PI'):
                    ## Se crea el registro para los precios implícitos
                    BalanzaComercialPrecioImplicito.objects.update_or_create(balanza = balanza_base, defaults={
                        'importacion_publica':check_val_data(row[11]),
                        'importacion_privada':check_val_data(row[14]),
                        'exportacion_publica':check_val_data(row[3]),
                        'exportacion_privada':check_val_data(row[6]),
                        'importacion_bien':check_val_data(row[10]),
                        'exportacion_bien':check_val_data(row[2]),
                    })
                    
                    ## Se crea el registro para Exportaciones de bienes FOB
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="EB", defaults={
                        'publico_petroleo':check_val_data(row[4]),
                        'publico_no_petroleo':check_val_data(row[5]),
                        'privado_petroleo':check_val_data(row[7]),
                        'privado_no_petroleo':check_val_data(row[8]),
                    })
                    
                    ## Se crea el registro para Importaciones de Bienes CIF
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="IB", defaults={
                        'publico_petroleo':check_val_data(row[12]),
                        'publico_no_petroleo':check_val_data(row[13]),
                        'privado_petroleo':check_val_data(row[15]),
                        'privado_no_petroleo':check_val_data(row[16]),
                    })
                    
                    ## Se crea el registro de las exportaciones/importaciones de servicios
                    BalanzaComercialServicios.objects.update_or_create(balanza = balanza_base, defaults={
                        'exportacion_servicio': check_val_data(row[9]),
                        'importacion_servicio': check_val_data(row[17]),
                    })
                ## Se crea la balanza para precios corrientes (usd)
                else:
                    ## Se crea el registro para Exportaciones de bienes FOB
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="EB", defaults={
                        'publico_petroleo':check_val_data(row[2]),
                        'publico_no_petroleo':check_val_data(row[3]),
                        'privado_petroleo':check_val_data(row[4]),
                        'privado_no_petroleo':check_val_data(row[5]),
                    })
                    ## Se crea el registro para Exportaciones de Servicios
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="ES", defaults={
                        'publico_petroleo':check_val_data(row[6]),
                        'publico_no_petroleo':check_val_data(row[7]),
                        'privado_petroleo':check_val_data(row[8]),
                        'privado_no_petroleo':check_val_data(row[9]),
                    })
                    ## Se crea el registro para Importaciones de Bienes CIF
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="IB", defaults={
                        'publico_petroleo':check_val_data(row[10]),
                        'publico_no_petroleo':check_val_data(row[11]),
                        'privado_petroleo':check_val_data(row[12]),
                        'privado_no_petroleo':check_val_data(row[13]),
                    })
                    ## Se crea el registro para Fletes y Seguros
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="FS", defaults={
                        'publico_petroleo':check_val_data(row[14]),
                        'publico_no_petroleo':check_val_data(row[15]),
                        'privado_petroleo':check_val_data(row[16]),
                        'privado_no_petroleo':check_val_data(row[17]),
                    })
                    ## Se crea el registro para Importaciones de Servicios
                    BalanzaComercialDatos.objects.update_or_create(balanza = balanza_base, tipo="IS", defaults={
                        'publico_petroleo':check_val_data(row[18]),
                        'publico_no_petroleo':check_val_data(row[19]),
                        'privado_petroleo':check_val_data(row[20]),
                        'privado_no_petroleo':check_val_data(row[21]),
                    })
               
            except Exception as e:
                errors += "- %s\n" % str(e)

        if errors:
            message = str(_("Error procesando datos. Verifique su correo para detalles del error"))
            load_data_msg = str(_("Error al procesar datos del área Económica - Externo"))


        # Envia correo electronico al usuario indicando el estatus de la carga de datos
        enviar_correo(user.email, 'gestion.informacion.load.mail', EMAIL_SUBJECT_LOAD_DATA, {
            'load_data_msg': load_data_msg, 'administrador': administrador, 'admin_email': admin_email,
            'errors': errors
        })
        
        return {'result': result, 'message': message}

@python_2_unicode_compatible
class BalanzaComercialDatos(models.Model):
    """!
    Clase que contiene los registros de datos de la Balanza Comercial
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-05-2017
    @version 1.0.0
    """
    
    ## Valor público del petróleo
    publico_petroleo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Pública Petrólera")
    )
    
    ## Valor no público del petróleo
    publico_no_petroleo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Pública No Petrólera")
    )
    
    ## Valor privado del petróleo
    privado_petroleo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Privado Petrólero")
    )
    
    ## Valor no privado del petróleo
    privado_no_petroleo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Privado No Petrólero")
    )
    
    ## Tipo de dato de la balanza
    tipo = models.CharField(max_length=2, choices=BALANZA_DATOS)
    
    ## Relación con la balanza base
    balanza = models.ForeignKey(BalanzaComercialBase)
    
@python_2_unicode_compatible
class BalanzaComercialServicios(models.Model):
    """!
    Clase que contiene los registros de datos de la Balanza Comercial
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-05-2017
    @version 1.0.0
    """
    
    ## Valor de importacion del servicio
    exportacion_servicio = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Exportaciones de Servicios")
    )
    
    ## Valor de exportación del servicio
    importacion_servicio = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Importaciones de Servicios")
    )
    
    ## Relación con la balanza base
    balanza = models.ForeignKey(BalanzaComercialBase)
    
@python_2_unicode_compatible
class BalanzaComercialPrecioImplicito(models.Model):
    """!
    Clase que contiene los registros de datos de Precios Implicitos de la Balanza Comercial
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 03-05-2017
    @version 1.0.0
    """
    ## Valor público de la importación
    importacion_publica = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Importaciones Públicas")
    )
    
    ## Valor privado de la importación
    importacion_privada = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Importaciones Privadas")
    )
    
    ## Valor público de la exportación
    exportacion_publica = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Exportaciones Públicas")
    )
    
    ## Valor privado de la exportación
    exportacion_privada = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Exportaciones Privadas")
    )
    
    ## Valor de importación de los bienes
    importacion_bien = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Importaciones de Bienes CIF")
    )
    
    ## Valor de exportación de los bienes
    exportacion_bien = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Exportaciones de Bienes FOB")
    )
    
    ## Relación con la balanza base
    balanza = models.ForeignKey(BalanzaComercialBase)
    
# ------------ Económico Externo - Cuenta Capital  --------------------
# ---------------------  Balanza de Pagos  ----------------------------
@python_2_unicode_compatible
class CuentaCapitalBalanzaBase(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital, en la parte de balanza de pagos
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """
    ## Año al que pertenece el(los) registro(s)
    anho = models.CharField(max_length=4, verbose_name=_("Año"))

    ## Trimestre del registro
    trimestre = models.CharField(max_length=2, choices=TRIMESTRES[1:], verbose_name=_("Trimestre"))
    
    class Meta:
        unique_together = ("anho", "trimestre")
        
    def gestion_init(self, *args, **kwargs):
        """!
        Método que permite descargar un archivo con los datos a gestionar

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 08-05-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{tupla}</b> Tupla con argumentos opcionales
        @param kwargs <b>{dic}</b> Diccionario con filtros opcionales
        @return Devuelve los datos a incluír en el archivo
        """
        nombre_archivo = 'cuenta_capital'
        fields = []
        header = []
        sub_header = []
        
        ## Cabecera para balanza de pagos
        if(kwargs['dominio']=='BP'):
            nombre_archivo += "_balanza_pagos"
            head = [
                {'tag': '', 'cabecera': True},
                {'tag': '', 'cabecera': True},
                {'tag': str(_("Cuenta Corriente")), 'color': 'ocean_blue', 'text_color': 'white', 'combine': 11, 'cabecera': True},
                {'tag': str(_("Cuenta Capital y Financiera")), 'color': 'aqua', 'text_color': 'white', 'combine': 27, 'cabecera': True},
                {'tag': '', 'cabecera': True},
            ]
            header = [
                {'tag': '', 'cabecera': True},
                {'tag': '', 'cabecera': True},
                {'tag': str(_("Saldo de Servicios")), 'color': 'sky_blue', 'text_color': 'white', 'combine': 6, 'cabecera': True},
                {'tag': str(_("Saldo en Renta")), 'color': 'coral', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': '', 'cabecera': True,'color': 'white'},
                {'tag': str(_("Cuenta Capital")), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_("Cuenta Financiera")), 'color': 'ice_blue', 'text_color': 'white', 'combine': 26, 'cabecera': True},
                {'tag': '', 'color': 'orange', 'cabecera': True},
            ]
            ## Se añade la cabecera
            fields.append(head)
            fields.append(header)
            sub_header = [
                {'tag': str(_("Trimestre")), 'color': 'white', 'text_color': 'black','cabecera': True},
                {'tag': str(_("Año")), 'color': 'white', 'text_color': 'black', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('transporte').verbose_name)), 'color': 'sky_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('viajes').verbose_name)), 'color': 'sky_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('comunicacion').verbose_name)), 'color': 'sky_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('seguro').verbose_name)), 'color': 'sky_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('gobierno').verbose_name)), 'color': 'sky_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('otros').verbose_name)), 'color': 'sky_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('remuneracion_empleado').verbose_name)), 'color': 'coral', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('inversion_directa').verbose_name)), 'color': 'coral', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('inversion_cartera').verbose_name)), 'color': 'coral', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalSaldos._meta.get_field('otra_inversion').verbose_name)), 'color': 'coral', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalOtros._meta.get_field('transferencia_corriente').verbose_name)), 'color': 'white', 'text_color': 'black', 'cabecera': True},
                {'tag': str(_(CuentaCapitalOtros._meta.get_field('cuenta_capital').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': "ID_"+str(_(CuentaCapitalInversionDirecta._meta.get_field('extranjero').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "ID_"+str(_(CuentaCapitalInversionDirecta._meta.get_field('pais').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "IC_A_Spu"+str(_(CuentaCapitalInversionCartera._meta.get_field('titulo_participacion_capital').verbose_name)), 'color': 'ice_blue','text_color': 'white', 'cabecera': True},
                {'tag': "IC_A_Spu"+str(_(CuentaCapitalInversionCartera._meta.get_field('titulo_deuda').verbose_name)), 'color': 'ice_blue','text_color': 'white', 'cabecera': True},
                {'tag': "IC_A_Spr"+str(_(CuentaCapitalInversionCartera._meta.get_field('titulo_participacion_capital').verbose_name)), 'color': 'ice_blue','text_color': 'white', 'cabecera': True},
                {'tag': "IC_A_Spr"+str(_(CuentaCapitalInversionCartera._meta.get_field('titulo_deuda').verbose_name)), 'color': 'ice_blue','text_color': 'white', 'cabecera': True},
                {'tag': "IC_P_Spu"+str(_(CuentaCapitalInversionCartera._meta.get_field('titulo_participacion_capital').verbose_name)), 'color': 'ice_blue','text_color': 'white', 'cabecera': True},
                {'tag': "IC_P_Spu"+str(_(CuentaCapitalInversionCartera._meta.get_field('titulo_deuda').verbose_name)), 'color': 'ice_blue','text_color': 'white', 'cabecera': True},
                {'tag': "IC_P_Spr"+str(_(CuentaCapitalInversionCartera._meta.get_field('titulo_participacion_capital').verbose_name)), 'color': 'ice_blue','text_color': 'white', 'cabecera': True},
                {'tag': "IC_P_Spr"+str(_(CuentaCapitalInversionCartera._meta.get_field('titulo_deuda').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_A_Spu"+str(_(CuentaCapitalOtraInversion._meta.get_field('credito_comercial').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_A_Spu"+str(_(CuentaCapitalOtraInversion._meta.get_field('prestamo').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_A_Spu"+str(_(CuentaCapitalOtraInversion._meta.get_field('moneda_deposito').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_A_Spu"+str(_(CuentaCapitalOtraInversion._meta.get_field('otros').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_A_Spr"+str(_(CuentaCapitalOtraInversion._meta.get_field('credito_comercial').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_A_Spr"+str(_(CuentaCapitalOtraInversion._meta.get_field('prestamo').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_A_Spr"+str(_(CuentaCapitalOtraInversion._meta.get_field('moneda_deposito').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_A_Spr"+str(_(CuentaCapitalOtraInversion._meta.get_field('otros').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_P_Spu"+str(_(CuentaCapitalOtraInversion._meta.get_field('credito_comercial').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_P_Spu"+str(_(CuentaCapitalOtraInversion._meta.get_field('prestamo').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_P_Spu"+str(_(CuentaCapitalOtraInversion._meta.get_field('moneda_deposito').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_P_Spu"+str(_(CuentaCapitalOtraInversion._meta.get_field('otros').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_P_Spr"+str(_(CuentaCapitalOtraInversion._meta.get_field('credito_comercial').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_P_Spr"+str(_(CuentaCapitalOtraInversion._meta.get_field('prestamo').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_P_Spr"+str(_(CuentaCapitalOtraInversion._meta.get_field('moneda_deposito').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': "OI_P_Spr"+str(_(CuentaCapitalOtraInversion._meta.get_field('otros').verbose_name)), 'color': 'ice_blue', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalOtros._meta.get_field('errores_omisiones').verbose_name)), 'color': 'orange', 'text_color': 'white', 'cabecera': True},
            ]
            ## Se añade la subcabecera
            fields.append(sub_header)
        ## Cabecera para deudas
        elif(kwargs['dominio']=='DE'):
            nombre_archivo += "_deudas"
            head = [
                {'tag': '', 'cabecera': True},
                {'tag': '', 'cabecera': True},
                {'tag': str(_("Sector Público")), 'color': 'ocean_blue', 'text_color': 'white', 'combine': 9, 'cabecera': True},
                {'tag': str(_("Sector Privado")), 'color': 'aqua', 'text_color': 'white', 'combine': 9, 'cabecera': True},
            ]
            header = [
                {'tag': '', 'cabecera': True},
                {'tag': '', 'cabecera': True},
                {'tag': str(_("Capital")), 'color': 'green', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': str(_("Intereses")), 'color': 'indigo', 'text_color': 'white', 'combine': 5, 'cabecera': True},
                {'tag': str(_("Capital")), 'color': 'green', 'text_color': 'white', 'combine': 4, 'cabecera': True},
                {'tag': str(_("Intereses")), 'color': 'indigo', 'text_color': 'white', 'combine': 5, 'cabecera': True},
            ]
            ## Se añade la cabecera
            fields.append(head)
            fields.append(header)
            sub_header = [
                {'tag': str(_("Trimestre")), 'color': 'white', 'text_color': 'black','cabecera': True},
                {'tag': str(_("Año")), 'color': 'white', 'text_color': 'black', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaCapital._meta.get_field('bono_pagare').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaCapital._meta.get_field('credito_comercial').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaCapital._meta.get_field('prestamo').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaCapital._meta.get_field('otros').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('bono_pagare').verbose_name)), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('instrumento_mercado').verbose_name)), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('credito_comercial').verbose_name)), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('prestamo').verbose_name)), 'color': 'indigo', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('otros').verbose_name)), 'color': 'indigo', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaCapital._meta.get_field('bono_pagare').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaCapital._meta.get_field('credito_comercial').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaCapital._meta.get_field('prestamo').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaCapital._meta.get_field('otros').verbose_name)), 'color': 'green', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('bono_pagare').verbose_name)), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('instrumento_mercado').verbose_name)), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('credito_comercial').verbose_name)), 'color': 'indigo', 'text_color': 'white', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('prestamo').verbose_name)), 'color': 'indigo', 'cabecera': True},
                {'tag': str(_(CuentaCapitalDeudaIntereses._meta.get_field('otros').verbose_name)), 'color': 'indigo', 'cabecera': True},
            ]
            ## Se añade la subcabecera
            fields.append(sub_header)
        
        # Almacena los datos de año y trimestre inicial provenientes del formulario
        anho_ini = int(kwargs['anho__gte'])
        trimestre_ini = int(kwargs['trimestre__gte'])
        
        while True:
            registros = [({'tag': anho_ini})]
            registros.append({'tag': trimestre_ini})
            # Agrega los datos a la nueva fila del archivo a generar
            fields.append(registros)
            if (anho_ini == int(kwargs['anho__lte']) and trimestre_ini == int(kwargs['trimestre__lte'])):
                break
            if (trimestre_ini == 4):
                trimestre_ini = 0
                anho_ini += 1
            trimestre_ini += 1
        
        return {'fields': fields, 'output': nombre_archivo}
        
@python_2_unicode_compatible
class CuentaCapitalSaldos(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital, en la parte de balanza de pagos (saldos)
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """
    ## --------------> Saldo de Servicios
    
    ## Valor del transporte
    transporte = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Transportes")
    )
    
    ## Valor de los viajes
    viajes = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Viajes")
    )
    
    ## Valor de la comunicación
    comunicacion = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Comunicaciones")
    )
    
    ## Valor del seguro
    seguro = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Seguros")
    )
    
    ## Valor del gobierno
    gobierno = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Gobierno n.i.o.p.")
    )
    
    ## Otros valores
    otros = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Otros")
    )
    
    ## --------------> Saldo en Renta
    
    ## Valor de la remuneración del empleado
    remuneracion_empleado = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Remuneración Empleados")
    )
    
    ## Valor de la inversión directa
    inversion_directa = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Inversión Directa")
    )
    
    ## Valor de la inversión de cartera
    inversion_cartera = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Inversión de Cartera")
    )
    
    ## Valor de otras inversiones
    otra_inversion = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Otra Inversión")
    )
    
    ## Relación con el registro base de la cuenta capital
    cuenta_capital = models.ForeignKey(CuentaCapitalBalanzaBase)
    
@python_2_unicode_compatible
class CuentaCapitalOtros(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital, en la parte de balanza de pagos (otros)
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """   
    ## Valor de la transferencias corrientes
    transferencia_corriente = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Transferencias Corrientes")
    )
    
    ## Valor de la cuenta capital
    cuenta = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Cuenta Capital")
    )
    
    ## Valor de los errores u omisiones
    errores_omisiones = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Errores y Omisiones")
    ) 
    
    ## Relación con el registro base de la cuenta capital
    cuenta_capital = models.ForeignKey(CuentaCapitalBalanzaBase)
    
@python_2_unicode_compatible
class CuentaCapitalInversionCartera(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital, en la parte de balanza de pagos (inversión cartera)
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """   
    ## Valor del título de participacion capital
    titulo_participacion_capital = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Títulos de participación en el capital")
    )
    
    ## Valor del título de la deuda
    titulo_deuda = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Títulos de deuda")
    )
    
    ## Tipo de dato de la inversión de cartera
    tipo = models.CharField(max_length=2, choices=INVERSION_CARTERA)
       
    ## Relación con el registro base de la cuenta capital
    cuenta_capital = models.ForeignKey(CuentaCapitalBalanzaBase)
    
@python_2_unicode_compatible
class CuentaCapitalInversionDirecta(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital, en la parte de balanza de pagos (inversión directa)
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """   
    ## Valor de la inversión directa en el extranjero
    extranjero = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Extranjero")
    )
    
    ## Valor de la inversión directa en el país
    pais = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("País")
    )
       
    ## Relación con el registro base de la cuenta capital
    cuenta_capital = models.ForeignKey(CuentaCapitalBalanzaBase)
    
@python_2_unicode_compatible
class CuentaCapitalOtraInversion(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital, en la parte de balanza de pagos (otras inversiones)
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """   
    ## Valor del crédito comercial
    credito_comercial = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Créditos Comerciales")
    )
    
    ## Valores del préstamo
    prestamo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Préstamos")
    )
    
    ## Valores de monedas y depósitos
    moneda_deposito = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Monedas y depósitos")
    )
    
    ## Otros valores
    otros = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Otros")
    )
    
    ## Tipo de dato de la inversión de cartera
    tipo = models.CharField(max_length=2, choices=INVERSION_CARTERA)
       
    ## Relación con el registro base de la cuenta capital
    cuenta_capital = models.ForeignKey(CuentaCapitalBalanzaBase)
    
    
# ---------------------  Deudas  ----------------------------
@python_2_unicode_compatible
class CuentaCapitalDeudaBase(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital, en la parte de deudas
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """
    ## Año al que pertenece el(los) registro(s)
    anho = models.CharField(max_length=4, verbose_name=_("Año"))

    ## Trimestre del registro
    trimestre = models.CharField(max_length=2, choices=TRIMESTRES[1:], verbose_name=_("Trimestre"))
    
    class Meta:
        unique_together = ("anho", "trimestre")
        
@python_2_unicode_compatible
class CuentaCapitalDeudaCapital(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital Deuda, en la parte de deudas (capital)
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """   
    ## Valor de los bonos y pagarés
    bono_pagare = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Bonos y Pagarés")
    )
    
    ## Valores de los cŕeditos comerciales
    credito_comercial = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Créditos Comerciales")
    )
    
    ## Valores del préstamo
    prestamo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Préstamos")
    )
    
    ## Otros valores
    otros = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Otros")
    )
    
    ## Tipo de dato de la deuda
    tipo = models.CharField(max_length=2, choices=SECTOR_DEUDA)
       
    ## Relación con el registro base de la cuenta capital (deuda)
    deuda = models.ForeignKey(CuentaCapitalDeudaBase)
    
    
@python_2_unicode_compatible
class CuentaCapitalDeudaIntereses(models.Model):
    """!
    Clase que contiene los registros base de la Cuenta Capital Deuda, en la parte de deudas (intereses)
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-05-2017
    @version 1.0.0
    """   
    ## Valor de los bonos y pagarés
    bono_pagare = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Bonos y Pagarés")
    )
    
    ## Valores del instrumento del mercado monetario
    instrumento_mercado = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Instrumentos del Mercado Monetario")
    )
    
    ## Valores de los cŕeditos comerciales
    credito_comercial = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Créditos Comerciales")
    )
    
    ## Valores del préstamo
    prestamo = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Préstamos")
    )
    
    ## Otros valores
    otros = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.0, verbose_name=_("Otros")
    )
    
    ## Tipo de dato de la deuda
    tipo = models.CharField(max_length=2, choices=SECTOR_DEUDA)
       
    ## Relación con el registro base de la cuenta capital (deuda)
    deuda = models.ForeignKey(CuentaCapitalDeudaBase)