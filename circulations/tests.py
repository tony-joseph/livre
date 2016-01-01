from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import BookCirculation
from items.models import Language, Category, BookDetail, BookCopy


class CirculationsViewsTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='user_1', password='pass1234')
        self.user_2 = User.objects.create_user(username='user_2', password='pass1234')
        self.staff_user = User.objects.create_user(username='staff_user', password='pass1234', is_staff=True)
        self.language = Language.objects.create(
            name='test language',
            short_code='tl',
            created_by=self.staff_user,
            updated_by=self.staff_user,
        )
        self.category = Category.objects.create(
            title='test category',
            slug='test-category',
            created_by=self.staff_user,
            updated_by=self.staff_user,
        )
        self.book_detail_1 = BookDetail.objects.create(
            title='Test book detail',
            author='test author',
            category=self.category,
            language=self.language,
            created_by=self.staff_user,
            updated_by=self.staff_user,
        )
        self.book_copy_1 = BookCopy.objects.create(
            book_detail=self.book_detail_1,
            book_status=1,
            created_by=self.staff_user,
            updated_by=self.staff_user,
        )

    def test_add_book(self):
        client = Client()
        client.login(username='staff_user', password='pass1234')
        response = client.post(reverse('circulations:add_circulation'), {
            'username': self.user_1.username,
            'book_id': self.book_copy_1.id,
        })
        print(response)
        client.post('{}?user={}&book={}'.format(reverse('circulations:add_circulation_confirm'), self.user_1.id,
                                                self.book_detail_1.id), {
            'issued_on': '2015-12-20',
            'due_date': '2015-12-21',
        })
        self.assertEqual(BookCirculation.objects.filter(book_copy=self.book_copy_1,
                                                        user=self.user_1, is_returned=False).exists(), True)

    def test_book_multiple_issue(self):
        """Checks if a book in circulation can be issued to another user."""

        client = Client()
        client.login(username='staff_user', password='pass1234')
        client.post(reverse('circulations:add_circulation'), {
            'username': self.user_1.username,
            'book_id': self.book_copy_1.id,
        })
        client.post('{}?user={}&book={}'.format(reverse('circulations:add_circulation_confirm'), self.user_1.id,
                                                self.book_detail_1.id), {
            'issued_on': '2015-12-20',
            'due_date': '2015-12-21',
        })
        client.post(reverse('circulations:add_circulation'), {
            'username': self.user_2.username,
            'book_id': self.book_copy_1.id,
        })
        client.post('{}?user={}&book={}'.format(reverse('circulations:add_circulation_confirm'), self.user_2.id,
                                                self.book_detail_1.id), {
            'issued_on': '2015-12-20',
            'due_date': '2015-12-21',
        })
        self.assertEqual(BookCirculation.objects.filter(book_copy=self.book_copy_1,
                                                        user=self.user_2, is_returned=False).exists(), False)
