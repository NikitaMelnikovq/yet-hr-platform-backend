from django.urls import path
from .views import (
    ManagerVacancyCreateAPIView,
    VacancyRetrieveAPIView,
    ManagerVacancyDetailAPIView,
    VacancyListView
)

app_name = 'vacancies'

urlpatterns = [
    path('manager/vacancies/create', ManagerVacancyCreateAPIView.as_view(), name='vacancy-create'),
    path('vacancies/<int:pk>/', VacancyRetrieveAPIView.as_view(), name='vacancy-detail'),
    path('vacancies/', VacancyListView.as_view(), name="vacancy-list"),
    path('manager/vacancies/<int:id>', ManagerVacancyDetailAPIView.as_view(), name='vacancy-update-delete'),
]
