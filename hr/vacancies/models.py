import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class WorkFormat(models.TextChoices):
    ON_SITE    = 'ON_SITE',    'Офис'
    REMOTE     = 'REMOTE',     'Удалённо'
    HYBRID     = 'HYBRID',     'Гибрид'
    FIELD_WORK = 'FIELD_WORK', 'Разъездная работа'


class WorkTime(models.TextChoices):
    HOURS_2 = 'HOURS_2', '2 ч'
    HOURS_4 = 'HOURS_4', '4 ч'
    HOURS_6 = 'HOURS_6', '6 ч'
    HOURS_8 = 'HOURS_8', '8 ч'


class WorkSchedule(models.TextChoices):
    SEVEN_ON_ZERO_OFF = 'SEVEN_ON_ZERO_OFF', '7/0'
    FIVE_ON_TWO_OFF   = 'FIVE_ON_TWO_OFF',   '5/2'
    TWO_ON_TWO_OFF    = 'TWO_ON_TWO_OFF',    '2/2'


class ExperienceLevel(models.TextChoices):
    NO_EXPERIENCE   = 'noExperience',   'Нет опыта'
    BETWEEN_1_AND_3 = 'between1and3',   '1‑3 года'
    BETWEEN_3_AND_6 = 'between3and6',   '3‑6 лет'
    MORE_THAN_SIX   = 'moreThan6',   'более 6-ти лет'


class ResponseStatus(models.TextChoices):
    NOT_VIEWED          = 'NOT_VIEWED',          'Не просмотрено'
    REJECTED            = 'REJECTED',            'Отклонено'
    APPROVED            = 'APPROVED',            'Одобрено'
    INTERVIEW_CONFIRMED = 'INTERVIEW_CONFIRMED', 'Собес. назначено'
    CLOSED              = 'CLOSED',              'Закрыто'


class Area(models.Model):
    """
    Наследуемся от UUIDField, чтобы area_id на схеме (area_uuid) был
    уникальным ключом‑ссылкой, удобным при импорте из внешних систем.
    """
    id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self) -> str:
        return self.name


class Vacancy(models.Model):
    title             = models.CharField(max_length=255)
    description       = models.TextField()
    short_description = models.CharField(max_length=500)
    areas             = models.ManyToManyField(Area, related_name='vacancies')


    salary_from = models.PositiveIntegerField(null=True, blank=True)
    salary_to   = models.PositiveIntegerField(null=True, blank=True)

    address_raw  = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    archived     = models.BooleanField(default=False)

    work_formats = ArrayField(
        models.CharField(max_length=20, choices=WorkFormat.choices),
        blank=True,
        default=list
    )
    work_time            = models.CharField(max_length=20, choices=WorkTime.choices,   null=True, blank=True)
    work_schedule        = models.CharField(max_length=30, choices=WorkSchedule.choices, null=True, blank=True)
    required_experience  = models.CharField(max_length=20, choices=ExperienceLevel.choices, null=True, blank=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self) -> str:
        return self.title


class CandidateResponse(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='responses', null=True, blank=True)
    status  = models.CharField(max_length=30, choices=ResponseStatus.choices, default=ResponseStatus.NOT_VIEWED)

    resume_url  = models.URLField(null=True, blank=True)
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)

    name       = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone      = models.CharField(max_length=32)
    email      = models.EmailField()

    # Сколько лет опыта указал кандидат
    experience = models.PositiveIntegerField()

    letter       = models.TextField(null=True, blank=True)
    notes        = models.TextField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    desired_role = models.CharField(max_length=50, default=' ')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self) -> str:
        return f'{self.name} → {self.vacancy}'
