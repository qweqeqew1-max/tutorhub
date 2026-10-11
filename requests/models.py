from django.db import models
from tutors.models import Tutor
from subjects.models import Subject

class Request(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Репетитор')
    date = models.DateField(verbose_name='Дата занятия')
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.name} — {self.subject.name}'


class Review(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='reviews', verbose_name='Репетитор')
    author = models.CharField(max_length=100, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(default=5, verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.author} — {self.tutor.name}'