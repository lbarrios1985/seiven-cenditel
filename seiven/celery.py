"""
Sistema Estadístico Integral de Venezuela - (SEIVEN)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://mpv.cenditel.gob.ve/seiven
"""
## @package seiven.celery
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para los modelos del área económica
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

## Configuración de la variable de entorno para el uso del módulo de configuración de la aplicación
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seiven.settings')

## Aplicación para el uso de Celery
app = Celery('CargaMasiva')

## Inicialización de la aplicación de celery con la configuración del proyecto
app.config_from_object('django.conf:settings')

## Inspección sobre todas las aplicaciones del sistema en búsca de los métodos de celery '@task' para la ejecución de
# tareas
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    BROKER_URL='django://',
)
