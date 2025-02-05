from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model


def transliterate(text):
    """"Функция костыль для слага"""
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
        'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }

    transliterated_text = ''.join(translit_dict.get(
        char, char) for char in text.lower())
    return transliterated_text


class Place(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название места'
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='Url изображения места'
    )
    city = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название города/пгт/мегаполиса'
    )
    website = models.URLField(
        max_length=500,
        blank=False,
        verbose_name='Сайт места'
    )
    rating = models.FloatField(
        blank=False,
        verbose_name='Рейтинг места'
    )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название мероприятия'
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=False
    )

    plan = models.TextField(
        blank=False,
        verbose_name='План мероприятия'
    )
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name='Время создания')
    person = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Ссылка на человека'
    )
    place = models.ForeignKey(
        to=Place,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        verbose_name='Ссылка на место'
    )

    class Meta:
        verbose_name = "Мероприятия"
        verbose_name_plural = 'Мероприятия'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        current_time = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')
        base_slug = slugify(transliterate(
            f"{self.person.username}-{self.place.name}-{current_time}"))
        self.slug = base_slug[:255]
        super().save(*args, **kwargs)


class Upload_files(models.Model):
    file = models.FileField()

    class Meta:
        verbose_name = "Изображения"
        verbose_name_plural = 'Изображения'
