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

    class Meta:
        unique_together = ("anho", "mes")

    def gestion_init(self, *args, **kwargs): #ciudad=None, anho_base=None, mes_ini=None, mes_fin=None, anho_ini=None, anho_fin=None

        grupo_label = str(PreciosGrupo._meta.verbose_name)
        grupo_count_fields = PreciosGrupo._meta.get_fields()[:-4].__len__()
        sector_label = str(PreciosSector._meta.verbose_name)
        sector_count_fields = PreciosSector._meta.get_fields()[:-4].__len__()
        naturaleza_label = str(PreciosNaturaleza._meta.verbose_name)
        naturaleza_count_fields = PreciosNaturaleza._meta.get_fields()[:-4].__len__()
        servicios_label = str(PreciosServicios._meta.verbose_name)
        servicios_count_fields = PreciosServicios._meta.get_fields()[:-4].__len__()
        inflacionario_label = str(PreciosInflacionario._meta.verbose_name)
        inflacionario_count_fields = PreciosInflacionario._meta.get_fields()[:-4].__len__()
        productos_label = str(PreciosProductos._meta.verbose_name)
        productos_count_fields = PreciosProductos._meta.get_fields()[:-4].__len__()
        fields = [
            [
                {'tag': '', 'color': '', 'text_color': '', 'combine': 0},
                {'tag': '', 'color': '', 'text_color': '', 'combine': 0},
                {'tag': '', 'color': '', 'text_color': '', 'combine': 0},
                {'tag': grupo_label, 'color': 'indigo', 'text_color': 'white', 'combine': grupo_count_fields},
                {'tag': sector_label, 'color': 'orange', 'text_color': 'white', 'combine': sector_count_fields},
                {'tag': naturaleza_label, 'color': 'gray25', 'text_color': 'black', 'combine': naturaleza_count_fields},
                {'tag': servicios_label, 'color': 'green', 'text_color': 'white', 'combine': servicios_count_fields},
                {'tag': inflacionario_label, 'color': 'red', 'text_color': 'white', 'combine': inflacionario_count_fields},
                {'tag': productos_label, 'color': 'aqua', 'text_color': 'black', 'combine': productos_count_fields},
            ],
            []
        ]
        relations, data, exclude_fields = [], [], ['id', 'anho_base', 'real_precios_id', 'base']

        if not 'dominio' in kwargs or not kwargs['dominio'] == 'C':
            exclude_fields.append('ciudad')

        for f in self._meta.get_fields():
            try:
                field, label, null = f.attname, str(f.verbose_name), f.null
                if not field in exclude_fields and not f.get_internal_type() == "ManyToOneRel":
                    type, validators, error_messages = f.get_internal_type(), f.validators, f.error_messages

                    if type == "ForeignKey":
                        relations.append(f.rel.to)

                    fields[1].append({
                        'field': field, 'label': label, 'type': type, 'null': null, 'validators': validators,
                        'error_messages': error_messages
                    })
            except Exception as e:
                pass

        ## Extrae los campos del modelo de precios por grupo
        for grupo in PreciosGrupo._meta.get_fields():
            if not grupo.attname in exclude_fields:
                fields[1].append({
                    'field': grupo.attname, 'label': str(grupo.verbose_name), 'type': grupo.get_internal_type(),
                    'null': grupo.null, 'validators': grupo.validators, 'error_messages': grupo.error_messages
                })

        ## Extrae los campos del modelo de precios por sector
        for sector in PreciosSector._meta.get_fields():
            if not sector.attname in exclude_fields:
                fields[1].append({
                    'field': sector.attname, 'label': str(sector.verbose_name), 'type': sector.get_internal_type(),
                    'null': sector.null, 'validators': sector.validators, 'error_messages': sector.error_messages
                })

        ## Extrae los campos del modelo de precios por naturaleza
        for naturaleza in PreciosNaturaleza._meta.get_fields():
            if not naturaleza.attname in exclude_fields:
                fields[1].append({
                    'field': naturaleza.attname, 'label': str(naturaleza.verbose_name), 'type': naturaleza.get_internal_type(),
                    'null': naturaleza.null, 'validators': naturaleza.validators, 'error_messages': naturaleza.error_messages
                })

        ## Extrae los campos del modelo de precios por servicios
        for servicios in PreciosServicios._meta.get_fields():
            if not servicios.attname in exclude_fields:
                fields[1].append({
                    'field': servicios.attname, 'label': str(servicios.verbose_name), 'type': servicios.get_internal_type(),
                    'null': servicios.null, 'validators': servicios.validators, 'error_messages': servicios.error_messages
                })

        ## Extrae los campos del modelo de precios por núcleo inflacionario
        for inflacionario in PreciosInflacionario._meta.get_fields():
            if not inflacionario.attname in exclude_fields:
                fields[1].append({
                    'field': inflacionario.attname, 'label': str(inflacionario.verbose_name), 'type': inflacionario.get_internal_type(),
                    'null': inflacionario.null, 'validators': inflacionario.validators, 'error_messages': inflacionario.error_messages
                })

        ## Extrae los campos del modelo de precios por productos controlados y no controlados
        for productos in PreciosProductos._meta.get_fields():
            if not productos.attname in exclude_fields:
                fields[1].append({
                    'field': productos.attname, 'label': str(productos.verbose_name), 'type': productos.get_internal_type(),
                    'null': productos.null, 'validators': productos.validators, 'error_messages': productos.error_messages
                })

        ## Estrae los registros asociados a descargar en archivo
        for p in Precios.objects.filter(**kwargs):
            registros = [p.anho, p.mes, p.inpc]
            #registros.append()
            data.append(registros)

        return {'cabecera': fields, 'relations': relations, 'data': data, 'output': 'precios'}

    def gestion_process(self, file, user, *args, **kwargs):
        load_file = pyexcel.get_sheet(file_name=file)
        anho_base, i, col_ini, errors, result, message = '', 0, 2, '', True, ''
        load_data_msg = str(_("Datos Cargados"))

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
                inpc = row[3] if self.ciudad else row[2]

                # Condición que indica si el registro corresponde al año base
                base = True if i == 0 else False

                # Gestión para los datos básicos de precios
                real_p, created = Precios.objects.update_or_create(anho=anho, mes=mes, ciudad=ciudad, defaults={
                    'anho_base': anho_b, 'inpc': inpc
                })


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
                errors = errors + "<li>%s</li>" % str(e)

            i += 1

        if errors:
            message = str(_("Error procesando datos. Verifique su correo para detalles del error"))
            load_data_msg = str(_("Error al procesar datos"))


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