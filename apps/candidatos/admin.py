from django.contrib import admin

from apps.candidatos.models import Candidato

# Register your models here.


@admin.register(Candidato)
class CustomCandidatoAdmin(admin.ModelAdmin):
    list_per_page = 30
    search_fields = [
        "identification",
        "name",
        "last_name",
        
    ]
    
    readonly_fields = (
        "id",
        "changed_by",
    )