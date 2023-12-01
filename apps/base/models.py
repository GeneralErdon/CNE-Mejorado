from typing import Any
import uuid
from django.db import models
from datetime import datetime as dt
from simple_history.models import HistoricalRecords

SEX_CHOICES = (
    ("M", "Masculino"),
    ("F", "Femenino"),
)


# Create your models here.
class BaseModel(models.Model):
    
    id = models.UUIDField(
        verbose_name="ID",
        help_text="Identificador del registro",
        primary_key=True,
        db_index=True,
        unique=True,
        default=uuid.uuid4,
    )
    
    status = models.BooleanField(
        verbose_name="Estado",
        help_text="Activo✅ / Inactivo ❌ ",
        default=True,
        db_index=True,
    )
    changed_by = models.ForeignKey(
        'auth.User', on_delete=models.RESTRICT,
        verbose_name="Modificado por", 
        help_text="Último usuario en alterar el registro",
        )
    
    created_date = models.DateTimeField(
        verbose_name="Fecha creación",
        help_text="Fecha en la cuál se creó el registro",
        auto_now=False, auto_now_add=True,
        db_index=True,
    )
    modified_date = models.DateTimeField(
        verbose_name="Fecha de modificación",
        help_text="Fecha de última modificación del registro",
        auto_now=True, auto_now_add=False,
    )
    deleted_date = models.DateTimeField(
        verbose_name="Fecha de eliminación",
        help_text="Fecha de desactivación del registro.",
        auto_now=True, auto_now_add=False,
    )
    
    # Simple History config
    history = HistoricalRecords(inherit=True,)
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
    
    
    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        
        self.status = False
        self.deleted_date = dt.now(tz=None)
        self.save()
    
    class Meta:
        abstract = True
        verbose_name = 'BaseModel'
        verbose_name_plural = 'BaseModels'



class PersonModel(BaseModel):
    
    identification = models.CharField(
        verbose_name="Cédula o Pasaporte",
        help_text="Número de documento de identificación",
        unique=True,
        db_index=True,
        max_length=11
    )
    
    name = models.CharField(
        verbose_name="Nombres",
        help_text="Nombre y segundo nombre",
        max_length=252,
    )
    
    last_name = models.CharField(
        verbose_name="Apellidos",
        help_text="Apellido y segundo apellido",
        max_length=252,
    )
    
    sex = models.CharField(
        verbose_name="Sexo",
        help_text="Masculino o Femenino",
        db_index=True,
        choices=SEX_CHOICES,
        default="M",
    )
    
    class Meta:
        abstract = True
        verbose_name = 'PersonBaseModel'
        verbose_name_plural = 'PersonBaseModels'