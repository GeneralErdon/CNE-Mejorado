

from apps.base.serializers import BaseReadOnlySerializer
from apps.candidatos.models import Candidato


class CandidatoReadOnlySerializer(BaseReadOnlySerializer):
    
    class Meta:
        model = Candidato
        fields = "__all__"