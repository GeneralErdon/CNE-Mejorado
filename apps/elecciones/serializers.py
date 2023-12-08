from rest_framework import serializers
from django.db.models import QuerySet

from apps.base.serializers import BaseReadOnlySerializer
from apps.base.utils import EleccionesManager
from apps.candidatos.models import Cargo
from apps.candidatos.serializers import CandidatoReadOnlySerializer

from apps.elecciones.models import Eleccion, Elecciones_Candidato, Voto
from apps.elecciones.types import TVotoData, TVotoSerializerData


class Elecciones_CandidatoSerializer(BaseReadOnlySerializer):
    candidato = CandidatoReadOnlySerializer(read_only=True)
    cargo = serializers.CharField(source="cargo.description", read_only=True)
    class Meta:
        model = Elecciones_Candidato
        fields = ("candidato", "cargo",)

class EleccionReadOnlySerializer(BaseReadOnlySerializer):
    fecha_inicio = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    fecha_final = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    candidatos = serializers.SerializerMethodField("get_candidatos")
    
    class Meta:
        model = Eleccion
        fields = "__all__"
    
    def get_candidatos(self, obj:Eleccion):
        
        result = {}
        elecciones_candidato_qs:QuerySet[Elecciones_Candidato] = obj.elecciones_candidato_set.all()
        
        for e_c in elecciones_candidato_qs:
            if e_c.cargo.description not in result:
                result[e_c.cargo.description] = []
            
            result[e_c.cargo.description].append(CandidatoReadOnlySerializer(e_c.candidato).data)
        
        
        return result


class VotarModelSerializer(BaseReadOnlySerializer):
    class Meta:
        model = Voto
        fields = "__all__"
        read_only_fields = ("created_date","modified_date", "deleted_date", "changed_by",)
    
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
        
        # Verifica la PK de la eleccion actual, con las Elecciones Activas. a ver si estamos en epoca de elecciones
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
        #max_length=8, #! Cambiar, porq esto es así por ahora XD
    )
    elecciones = serializers.PrimaryKeyRelatedField(
        queryset=EleccionesManager().get_actual_election(),
    )
    
    
    
    def validate(self, attrs:TVotoSerializerData) -> TVotoSerializerData:
        elecciones_candidato:QuerySet[Elecciones_Candidato] = attrs["elecciones"].elecciones_candidato_set.all()
        
        conteo:dict[str, int] = {}
        # Obtengo los Cargos que participan en estas elecciones, y Obtengo la cantidad de veces que cada persona puede votar
        # Los diferencio por el PK del cargo
        votos_maximos = sum(elecciones_candidato.values_list("cargo__max_votos", flat=True).distinct("cargo__pk"))
        
        if len(attrs["votos"]) > votos_maximos:
            raise serializers.ValidationError({"error": "Más del máximo de votos (%s)" % votos_maximos})
        
        acciones = 0
        # Ciclo para contar cuántos votos se han hecho por Cargo
        for voto in attrs["votos"]:
            
            acciones = voto["acciones"]
            
            if voto["eleccion"].pk != attrs["elecciones"].pk:
                raise serializers.ValidationError({"error": "Los votos deben ser para las elecciones actuales."})
            
            if voto["tipo"] == "N":
                continue
            # Obtengo el Cargo que está siendo votado a este candidato
            obj = elecciones_candidato.filter(candidato=voto["candidato"]).first()
            # Si el cargo no está siendo conteado, lo inicializo
            if obj.cargo.description not in conteo:
                conteo[obj.cargo.description] =  0
            
            # +1 porque el voto que actualmente está iterando es para este candidato con este cargo
            conteo[obj.cargo.description] += 1
            if conteo[obj.cargo.description] > obj.cargo.max_votos:
                raise serializers.ValidationError({"error": "Votó más veces de lo permitido a este cargo"})
        
        
        # Rellena con Votos nulos en caso de no haber votado completamente
        while len(attrs["votos"]) < votos_maximos:
            attrs["votos"].append({"tipo":"N", "acciones":acciones, "eleccion": attrs["elecciones"], "candidato": None})
        
        return attrs
    
    def create(self, validated_data:TVotoSerializerData):
        
        votos = validated_data["votos"]
        
        return Voto.objects.bulk_create(Voto(**voto) for voto in votos)