import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(
        verbose_name="ID",
        help_text="Identificador del registro",
        primary_key=True,
        db_index=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

