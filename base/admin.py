from __future__ import unicode_literals

from django.contrib import admin

from .models import Institucion

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

class InstitucionAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'descripcion')
	list_filter = ('nombre', 'descripcion')
	ordering = ('nombre',)
	search_fields = ('nombre', 'descripcion')

admin.site.register(Institucion, InstitucionAdmin)
