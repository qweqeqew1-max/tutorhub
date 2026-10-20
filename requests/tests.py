from django.test import TestCase
from django.urls import reverse
from .models import Request
from subjects.models import Subject


class RequestViewsTest(TestCase):
    """Тесты страниц приложения requests"""

    def setUp(self):
        """Перед каждым тестом создаём предмет — он нужен для страницы формы"""
        self.subject = Subject.objects.create(name="Математика", slug="matematika")

    def test_form_page_status_200(self):
        """Страница формы заявки отвечает 200"""
        response = self.client.get(reverse('requests:create'))
        self.assertEqual(response.status_code, 200)

    def test_success_page_status_200(self):
        """Страница 'спасибо за заявку' отвечает 200"""
        response = self.client.get(reverse('requests:success'))
        self.assertEqual(response.status_code, 200)

    def test_form_submit_creates_request(self):
        """Отправка формы создаёт заявку и перекидывает на страницу успеха"""
        response = self.client.post(reverse('requests:create'), {
            'name': 'Тест Тестов',
            'phone': '+79990000000',
            'email': 'test@example.com',
            'subject': self.subject.pk,
            'tutor': '',
            'date': '2026-11-01',
        })
        # После успешной отправки происходит redirect (код 302)
        self.assertEqual(response.status_code, 302)
        # И заявка действительно появилась в базе
        self.assertEqual(Request.objects.count(), 1)
