from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BookCirculation(models.Model):
    """Model to store book circulations."""

    book_copy = models.ForeignKey('items.BookCopy')
    user = models.ForeignKey(User)
    issued_on = models.DateField()
    issued_by = models.ForeignKey(User, related_name='issued_by_user')
    due_date = models.DateField()
    returned_on = models.DateField(blank=True, null=True)
    returned_by = models.ForeignKey(User, related_name='returned_by_user', blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return not self.is_returned and self.due_date < timezone.now().date()

    def get_status(self):
        if self.is_expired():
            return 'Due'
        elif self.is_returned:
            return 'Returned'
        else:
            return 'On circulation'
