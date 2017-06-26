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
from __future__ import absolute_import, unicode_literals

from datetime import datetime

import sys
from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from base.constant import EMAIL_SUBJECT_CM_RESULT
from base.functions import enviar_correo
from seiven.celery import app

import logging
import json

logger = logging.getLogger("carga_masiva")


@app.task
def cargar_datos_masivos(app, mod, user, file_content,**kwargs):
    instance = apps.get_model(app, mod)
    modelo = instance()
    
    resultado = modelo.gestion_process(user=user, file_content=file_content,**kwargs)