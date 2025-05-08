# vacancies/views.py
from rest_framework import generics, parsers
from rest_framework.permissions import IsAuthenticated
from .models import Vacancy
from .serializers import VacancySerializer, CandidateResponseSerializer
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
    """
    GET /api/v1/vacancies/                 → только опубликованные (archived=False)
    GET /api/v1/vacancies/?archived=true   → только архив
    GET /api/v1/vacancies/?archived=false  → только опубликованные
    """
    serializer_class = VacancySerializer

    def get_queryset(self):
        qs = Vacancy.objects.all()
        param = self.request.query_params.get('archived')

        if param is None:                 # без параметра → по умолчанию опубликованные
            return qs.filter(archived=False)

        param = param.lower()
        if param in ('true', '1'):
            return qs.filter(archived=True)
        if param in ('false', '0'):
            return qs.filter(archived=False)

        return qs  # неверное значение – без фильтра

class ReceiveCandidateResponseView(generics.CreateAPIView):
    serializer_class = CandidateResponseSerializer
    parser_classes   = [parsers.MultiPartParser, parsers.FormParser]

    

    