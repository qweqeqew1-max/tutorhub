from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название предмета')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name