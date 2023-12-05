

from typing import Literal, TypedDict

from apps.candidatos.models import Candidato
from apps.elecciones.models import Eleccion


class TVotoData(TypedDict):
    candidato: Candidato | None
    eleccion: Eleccion
    acciones: int
    tipo: Literal["N"] | Literal["V"] # Nulo o válido

class TVotoSerializerData(TypedDict):
    elecciones:Eleccion
    votos:list[TVotoData]