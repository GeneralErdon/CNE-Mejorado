from rest_framework import serializers
from apps.base.serializers import BaseReadOnlySerializer
from apps.candidatos.serializers import CandidatoReadOnlySerializer

from apps.elecciones.models import Eleccion, Voto

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
        exclude = ("created_date", "modified_date", "deleted_date", "changed_by")
    
    def validate(self, attrs:dict) -> dict:
        
        
        
        return attrs

class VotosSerializer(serializers.Serializer):
    votos = serializers.ListField(
        child=VotarModelSerializer(),
        allow_empty=True,
        max_length=8, #! Cambiar, porq esto es así por ahora XD
    )
    
    def validate_votos(self, votos:list):
        if len(votos) > 8:
            raise serializers.ValidationError({"error": "Más de 8 votos"})
        
        
        
        
        return votos