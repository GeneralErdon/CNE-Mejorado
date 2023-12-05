

from typing import TypedDict


class TVotosCount(TypedDict):
    total_absoluto: int
    total_acciones: int

class TVotosCandidato(TypedDict):
    candidato: str
    cargo:str
    votos: TVotosCount

class TVotosTotalizados(TypedDict):
    nulos_totales: TVotosCount
    candidatos: dict[str, TVotosCandidato]