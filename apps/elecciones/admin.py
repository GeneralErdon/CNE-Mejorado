from django.contrib import admin

from apps.elecciones.models import Eleccion, Elecciones_Candidato

# Register your models here.

class Candidatos_Eleccion_Inline(admin.TabularInline):
    model = Elecciones_Candidato
    extra = 2
    fields = (
        "candidato",
        "cargo",
        
    )


@admin.register(Eleccion)
class EleccionAdmin(admin.ModelAdmin):
    
    
    inlines = (Candidatos_Eleccion_Inline, )
    list_per_page = 30
    readonly_fields = (
        "id",
        "status",
        "changed_by",
    )