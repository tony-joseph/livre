from django import forms

from .models import Category, Language, BOOK_STATUS_CHOICES


# Trying to use Category and Language models before running migrations will result in errors.
# Try block is used to prevent those errors.
try:
    CATEGORY_CHOICES = [[x.slug, x.title] for x in Category.objects.all()]
    LANGUAGE_CHOICES = [[x.short_code, x.name] for x in Language.objects.all()]
except:
    CATEGORY_CHOICES = []
    LANGUAGE_CHOICES = []


class CategoryForm(forms.Form):
    title = forms.CharField(label='Title*:', max_length=500, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Title'
    }))
    slug = forms.SlugField(label='Slug*:', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Slug',
    }))
    description = forms.CharField(label='Description:', max_length=4000, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description',
    }), required=False)


class LanguageForm(forms.Form):
    name = forms.CharField(label='Name*:', max_length=500, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Name'
    }))
    short_code = forms.SlugField(label='Short code*:', max_length=8, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Short code',
    }))
    description = forms.CharField(label='Description:', max_length=4000, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description',
    }), required=False)


class BookDetailForm(forms.Form):
    title = forms.CharField(label='Title*:', max_length=1000, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Title'
    }))
    author = forms.CharField(label='Author*:', max_length=1000, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Author'
    }))
    description = forms.CharField(label='Description:', max_length=10000, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description',
    }), required=False)
    category = forms.ChoiceField(label='Category*:', choices=CATEGORY_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'required': 'required',
    }, choices=CATEGORY_CHOICES))
    language = forms.ChoiceField(label='Language*:', choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'required': 'required',
    }, choices=LANGUAGE_CHOICES))
    publisher = forms.CharField(label='Publisher:', max_length=500, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Publisher'
    }), required=False)
    published_on = forms.DateField(label='Published on:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Published on'
    }), required=False)
    pages = forms.IntegerField(label='Pages:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Pages',
    }), required=False)
    isbn = forms.CharField(label='ISBN:', max_length=1000, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ISBN',
    }), required=False)
    tags = forms.CharField(label='Tags:', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tags'
    }))


class BookCopyForm(forms.Form):
    book_status = forms.ChoiceField(label='Book status*:', widget=forms.Select(choices=BOOK_STATUS_CHOICES, attrs={
        'class': 'form-control',
    }), choices=BOOK_STATUS_CHOICES)
    remarks = forms.CharField(label='Description:', max_length=4000, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Remarks',
    }), required=False)


class PeriodicalForm(forms.Form):
    title = forms.CharField(label='Title*:', max_length=1000, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Title'
    }))
    description = forms.CharField(label='Description:', max_length=10000, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description',
    }), required=False)
    category = forms.ChoiceField(label='Category*:', choices=CATEGORY_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'required': 'required',
    }, choices=CATEGORY_CHOICES))
    language = forms.ChoiceField(label='Language*:', choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'required': 'required',
    }, choices=LANGUAGE_CHOICES))
    publisher = forms.CharField(label='Publisher:', max_length=500, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Publisher'
    }), required=False)
    tags = forms.CharField(label='Tags:', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tags'
    }))


class PeriodicalIssueForm(forms.Form):
    issue_status = forms.ChoiceField(label='Issue status*:', widget=forms.Select(choices=BOOK_STATUS_CHOICES, attrs={
        'class': 'form-control',
    }), choices=BOOK_STATUS_CHOICES)
    published_on = forms.DateField(label='Published on:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Published on'
    }), required=False)
    volume = forms.IntegerField(label='Volume:', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Volume',
    }))
    issue = forms.IntegerField(label='Issue:', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Issue',
    }))
    remarks = forms.CharField(label='Description:', max_length=4000, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Remarks',
    }), required=False)
    tags = forms.CharField(label='Tags:', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tags'
    }))
