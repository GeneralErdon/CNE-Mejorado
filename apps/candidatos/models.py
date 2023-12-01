from django.db import models
from datetime import datetime as dt

from apps.base.models import PersonModel

# Create your models here.

def candidato_image_path(instance, filename):
    
    identify:str = f"{instance.__str__()}-{instance.identification}"
    year = dt.today().year
    return f"Candidato_img/{year}/{identify}/{filename}"

class Candidato(PersonModel):
    
    photo = models.ImageField(
        verbose_name="Foto del candidato",
        help_text="Foto del candidato",
        null=True, blank=True,
        upload_to=candidato_image_path,
        
    )
    
    
    def __str__(self) -> str:
        return f"{self.last_name}, {self.name}"
    
    def clean(self) -> None:
        self.name = self.name.upper()
        self.last_name = self.last_name.upper()
        return super().clean()
    class Meta:
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'