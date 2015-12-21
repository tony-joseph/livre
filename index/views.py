from django.shortcuts import render

from items.models import BookDetail, BookCopy, Periodical, PeriodicalIssue, Category, Language


def index(request):
    """Home page."""

    stats = {
        'books': BookDetail.objects.all().count(),
        'book_copies': BookCopy.objects.all().count(),
        'periodicals': Periodical.objects.all().count(),
        'periodical_issues': PeriodicalIssue.objects.all().count(),
        'categories': Category.objects.all().count(),
        'languages': Language.objects.all().count(),
    }

    return render(request, 'index/index.html', {'stats': stats})
