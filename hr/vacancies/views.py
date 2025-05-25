# vacancies/views.py
import requests

from rest_framework import generics, parsers
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.views import View

from .serializers import VacancySerializer, CandidateResponseSerializer
from .permissions import IsManager
from .models import (
    Vacancy, Area, CandidateResponse,
    WorkFormat, WorkTime, WorkSchedule, ExperienceLevel
)

HH_API_URL = "https://api.hh.ru/vacancies"
USER_AGENT = "Mozilla/5.0 (Linux x86_64) Gecko/20100101 Firefox/45.9"

FORMAT_MAP = {
    "remote": WorkFormat.REMOTE,
    "in_office": WorkFormat.ON_SITE,
    "hybrid": WorkFormat.HYBRID,
    "field": WorkFormat.FIELD_WORK,
}
SCHEDULE_MAP = {
    "fullDay": WorkSchedule.FIVE_ON_TWO_OFF,
    "shift":    WorkSchedule.SEVEN_ON_ZERO_OFF,
    "flexible": WorkSchedule.TWO_ON_TWO_OFF,
}
EXP_MAP = {
    "noExperience":   ExperienceLevel.NO_EXPERIENCE,
    "between1and3":   ExperienceLevel.BETWEEN_1_AND_3,
    "between3and6":   ExperienceLevel.BETWEEN_3_AND_6,
    "moreThan6":      ExperienceLevel.MORE_THAN_SIX,
}

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


class UserVacancyDetailAPIView(generics.RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    lookup_field = 'id'
    http_method_names = ['get']


class VacancyListView(generics.ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        qs = Vacancy.objects.all()
        param = self.request.query_params.get('archived')

        if param is None:
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


class CandidateResponseList(generics.ListAPIView):
    serializer_class = CandidateResponseSerializer
    
    def get_queryset(self):
        qs = CandidateResponse.objects.all()
        status = self.request.query_params.get('status')
        if status in dict(CandidateResponse._meta.get_field('status').choices):
            qs = qs.filter(status=status)
        return qs


class CandidateResponseView(generics.RetrieveUpdateAPIView):
    queryset = CandidateResponse.objects.all()
    serializer_class = CandidateResponseSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        self.partial = True
        return super().update(request, *args, **kwargs)

@method_decorator(csrf_exempt, name="dispatch")
class SyncVacanciesView(View):
    def post(self, request, *args, **kwargs):
        employer_id = getattr(settings, "HH_EMPLOYER_ID", None)
        if not employer_id:
            return HttpResponseBadRequest("Не задан HH_EMPLOYER_ID в settings")

        params = {"employer_id": employer_id, "per_page": 100, "page": 0}
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        created = 0

        # Сразу подтягиваем все существующие заголовки в нижнем регистре
        exists_titles = set(
            Vacancy.objects.values_list("title", flat=True)
        )
        exists_titles = {t.lower() for t in exists_titles}

        while True:
            resp = requests.get(HH_API_URL, params=params, headers=headers)
            resp.raise_for_status()
            payload = resp.json()

            with transaction.atomic():
                for item in payload["items"]:
                    title = item["name"].strip()
                    if title.lower() in exists_titles:
                        continue

                    descr       = item.get("snippet", {}).get("responsibility", "") or ""
                    short_descr = item.get("snippet", {}).get("requirement", "") or ""
                    sal         = item.get("salary") or {}
                    salary_from = sal.get("from")
                    salary_to   = sal.get("to")
                    addr        = item.get("address", {}).get("raw", "") or ""
                    pub         = parse_datetime(item["published_at"])

                    wf = item.get("work_format", {})[0].get("id")
                    wf = [wf]
                    sched_id = item.get("schedule", {}).get("id")
                    schedule = SCHEDULE_MAP.get(sched_id)

                    exp_id = item.get("experience", {}).get("id")
                    
                    vac = Vacancy.objects.create(
                        title=title,
                        description=descr,
                        short_description=short_descr,
                        salary_from=salary_from,
                        salary_to=salary_to,
                        address_raw=addr,
                        published_at=pub,
                        work_formats=wf,
                        work_schedule=schedule,
                        required_experience=exp_id,
                    )

                    area_name = item.get("area", {}).get("name")
                    if area_name:
                        area_obj, _ = Area.objects.get_or_create(name=area_name)
                        vac.areas.add(area_obj)

                    exists_titles.add(title.lower())
                    created += 1

            if params["page"] + 1 >= payload["pages"]:
                break
            params["page"] += 1

        return JsonResponse({"created": created, "total_pages": payload["pages"]})