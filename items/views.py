from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Category, Language, BookDetail, BookCopy, Periodical, PeriodicalIssue
from .forms import CategoryForm, LanguageForm, BookDetailForm, BookCopyForm, PeriodicalForm, PeriodicalIssueForm


@login_required
def add_category(request):
    """View to add a new category."""

    if not request.user.is_staff:
        raise Http404

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category.objects.create(
                title=form.cleaned_data['title'],
                slug=form.cleaned_data['slug'],
                description=form.cleaned_data['description'],
                created_by=request.user,
                updated_by=request.user,
            )
            messages.add_message(request, messages.SUCCESS, 'New category added.')
            return redirect(category.get_absolute_url())
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'items/add-category.html', context)


def list_categories(request):
    """View to list all categories."""

    return render(request, 'items/list-categories.html', {'categories': Category.objects.all()})


def view_category(request, slug):
    """View to display category details."""

    category = get_object_or_404(Category, slug=slug)
    return render(request, 'items/view-category.html', {'category': category})


@login_required
def edit_category(request, slug):
    """View to edit a category."""

    if not request.user.is_staff:
        raise Http404
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category.title = form.cleaned_data['title']
            category.slug = form.cleaned_data['slug']
            category.description = form.cleaned_data['description']
            category.updated_by = request.user
            category.save()
            messages.add_message(request, messages.SUCCESS, 'Details updated.')
            return redirect(category.get_absolute_url())
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'items/edit-category.html', context)


@login_required
def delete_category(request, slug):
    """View to delete a category."""

    if not request.user.is_staff:
        raise Http404
    category = get_object_or_404(Category, slug=slug)

    if BookDetail.objects.filter(category=category).exists():
        messages.add_message(request, messages.ERROR, 'Unable to delete. Books exists in this category')
        return redirect(reverse('items:list_categories'))

    category.delete()
    return redirect(reverse('items:categories'))


@login_required
def category_books(request, slug):
    """View to display paginated list of books in the category."""

    category = get_object_or_404(Category, slug=slug)
    book_details = BookDetail.objects.filter(category=category)
    page = request.GET.get('page')
    paginator = Paginator(book_details, 50)
    try:
        book_details = paginator.page(page)
    except PageNotAnInteger:
        book_details = paginator.page(1)
    except EmptyPage:
        book_details = paginator.page(paginator.num_pages)

    context = {
        'book_details': book_details,
        'category': category,
    }
    return render(request, 'items/category-books.html', context)


@login_required
def add_language(request):
    """View to add a new language."""

    if not request.user.is_staff:
        raise Http404

    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = Language.objects.create(
                name=form.cleaned_data['name'],
                short_code=form.cleaned_data['short_code'],
                description=form.cleaned_data['description'],
                created_by=request.user,
                updated_by=request.user,
            )
            messages.add_message(request, messages.SUCCESS, 'New language added.')
            return redirect(language.get_absolute_url())
    else:
        form = LanguageForm()

    context = {
        'form': form,
    }
    return render(request, 'items/add-language.html', context)


def list_languages(request):
    """View to list all languages."""

    return render(request, 'items/list-languages.html', {'languages': Language.objects.all()})


def view_language(request, slug):
    """View to display language details."""

    language = get_object_or_404(Language, short_code=slug)
    return render(request, 'items/view-language.html', {'language': language})


@login_required
def edit_language(request, slug):
    """View to edit a language."""

    if not request.user.is_staff:
        raise Http404
    language = get_object_or_404(Language, short_code=slug)

    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language.name = form.cleaned_data['name']
            language.short_code = form.cleaned_data['short_code']
            language.description = form.cleaned_data['description']
            language.updated_by = request.user
            language.save()
            messages.add_message(request, messages.SUCCESS, 'Details updated.')
            return redirect(language.get_absolute_url())
    else:
        form = LanguageForm()

    context = {
        'form': form,
        'language': language,
    }
    return render(request, 'items/edit-language.html', context)


@login_required
def delete_language(request, slug):
    """View to delete a language."""

    if not request.user.is_staff:
        raise Http404
    language = get_object_or_404(Language, short_code=slug)

    if BookDetail.objects.filter(language=language).exists():
        messages.add_message(request, messages.ERROR, 'Unable to delete. Books exists in this language')
        return redirect(language.get_absolute_url())

    language.delete()
    return redirect(reverse('items:list_languages'))


@login_required
def add_book_detail(request):
    """View to add a new detail."""

    if not request.user.is_staff:
        raise Http404
    if request.method == 'POST':
        form = BookDetailForm(request.POST)
        if form.is_valid():
            language = get_object_or_404(Language, short_code=form.cleaned_data['language'])
            category = get_object_or_404(Category, slug=form.cleaned_data['category'])
            book_detail = BookDetail.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                description=form.cleaned_data['description'],
                category=category,
                language=language,
                publisher=form.cleaned_data['publisher'],
                published_on=form.cleaned_data['published_on'],
                pages=form.cleaned_data['pages'],
                isbn=form.cleaned_data['isbn'],
                tags=form.cleaned_data['tags'],
                created_by=request.user,
                updated_by=request.user,
            )
            BookCopy.objects.create(
                book_detail=book_detail,
                book_status=1,
                created_by=request.user,
                updated_by=request.user,
            )
            messages.add_message(request, messages.SUCCESS, 'New book added.')
            return redirect(book_detail.get_absolute_url())
    else:
        form = BookDetailForm()

    context = {
        'form': form,
    }
    return render(request, 'items/add-book-detail.html', context)


def list_book_details(request):
    """View to list all book detail objects."""

    book_details = BookDetail.objects.all().order_by('id')
    page = request.GET.get('page')
    paginator = Paginator(book_details, 50)
    try:
        book_details = paginator.page(page)
    except PageNotAnInteger:
        book_details = paginator.page(1)
    except EmptyPage:
        book_details = paginator.page(paginator.num_pages)

    return render(request, 'items/list-book-details.html', {'book_details': book_details})


def view_book_detail(request, id):
    """View to display book details."""

    book_detail = get_object_or_404(BookDetail, id=id)
    book_copies = BookCopy.objects.filter(book_detail=book_detail)
    return render(request, 'items/view-book-detail.html', {'book_detail': book_detail, 'book_copies': book_copies})


@login_required
def edit_book_detail(request, id):
    """View to edit a book detail."""

    if not request.user.is_staff:
        raise Http404
    book_detail = get_object_or_404(BookDetail, id=id)

    if request.method == 'POST':
        form = BookDetailForm(request.POST)
        if form.is_valid():
            language = get_object_or_404(Language, short_code=form.cleaned_data['language'])
            category = get_object_or_404(Category, slug=form.cleaned_data['category'])
            book_detail.title = form.cleaned_data['title']
            book_detail.author = form.cleaned_data['author']
            book_detail.description = form.cleaned_data['description']
            book_detail.category = category
            book_detail.language = language
            book_detail.publisher = form.cleaned_data['publisher']
            book_detail.published_on = form.cleaned_data['published_on']
            book_detail.pages = form.cleaned_data['pages']
            book_detail.isbn = form.cleaned_data['isbn']
            book_detail.tags = form.cleaned_data['tags']
            book_detail.updated_by = request.user
            book_detail.save()
            messages.add_message(request, messages.SUCCESS, 'Details updated.')
            return redirect(book_detail.get_absolute_url())
    else:
        form = BookDetailForm()

    context = {
        'form': form,
        'book_detail': book_detail,
    }
    return render(request, 'items/edit-book-detail.html', context)


@login_required
def delete_book_detail(request, id):
    """View to delete a book detail."""

    if not request.user.is_staff:
        raise Http404
    book_detail = get_object_or_404(BookDetail, id=id)

    if BookCopy.objects.filter(book_detail=book_detail).exists():
        messages.add_message(request, messages.ERROR, 'Unable to delete. Book copies exists.')
        return redirect(book_detail.get_absolute_url())

    book_detail.delete()
    return redirect(reverse('items:list_book_details'))


@login_required
def add_book_copy(request, book_id):
    """View to add a copy of a book."""

    if not request.user.is_staff:
        raise Http404
    book_detail = get_object_or_404(BookDetail, id=book_id)

    if request.method == 'POST':
        form = BookCopyForm(request.POST)
        if form.is_valid():
            BookCopy.objects.create(
                book_detail=book_detail,
                book_status=form.cleaned_data['book_status'],
                remarks=form.cleaned_data['remarks'],
                created_by=request.user,
                updated_by=request.user,
            )
            messages.add_message(request, messages.SUCCESS, 'New book copy added')
            return redirect(book_detail.get_absolute_url())
    else:
        form = BookCopyForm()

    context = {
        'form': form,
        'book_detail': book_detail,
    }
    return render(request, 'items/add-book-copy.html', context)


def view_book_copy(request, book_id, copy_id):
    """View to display book copy details."""

    book_detail = get_object_or_404(BookDetail, id=book_id)
    book_copy = get_object_or_404(BookCopy, book_detail=book_detail, id=copy_id)

    context = {
        'book_detail': book_detail,
        'book_copy': book_copy,
    }
    return render(request, 'items/view-book-copy.html', context)


@login_required
def edit_book_copy(request, book_id, copy_id):
    """View to edit book copy details."""

    if not request.user.is_staff:
        raise Http404
    book_detail = get_object_or_404(BookDetail, id=book_id)
    book_copy = get_object_or_404(BookCopy, book_detail=book_detail, id=copy_id)

    if request.method == 'POST':
        form = BookCopyForm(request.POST)
        if form.is_valid():
            book_copy.book_status=form.cleaned_data['book_status']
            book_copy.remarks=form.cleaned_data['remarks']
            book_copy.updated_by=request.user
            book_copy.save()

            messages.add_message(request, messages.SUCCESS, 'Details updated')
            return redirect(book_copy.get_absolute_url())
    else:
        form = BookCopyForm()

    context = {
        'form': form,
        'book_detail': book_detail,
        'book_copy': book_copy,
    }
    return render(request, 'items/edit-book-copy.html', context)


@login_required
def delete_book_copy(request, book_id, copy_id):
    """View to delete book copy."""

    if not request.user.is_staff:
        raise Http404
    book_detail = get_object_or_404(BookDetail, id=book_id)
    book_copy = get_object_or_404(BookCopy, book_detail=book_detail, id=copy_id)
    book_copy.delete()
    messages.add_message(request, messages.SUCCESS, 'Book copy deleted')
    return redirect(book_detail.get_absolute_url())


@login_required
def add_periodical(request):
    """View to add a new periodical."""

    if not request.user.is_staff:
        raise Http404

    if request.method == 'POST':
        form = PeriodicalForm(request.POST)
        if form.is_valid():
            language = get_object_or_404(Language, short_code=form.cleaned_data['language'])
            category = get_object_or_404(Category, slug=form.cleaned_data['category'])
            periodical = Periodical.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                category=category,
                language=language,
                publisher=form.cleaned_data['publisher'],
                tags = form.cleaned_data['tags'],
                created_by=request.user,
                updated_by=request.user,
            )
            messages.add_message(request, messages.SUCCESS, 'New periodical added.')
            return redirect(periodical.get_absolute_url())
    else:
        form = BookDetailForm()

    context = {
        'form': form,
    }
    return render(request, 'items/add-periodical.html', context)


def list_periodicals(request):
    """View to list all periodicals."""

    periodicals = Periodical.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(periodicals, 10)
    try:
        periodicals = paginator.page(page)
    except PageNotAnInteger:
        periodicals = paginator.page(1)
    except EmptyPage:
        periodicals = paginator.page(paginator.num_pages)

    return render(request, 'items/list-periodicals.html', {'periodicals': periodicals})


def view_periodical(request, id):
    """View to display periodical details."""

    periodical = get_object_or_404(Periodical, id=id)
    return render(request, 'items/view-periodical.html', {'periodical': periodical})


@login_required
def edit_periodical(request, id):
    """View to edit a periodical."""

    if not request.user.is_staff:
        raise Http404
    periodical = get_object_or_404(Periodical, id=id)

    if request.method == 'POST':
        form = PeriodicalForm(request.POST)
        if form.is_valid():
            language = get_object_or_404(Language, short_code=form.cleaned_data['language'])
            category = get_object_or_404(Category, slug=form.cleaned_data['category'])
            periodical.title = form.cleaned_data['title']
            periodical.description = form.cleaned_data['description']
            periodical.category = category
            periodical.language = language
            periodical.publisher = form.cleaned_data['publisher']
            periodical.tags = form.cleaned_data['tags']
            periodical.updated_by = request.user
            periodical.save()
            messages.add_message(request, messages.SUCCESS, 'Details updated.')
            return redirect(periodical.get_absolute_url())
    else:
        form = PeriodicalForm()

    context = {
        'form': form,
        'periodical': periodical,
    }
    return render(request, 'items/edit-periodical.html', context)


@login_required
def delete_periodical(request, id):
    """View to delete a periodical."""

    if not request.user.is_staff:
        raise Http404
    periodical = get_object_or_404(Periodical, id=id)

    if PeriodicalIssue.objects.filter(periodical=periodical).exists():
        messages.add_message(request, messages.ERROR, 'Unable to delete. Periodical issues exists.')
        return redirect(periodical.get_absolute_url())

    periodical.delete()
    return redirect(reverse('items:list_periodicals'))


@login_required
def add_periodical_issue(request, periodical_id):
    """View to add a periodical issue."""

    if not request.user.is_staff:
        raise Http404
    periodical = get_object_or_404(Periodical, id=periodical_id)

    if request.method == 'POST':
        form = PeriodicalIssueForm(request.POST)
        if form.is_valid():
            periodical_issue = PeriodicalIssue.objects.create(
                periodical=periodical,
                issue_status=form.cleaned_data['issue_status'],
                remarks=form.cleaned_data['remarks'],
                published_on=form.cleaned_data['published_on'],
                volume=form.cleaned_data['volume'],
                issue=form.cleaned_data['issue'],
                tags=form.cleaned_data['tags'],
                created_by=request.user,
                updated_by=request.user,
            )
            messages.add_message(request, messages.SUCCESS, 'New periodical added')
            return redirect(periodical_issue.get_absolute_url())
    else:
        form = PeriodicalIssueForm()

    context = {
        'form': form,
        'periodical': periodical,
    }
    return render(request, 'items/add-periodical-issue.html', context)


def list_periodical_issues(request, periodical_id):
    """View to list all periodicals."""

    periodical = get_object_or_404(Periodical, id=periodical_id)
    periodical_issues = PeriodicalIssue.objects.filter(periodical=periodical).order_by('-published_on')
    page = request.GET.get('page')
    paginator = Paginator(periodical_issues, 10)
    try:
        periodical_issues = paginator.page(page)
    except PageNotAnInteger:
        periodical_issues = paginator.page(1)
    except EmptyPage:
        periodical_issues = paginator.page(paginator.num_pages)

    context = {
        'periodical_issues': periodical_issues,
        'periodical': periodical,
    }
    return render(request, 'items/list-periodical-issues.html', context)


def view_periodical_issue(request, periodical_id, issue_id):
    """View to display book copy details."""

    periodical = get_object_or_404(Periodical, id=periodical_id)
    periodical_issue = get_object_or_404(PeriodicalIssue, periodical=periodical, id=issue_id)

    context = {
        'periodical': periodical,
        'periodical_issue': periodical_issue,
    }
    return render(request, 'items/view-periodical-issue.html', context)


@login_required
def edit_periodical_issue(request, periodical_id, issue_id):
    """View to edit book copy details."""

    if not request.user.is_staff:
        raise Http404
    periodical = get_object_or_404(Periodical, id=periodical_id)
    periodical_issue = get_object_or_404(PeriodicalIssue, periodical=periodical, id=issue_id)

    if request.method == 'POST':
        form = PeriodicalIssueForm(request.POST)
        if form.is_valid():
            periodical_issue.issue_status = form.cleaned_data['issue_status']
            periodical_issue.remarks = form.cleaned_data['remarks']
            periodical_issue.published_on = form.cleaned_data['published_on']
            periodical_issue.volume = form.cleaned_data['volume']
            periodical_issue.issue = form.cleaned_data['issue']
            periodical_issue.tags = form.cleaned_data['tags']
            periodical_issue.updated_by = request.user
            periodical_issue.save()

            messages.add_message(request, messages.SUCCESS, 'Details updated')
            return redirect(periodical_issue.get_absolute_url())
    else:
        form = PeriodicalIssueForm()

    context = {
        'form': form,
        'periodical': periodical,
        'periodical_issue': periodical_issue,
    }
    return render(request, 'items/edit-periodical-issue.html', context)


@login_required
def delete_periodical_issue(request, periodical_id, issue_id):
    """View to delete book copy."""

    if not request.user.is_staff:
        raise Http404
    periodical = get_object_or_404(Periodical, id=periodical_id)
    periodical_issue = get_object_or_404(PeriodicalIssue, periodical=periodical, id=issue_id)
    periodical_issue.delete()
    messages.add_message(request, messages.SUCCESS, 'Periodical issue deleted')
    return redirect(reverse('items:list_periodical_issues', kwargs={'periodical_id': periodical_id}))
