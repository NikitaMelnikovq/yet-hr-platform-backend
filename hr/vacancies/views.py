# vacancies/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Vacancy
from .serializers import VacancySerializer
from .permissions import IsManager

class ManagerVacancyCreateAPIView(generics.CreateAPIView):
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated, IsManager]

class VacancyRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

class ManagerVacancyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsManager]
    http_method_names = ['get', 'patch', 'delete']

class VacancyListView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer