from django.test import TestCase
from django.urls import reverse
from .models import Tutor
from subjects.models import Subject


class TutorModelTest(TestCase):
    """Тесты для модели Tutor (репетитор)"""

    def setUp(self):
        self.subject = Subject.objects.create(name="Математика", slug="matematika")

    def test_create_tutor(self):
        """Репетитор создаётся с обязательными полями"""
        tutor = Tutor.objects.create(
            name="Иван Иванов",
            experience=5,
            price=1500,
            subject=self.subject
        )
        self.assertEqual(tutor.name, "Иван Иванов")
        self.assertEqual(tutor.experience, 5)
        self.assertEqual(tutor.subject, self.subject)
        self.assertIsNotNone(tutor.pk)

    def test_str_method(self):
        """Метод __str__ возвращает имя репетитора"""
        tutor = Tutor.objects.create(
            name="Анна Петрова",
            experience=3,
            price=1200,
            subject=self.subject
        )
        self.assertEqual(str(tutor), "Анна Петрова")


class TutorViewsTest(TestCase):
    """Тесты страниц приложения tutors"""

    def setUp(self):
        self.subject = Subject.objects.create(name="Математика", slug="matematika")
        self.tutor = Tutor.objects.create(
            name="Иван Иванов",
            experience=5,
            price=1500,
            subject=self.subject
        )

    def test_tutor_list_status_200(self):
        """Страница списка репетиторов отвечает 200"""
        response = self.client.get(reverse('tutors:list'))
        self.assertEqual(response.status_code, 200)

    def test_tutor_list_shows_tutor(self):
        """Созданный репетитор виден на странице списка"""
        response = self.client.get(reverse('tutors:list'))
        self.assertContains(response, "Иван Иванов")

    def test_tutor_detail_status_200(self):
        """Страница конкретного репетитора отвечает 200"""
        response = self.client.get(reverse('tutors:detail', args=[self.tutor.pk]))
        self.assertEqual(response.status_code, 200)

    def test_tutor_detail_404_for_wrong_id(self):
        """Несуществующий репетитор даёт 404, а не падает с ошибкой"""
        response = self.client.get(reverse('tutors:detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_tutor_list_filter_by_subject(self):
        """Фильтр по предмету (?subject=...) работает и отвечает 200"""
        response = self.client.get(reverse('tutors:list') + '?subject=matematika')
        self.assertEqual(response.status_code, 200)
