from django.db import models
from subjects.models import Subject

class Tutor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    photo = models.ImageField(upload_to='tutors/', verbose_name='Фото')
    description = models.TextField(verbose_name='Описание')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tutors', verbose_name='Предмет')
    experience = models.IntegerField(verbose_name='Опыт (лет)')
    price = models.IntegerField(verbose_name='Цена за час')
    is_active = models.BooleanField(default=True, verbose_name='Показывать на сайте')

    class Meta:
        verbose_name = 'Репетитор'
        verbose_name_plural = 'Репетиторы'

    def __str__(self):
        return self.name