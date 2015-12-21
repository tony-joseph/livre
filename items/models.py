from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse


BOOK_STATUS_CHOICES = (
    (1, 'Available'),
    (2, 'In Circulation'),
    (3, 'Temporarily Unavailable'),
    (4, 'Unavailable'),
    (5, 'Protected'),
    (6, 'Damaged'),
)


class Category(models.Model):
    """Item category model."""

    title = models.CharField(max_length=512)
    slug = models.SlugField(max_length=128, unique=True, db_index=True)
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='category_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('items:view_category', kwargs={'slug': self.slug})


class Language(models.Model):
    """Language model"""

    name = models.CharField(max_length=512)
    short_code = models.CharField(max_length=8, db_index=True, unique=True)
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='language_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items:view_language', kwargs={'slug': self.short_code})


class BookDetail(models.Model):
    """Model to store book details."""

    title = models.CharField(max_length=1024)
    author = models.CharField(max_length=1024, default='Unknown')
    description = models.TextField(blank=True, default='')
    category = models.ForeignKey(Category)
    language = models.ForeignKey(Language)
    publisher = models.CharField(max_length=512, blank=True, default='')
    published_on = models.DateField(blank=True, null=True)
    pages = models.PositiveIntegerField(default=0, blank=True, null=True)
    ddc = models.CharField(max_length=1024, blank=True, default='')
    llcc = models.CharField(max_length=1024, blank=True, default='')
    isbn = models.CharField(max_length=1024, blank=True, default='')
    tags = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='book_detail_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('items:view_book_detail', kwargs={'id': self.id})

    def get_tags_string(self):
        return self.tags.capitalize()


class BookCopy(models.Model):
    """Model to store book copy details."""

    book_detail = models.ForeignKey(BookDetail)
    book_status = models.IntegerField(choices=BOOK_STATUS_CHOICES)
    remarks = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='book_copy_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('items:view_book_copy', kwargs={'book_id': self.book_detail.id, 'copy_id': self.id})


class Periodical(models.Model):
    """Model to store periodical data."""

    title = models.CharField(max_length=1024)
    description = models.TextField(blank=True, default='')
    category = models.ForeignKey(Category)
    language = models.ForeignKey(Language)
    publisher = models.CharField(max_length=512, blank=True, default='')
    tags = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='periodical_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('items:view_periodical', kwargs={'id': self.id})

    def get_tags_string(self):
        return self.tags.capitalize()


class PeriodicalIssue(models.Model):
    """Model to store periodical issues."""

    periodical = models.ForeignKey(Periodical)
    issue_status = models.IntegerField(choices=BOOK_STATUS_CHOICES)
    published_on = models.DateField(blank=True, null=True)
    volume = models.PositiveIntegerField(blank=True, null=True)
    issue = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, default='')
    tags = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='periodical_issue_updated_by')
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('items:view_periodical_issue', kwargs={'periodical_id': self.periodical.id, 'issue_id': self.id})

    def get_tags_string(self):
        return self.tags.capitalize()
