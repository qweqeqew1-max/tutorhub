from django.test import TestCase
from django.urls import reverse
from subjects.models import Subject
from tutors.models import Tutor


class IndexViewTest(TestCase):
    """Тесты главной страницы"""

    def setUp(self):
        """Главная показывает активных репетиторов — создаём один тестовый набор"""
        subject = Subject.objects.create(name="Математика", slug="matematika")
        self.tutor = Tutor.objects.create(
            name="Иван Иванов",
            experience=5,
            price=1500,
            subject=subject,
            is_active=True
        )

    def test_index_status_200(self):
        """Главная страница отвечает 200"""
        response = self.client.get(reverse('pages:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_shows_active_tutor(self):
        """Активный репетитор виден на главной"""
        response = self.client.get(reverse('pages:index'))
        self.assertContains(response, "Иван Иванов")

    def test_index_hides_inactive_tutor(self):
        """Неактивный репетитор НЕ виден на главной"""
        self.tutor.is_active = False
        self.tutor.save()
        response = self.client.get(reverse('pages:index'))
        self.assertNotContains(response, "Иван Иванов")


class AboutViewTest(TestCase):
    """Тесты страницы 'О нас'"""

    def test_about_status_200(self):
        response = self.client.get(reverse('pages:about'))
        self.assertEqual(response.status_code, 200)


class ContactsViewTest(TestCase):
    """Тесты страницы контактов"""

    def test_contacts_status_200(self):
        response = self.client.get(reverse('pages:contacts'))
        self.assertEqual(response.status_code, 200)
