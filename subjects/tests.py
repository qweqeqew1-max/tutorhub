from django.test import TestCase
from django.urls import reverse
from .models import Subject


class SubjectModelTest(TestCase):
    """Тесты для модели Subject (предмет)"""

    def test_create_subject(self):
        """Предмет создаётся и сохраняется в базу"""
        subj = Subject.objects.create(name="Физика", slug="fizika")
        self.assertEqual(subj.name, "Физика")
        self.assertEqual(subj.slug, "fizika")
        self.assertIsNotNone(subj.pk)

    def test_str_method(self):
        """Метод __str__ возвращает название предмета"""
        subj = Subject.objects.create(name="Химия", slug="himiya")
        self.assertEqual(str(subj), "Химия")

    def test_ordering(self):
        """Предметы можно получить из базы и их больше одного"""
        Subject.objects.create(name="Математика", slug="matematika")
        Subject.objects.create(name="История", slug="istoriya")
        self.assertEqual(Subject.objects.count(), 2)


class SubjectViewsTest(TestCase):
    """Тесты страниц приложения subjects"""

    def test_subject_list_status_200(self):
        """Страница списка предметов отвечает 200, даже когда предметов нет"""
        response = self.client.get(reverse('subjects:list'))
        self.assertEqual(response.status_code, 200)

    def test_subject_list_shows_subjects(self):
        """Созданные предметы видны на странице списка"""
        Subject.objects.create(name="Физика", slug="fizika")
        response = self.client.get(reverse('subjects:list'))
        self.assertContains(response, "Физика")
