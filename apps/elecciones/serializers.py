from rest_framework import serializers
from django.db.models import QuerySet

from apps.base.serializers import BaseReadOnlySerializer
from apps.base.utils import EleccionesManager
from apps.candidatos.serializers import CandidatoReadOnlySerializer

from apps.elecciones.models import Eleccion, Elecciones_Candidato, Voto
from apps.elecciones.types import TVotoData, TVotoSerializerData

class EleccionReadOnlySerializer(BaseReadOnlySerializer):
    fecha_inicio = serializers.DateTimeField(format="%d-%m-%Y %H:%M:S", read_only=True)
    fecha_final = serializers.DateTimeField(format="%d-%m-%Y %H:%M:S", read_only=True)
    candidatos = serializers.SerializerMethodField("get_candidatos")
    
    class Meta:
        model = Eleccion
        fields = "__all__"
    
    def get_candidatos(self, obj:Eleccion):
        
        return CandidatoReadOnlySerializer(
            instance=obj.candidatos, many=True
            ).data


class VotarModelSerializer(BaseReadOnlySerializer):
    class Meta:
        model = Voto
        fields = "__all__"
        read_only_fields = ("created_date","modified_date", "deleted_date", "changed_by")
    
    def validate(self, attrs:TVotoData) -> dict:
        tipo = attrs["tipo"]
        candidato = attrs.get("candidato", None)
        eleccion:Eleccion = attrs["eleccion"]
        e_manager = EleccionesManager()
        
        if attrs["acciones"] < 0:
            raise serializers.ValidationError({"error": "Ingresó acciones negativas?"})
        
        if tipo == "V" and candidato is None:
            raise serializers.ValidationError({"error": "El voto de tipo 'V' sólo es válido si seleccionas un Candidato"})
        
        if tipo == "N" and candidato is not None:
            raise serializers.ValidationError({"error": "El voto de tipo 'N' sólo es voto nulo, no envíes candidato"})
        
        if attrs["eleccion"].pk not in e_manager.get_actual_election().values_list("pk", flat=True):
            raise serializers.ValidationError({
                "error": ("No puede votar en elecciones que aún no han comenzado."
                        f" Estas elecciones comienzan el día {eleccion.fecha_inicio.date()}")
                })
        
        
        return attrs

class VotosSerializer(serializers.Serializer):
    votos = serializers.ListField(
        child=VotarModelSerializer(),
        allow_empty=True,
        max_length=8, #! Cambiar, porq esto es así por ahora XD
    )
    elecciones: serializers.PrimaryKeyRelatedField(
        queryset=Eleccion.objects.all(),
    )
    
    def validate_votos(self, votos:list[TVotoData]) -> list[TVotoData]:
        if len(votos) > 8:
            raise serializers.ValidationError({"error": "Más de 8 votos"})
        
        return votos
    
    def validate(self, attrs:TVotoSerializerData) -> TVotoSerializerData:
        elecciones_candidato:QuerySet[Elecciones_Candidato] = attrs["elecciones"].elecciones_candidato_set.all()
        
        conteo = {
            
        }
        # Ciclo para contar cuántos votos se han hecho por Cargo
        for voto in attrs["votos"]:
            if voto["tipo"] == "N":
                continue
            
            
            # Obtengo el Cargo que está siendo votado a este candidato
            obj = elecciones_candidato.filter(candidato=voto["candidato"]).first()
            # Si el cargo no está siendo conteado, lo inicializo
            if obj.cargo.description not in conteo:
                conteo[obj.cargo.description] = {"count": 0}
            
            # +1 porque el voto que actualmente está iterando es para este candidato con este cargo
            conteo[obj.cargo.description]["count"] += 1
            if conteo[obj.cargo.description]["count"] > obj.cargo.max_votos:
                raise serializers.ValidationError({"error": "Votó más veces de lo permitido a este cargo"})
        
        
        return attrs