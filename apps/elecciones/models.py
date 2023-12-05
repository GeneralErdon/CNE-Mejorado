from django.db import models

from apps.base.models import BaseModel
from apps.candidatos.models import Candidato, Cargo

# Create your models here.

class Eleccion(BaseModel):
    
    description = models.CharField(
        verbose_name="Descripción",
        help_text="Motivo o descripción de estas elecciones",
        max_length=200,
    )
    
    fecha_inicio = models.DateTimeField(
        verbose_name="Fecha y hora de inicio",
        help_text="Fecha y hora a la cual dará inicio el conteo de votos.",
    )
    
    fecha_final = models.DateTimeField(
        verbose_name="Fecha y hora de finalización",
        help_text="Fecha y hora que dará finalizado el conteo de votos."
    )
    
    observation = models.TextField(
        verbose_name="Observaciones",
        help_text="Indique alguna observación o notas acerca de estas elecciones",
        null=True, blank=True,
    )
    
    candidatos = models.ManyToManyField(
        Candidato,
        through="Elecciones_Candidato",
        help_text="Participantes como candidatos.",
        verbose_name="Candidatos",
    )
    
    def __str__(self) -> str:
        return self.description
    
    class Meta:
        verbose_name = 'Eleccion'
        verbose_name_plural = 'Elecciones'


class Elecciones_Candidato(BaseModel):
    eleccion = models.ForeignKey(
        to=Eleccion,
        verbose_name="Voto en esta Elección",
        help_text="Este voto está registrado en estas elecciones",
        on_delete=models.RESTRICT,
    )
    candidato = models.ForeignKey(
        to=Candidato,
        verbose_name="Candidato votado",
        help_text="Este voto es para este candidato, si no hay candidato, es voto nulo",
        on_delete=models.RESTRICT
    )
    
    cargo = models.ForeignKey(
        to=Cargo,
        verbose_name="Cargo",
        help_text="Cargo que desempeñará el candidato en las elecciones",
        on_delete=models.RESTRICT
    )
    


TIPOS_VOTOS = (
    ("N", "Voto nulo"),
    ("V", "Voto normal"),
)
class Voto(BaseModel):
    eleccion = models.ForeignKey(
        to=Eleccion,
        verbose_name="Voto en esta Elección",
        help_text="Este voto está registrado en estas elecciones",
        on_delete=models.RESTRICT,
    )
    candidato = models.ForeignKey(
        to=Candidato,
        verbose_name="Candidato votado",
        help_text="Este voto es para este candidato, si no hay candidato, es voto nulo",
        null=True, blank=True,
        on_delete=models.RESTRICT
    )
    
    acciones = models.BigIntegerField(
        verbose_name="Acciones del voto",
        help_text="El votante contaba con esta cantidad de acciones",
    )
    
    tipo = models.CharField(
        max_length=1,
        choices=TIPOS_VOTOS,
        verbose_name="Tipo de voto",
        help_text="Indica si el voto es Normal o es voto Nulo",
    )
    
    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
    
    def __str__(self):
        return f"voto de {self.acciones} acciones"