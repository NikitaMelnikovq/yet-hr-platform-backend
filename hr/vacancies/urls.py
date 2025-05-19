from django.urls import path
from .views import (
    ManagerVacancyCreateAPIView,
    VacancyRetrieveAPIView,
    ManagerVacancyDetailAPIView,
    VacancyListView,
    ReceiveCandidateResponseView,
    CandidateResponseList,
    UserVacancyDetailAPIView,
    CandidateResponseView
)

app_name = 'vacancies'

urlpatterns = [
    path('manager/vacancies/create', ManagerVacancyCreateAPIView.as_view(), name='vacancy-create'),
    path('user/vacancy/<int:id>/', UserVacancyDetailAPIView.as_view(), name='user-vacancy-datail'),
    path('vacancies/<int:pk>/', VacancyRetrieveAPIView.as_view(), name='vacancy-detail'),
    path('vacancies/', VacancyListView.as_view(), name="vacancy-list"),
    path('manager/vacancies/<int:id>/', ManagerVacancyDetailAPIView.as_view(), name='vacancy-update-delete'),
    path('candidate/response/create/', ReceiveCandidateResponseView.as_view(), name='candidate-response'),
    path('candidate/responses/', CandidateResponseList.as_view(), name='responses-list'),
    path('candidate/response/<int:id>', CandidateResponseView.as_view(), name='response'),
]
