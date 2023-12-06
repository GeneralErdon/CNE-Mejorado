import uuid
import datetime as dt

from django.db.models import QuerySet
from apps.base.types import TVotosTotalizados
from apps.candidatos.models import Candidato

from apps.elecciones.models import Eleccion, Elecciones_Candidato, Voto


class VotosManager:
    def get_queryset(self):
        return Voto.objects.all()
    
    def totalizar_votos(self, elecciones:Eleccion) -> TVotosTotalizados:
        candidatos:QuerySet[Candidato] = elecciones.candidatos.all()
        
        result:TVotosTotalizados = {
            "nulos_totales":elecciones.voto_set.filter(tipo="N").count(),
        }
        
        for candidato in candidatos:
            eleccion_candidato:Elecciones_Candidato = candidato.elecciones_candidato_set.filter(eleccion__pk=elecciones.pk).first()
            votos_candidato:QuerySet[Voto] = elecciones.voto_set.filter(candidato__pk=candidato.pk)
            
            result["candidatos"][candidato.identification]["candidato"] = candidato.__str__()
            result["candidatos"][candidato.identification]["cargo"] = eleccion_candidato.cargo.description
            result["candidatos"][candidato.identification]["votos"] = { 
                                            "total_absoluto": votos_candidato.count(),
                                            "total_acciones": sum(votos_candidato.values_list("acciones", flat=True))
                                        }
        
        
        return result

class EleccionesManager:
    
    def get_queryset(self):
        return Eleccion.objects.all()
    
    def get_proximas_elecciones(self):
        """Función que trae las proximas elecciones, basado en cuya fecha de inicio 
        esté próxima

        Returns:
            Queryset: Queryset de Elecciones
        """
        today_dt = dt.datetime.now()
        return self.get_queryset().filter(fecha_inicio__date__gte=today_dt.date())
    
    def get_actual_election(self) -> QuerySet[Eleccion]:
        """retorna un queryset con las Elecciones que se estén celebrando actualmente
        
        returns:
            Queryset[Eleccion]: Elecciones
        """
        today_dt = dt.datetime.now()
        return self.get_queryset().filter(fecha_inicio__lte=today_dt, fecha_final__gte=today_dt)
    
    def is_today_election(self) -> bool:
        """Funcion que debe decirme si el dia de hoy es dia de elecciones.
        basado en la fecha inicio y fecha final de cualquier registro de elecciones

        Returns:
            bool: True si actualmente hay elecciones activas, False si no
        """
        
        # Si la fecha de inicio es Menor y la fecha final es Mayor al Ahora
        return self.get_actual_election().exists()
        