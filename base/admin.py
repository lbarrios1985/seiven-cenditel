from __future__ import unicode_literals

from django.contrib import admin

from .models import Institucion, AnhoBase

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class InstitucionAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'descripcion')
	list_filter = ('nombre', 'descripcion')
	ordering = ('nombre',)
	search_fields = ('nombre', 'descripcion')

admin.site.register(Institucion, InstitucionAdmin)

class AnhoBaseAdmin(admin.ModelAdmin):
    """!
    Clase que gestiona los años base en el panel administrativo

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-07-2017
    @version 1.0.0
    """
    list_display = ('anho',)
    list_filter = ('anho',)
    ordering = ('anho',)
    search_fields = ('anho',)

## Registra el modelo Anho en el panel administrativo
admin.site.register(AnhoBase, AnhoBaseAdmin)
