from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import Language, Category, BookDetail, BookCopy, Periodical, PeriodicalIssue


class ItemsTestCase(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff-user', password='testpass1234', is_staff=True)
        self.non_staff_user = User.objects.create_user(username='non-staff-user', password='testpass1234')

    def test_items_creation_views(self):
        """Tests creation of all items by staff and non staff users."""

        client = Client()

        # Staff user tests
        client.login(username='staff-user', password='testpass1234')

        # Tests category creation by staff user
        client.post(reverse('items:add_category'), {
            'title': 'staff test',
            'slug': 'staff-test'
        })
        self.assertEqual(Category.objects.filter(slug='staff-test').exists(), True)

        # Tests language creation by staff user
        client.post(reverse('items:add_language'), {
            'name': 'staff test',
            'short_code': 'st'
        })
        self.assertEqual(Language.objects.filter(short_code='st').exists(), True)

        client.logout()

        # Non staff user tests.
        client.login(username='non-staff-user', password='testpass1234')

        # Tests language creation by non staff user.
        client.post(reverse('items:add_category'), {
            'title': 'non staff test',
            'slug': 'non-staff-test'
        })
        self.assertEqual(Category.objects.filter(slug='non-staff-test').exists(), False)

        # Tests category creation by non staff user.
        client.post(reverse('items:add_language'), {
            'name': 'staff test',
            'short_code': 'nt'
        })
        self.assertEqual(Language.objects.filter(short_code='nt').exists(), False)

        client.logout()
