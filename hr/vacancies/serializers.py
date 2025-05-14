# vacancies/serializers.py
from django.utils import timezone
from rest_framework import serializers
from .models import Vacancy, Area, WorkFormat, CandidateResponse

class AreaSlugField(serializers.SlugRelatedField):
    """
    SlugRelatedField, который умеет создавать Area по имени,
    если такой ещё не существует.
    """
    def to_internal_value(self, data):
        try:
            # пробуем стандартный вариант (область уже есть)
            return super().to_internal_value(data)
        except serializers.ValidationError:
            # создаём новую и возвращаем объект
            return self.get_queryset().model.objects.get_or_create(name=data)[0]
        

class VacancySerializer(serializers.ModelSerializer):
    # на входе/выходе вместо id передаём название области
    areas = AreaSlugField(
        many=True,
        slug_field="name",
        queryset=Area.objects.all(),
    )

    work_formats = serializers.ListField(
        child=serializers.ChoiceField(choices=WorkFormat.choices),
        required=False
    )

    class Meta:
        model  = Vacancy
        fields = '__all__'          # или перечислите явным списком
        read_only_fields = ('id', 'published_at')

    # ───────── create/ update ─────────
    def _get_area_obj(self, name: str) -> Area:
        """Берём существующий Area или создаём новый."""
        area, _ = Area.objects.get_or_create(name=name)
        return area

    def create(self, validated_data):
        areas_data = validated_data.pop("areas", [])
        formats_data = validated_data.pop("work_formats", [])
        validated_data['published_at'] = timezone.now()
        # создаём саму вакансию (без m2m и array)
        vacancy = super().create(validated_data)

        # подтягиваем m2m для регионов
        # get_or_create для каждого названия
        area_objs = [
            Area.objects.get_or_create(name=name)[0]
            for name in areas_data
        ]
        vacancy.areas.set(area_objs)

        # записываем массив форматов
        vacancy.work_formats = formats_data
        vacancy.save()

        return vacancy

    def update(self, instance, validated_data):
        areas_data = validated_data.pop("areas", None)
        formats_data = validated_data.pop("work_formats", None)

        vacancy = super().update(instance, validated_data)

        if areas_data is not None:
            area_objs = [
                Area.objects.get_or_create(name=name)[0]
                for name in areas_data
            ]
            vacancy.areas.set(area_objs)

        if formats_data is not None:
            vacancy.work_formats = formats_data
            vacancy.save()

        return vacancy
    
    # чтобы при выводе снова получить строку, а не id
    def to_representation(self, obj):
        rep = super().to_representation(obj)
        # вернём список имён, как и ожидалось на фронте
        rep["areas"] = [area.name for area in obj.areas.all()]
        return rep
    
class CandidateResponseSerializer(serializers.ModelSerializer):
    vacancy = VacancySerializer(read_only=True)

    vacancy_id = serializers.PrimaryKeyRelatedField(
        queryset=Vacancy.objects.all(),
        source='vacancy',
        write_only=True
    )


    class Meta:
        model = CandidateResponse
        fields = [
            'id',
            'vacancy_id',
            'vacancy',
            'resume_url',
            'resume_file',
            'name',
            'birth_date',
            'phone',
            'email',
            'experience',
            'letter',
            'status',
            'created_at',
        ]
