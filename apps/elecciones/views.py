from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from rest_framework.viewsets import GenericViewSet
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework import status

from apps.base.utils import EleccionesManager
from apps.elecciones.models import Eleccion, Voto
from apps.elecciones.serializers import EleccionReadOnlySerializer, VotarModelSerializer

# Create your views here.

class NotFoundView(View):
    def get(self, request:HttpRequest, *args, **kwargs):
        
        return render(request, "404.html")

class HomePage(View):
    
    
    def get(self, request, *args, **kwargs):
        e_manager = EleccionesManager()
        context = {
            "eleccion": None
        }
        
        proximas_elecciones = e_manager.get_proximas_elecciones()
        
        if proximas_elecciones.exists():
            
            if e_manager.is_today_election():
                # Si hoy es día de elecciones
                actual_eleccion = e_manager.get_actual_election().first()
                context['eleccion'] = EleccionReadOnlySerializer(actual_eleccion).data
                return render(request, 'apps/elecciones/elecciones_actual.html', context=context, status=status.HTTP_200_OK)
            
            else:
                # Si no es día de elecciones, pero hay elecciones planificadas, aquí se mostrará el conteo regresivo.
                return render(request, 'index.html', {}, status=status.HTTP_200_OK)
        
        # No hay nada planificado XD
        return render(request, '400.html', status=status.HTTP_400_BAD_REQUEST)

class VotarView(CreateView):
    
    """
    Ok la idea es la siguiente
    1 voto por presidente
    1 voto por vice presidente
    8 por director???
    
    en total serían 10 votos por persona 
    si Vota por menos de 10 candidatos, entonces los restantes se registrarán como votos Nulos con su cantidad de acciones
    
    El inpur podría ser un Array de Votos?
    [
        {candidato: 1, eleccion: 1, acciones: 22, tipo: "V"},
        ...
    ]
    
    en caso de Array .lenght <= 10. Se completa el resto con votos Nulos, o sea candidato None y tipo "nulo"
    
    luego se reinicia para el siguiente conteo.
    
    
    Acomodar el Jazzmin
    
    """
    
    model = Voto
    serializer_class = VotarModelSerializer
    
    def get_serializer_class(self, instance=None, data=None, *args, **kwargs) -> VotarModelSerializer:
        return self.serializer_class(instance, data, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        
        serializer = self.get_serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                "message": "Votos creados con éxito",
            }, status=status.HTTP_200_OK)
        
        
        return Response({
            "message": "Error, datos inválidos",
            **serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)