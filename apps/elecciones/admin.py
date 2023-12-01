from django.contrib import admin

from apps.elecciones.models import Eleccion

# Register your models here.

@admin.register(Eleccion)
class EleccionAdmin(admin.ModelAdmin):
    
    list_per_page = 30
    readonly_fields = (
        "id",
        "status",
        "changed_by",
    )