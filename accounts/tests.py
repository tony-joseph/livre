from django.test import TestCase
from django.contrib.auth.models import User

from .models import UserProfile


class AccountsTestCase(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='new-user', first_name='Test name', last_name='Test name',
                                                 password='newpass1234')

    def test_account_creation(self):
        """Tests creation and user profile creation.

        Checks user profile is created when a new user account is created.
        """
        self.assertEqual(UserProfile.objects.filter(user=self.new_user).exists(), True)
