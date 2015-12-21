from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from items.models import BookDetail, Periodical


def search_books(request):
    """View to search in books."""

    if request.GET.get('term'):
        term = request.GET.get('term').strip()
        book_details = BookDetail.objects.filter(
            Q(title__icontains=term) |
            Q(author__icontains=term) |
            Q(description__icontains=term)
        )
        page = request.GET.get('page')
        paginator = Paginator(book_details, 50)
        try:
            book_details = paginator.page(page)
        except PageNotAnInteger:
            book_details = paginator.page(1)
        except EmptyPage:
            book_details = paginator.page(paginator.num_pages)
    else:
        term = None
        book_details = None

    context = {
        'term': term,
        'book_details': book_details,
    }
    return render(request, 'search/search-books.html', context)


def search_periodicals(request):
    """View to search in books."""

    if request.GET.get('term'):
        term = request.GET.get('term').strip()
        periodicals = Periodical.objects.filter(
            Q(title__icontains=term) |
            Q(description__icontains=term)
        )
        page = request.GET.get('page')
        paginator = Paginator(periodicals, 50)
        try:
            periodicals = paginator.page(page)
        except PageNotAnInteger:
            periodicals = paginator.page(1)
        except EmptyPage:
            periodicals = paginator.page(paginator.num_pages)
    else:
        term = None
        periodicals = None

    context = {
        'term': term,
        'periodicals': periodicals,
    }
    return render(request, 'search/search-periodicals.html', context)
