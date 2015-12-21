from datetime import  timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import BookCirculation
from items.models import BookCopy
from .forms import CirculationForm, CirculationConfirmForm, ReturnForm, ReturnConfirmForm
from accounts.helpers import is_staff
from livre.config import MAX_CIRCULATION_DAYS


@login_required
@user_passes_test(is_staff)
def circulations(request):
    """View to list the circulations.

    filter parameter can be passed through GET data.
    """

    if request.GET.get('filter') == 'on-circulation':
        circulations_list = BookCirculation.objects.filter(is_returned=False)
        filter = 'on-circulation'
    elif request.GET.get('filter') == 'due':
        circulations_list = BookCirculation.objects.filter(is_returned=False, due_date__lt=timezone.now().date())
        filter = 'due'
    else:
        circulations_list = BookCirculation.objects.all()
        filter = 'all'

    paginator = Paginator(circulations_list, 50)
    try:
        circulations_list = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        circulations_list = paginator.page(1)
    except EmptyPage:
        circulations_list = paginator.page(paginator.num_pages)

    context = {
        'filter': filter,
        'circulations_list': circulations_list,
    }
    return render(request, 'circulations/circulations.html', context)


@login_required
@user_passes_test(is_staff)
def add_circulation(request):
    """View to issue a book to a user.

    Redirects to confirmation view if username and book id are valid.
    """

    if request.method == 'POST':
        form = CirculationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
                book_copy = BookCopy.objects.get(id=form.cleaned_data['book_id'])
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Invalid username')
            except BookCopy.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Invalid book id')
            else:
                if book_copy.book_status is not 1:
                    messages.add_message(request, messages.ERROR, 'This book is not available for circulation.')
                else:
                    return redirect("{}?user={}&book={}".format(reverse('circulations:add_circulation_confirm'),
                                                                user.id, book_copy.id))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid details')
    else:
        form = CirculationForm()

    return render(request, 'circulations/add-circulation.html', {'form': form})


@login_required
@user_passes_test(is_staff)
def add_circulation_confirm(request):
    """View to confirm a new circulation."""

    user = get_object_or_404(User, id=request.GET.get('user'))
    book_copy = get_object_or_404(BookCopy, id=request.GET.get('book'))

    if request.method == 'POST':
        form = CirculationConfirmForm(request.POST)
        if form.is_valid():
            issued_on = form.cleaned_data['issued_on']
            due_date = form.cleaned_data['due_date']

            if due_date < issued_on:
                messages.add_message(request, messages.ERROR, 'Due date should not be before issue date.')
            elif book_copy.book_status is not 1 or BookCirculation.objects.filter(book_copy=book_copy,
                                                                                   is_returned=False).exists():
                messages.add_message(request, messages.ERROR, 'This book is not available for circulation.')
            else:
                BookCirculation.objects.create(
                    book_copy=book_copy,
                    user=user,
                    issued_on=issued_on,
                    issued_by=request.user,
                    due_date=due_date,
                )
                book_copy.book_status = 2
                book_copy.save()
                messages.add_message(request, messages.SUCCESS, 'New book circulation added.')
                return redirect(reverse('circulations:add_circulation'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid dates')
    else:
        form = CirculationConfirmForm()

    context = {
        'book_copy': book_copy,
        'issue_user': user,
        'form': form,
        'issued_on': timezone.now().date(),
        'due_date': timezone.now().date()+timedelta(days=MAX_CIRCULATION_DAYS),
    }
    return render(request, 'circulations/add-circulation-confirm.html', context)


@login_required
@user_passes_test(is_staff)
def return_circulation(request):
    """View to return a book in circulation.

    Redirects to confirm page is book id is valid.
    """

    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            if BookCirculation.objects.filter(book_copy=form.cleaned_data['book_id'], is_returned=False).exists():
                return redirect('{}?book={}'.format(reverse('circulations:return_circulation_confirm'),
                                                    form.cleaned_data['book_id']))
            else:
                messages.add_message(request, messages.ERROR, 'This book is not in circulation.')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid book ID.')
    else:
        form = ReturnForm()

    return render(request, 'circulations/return-circulation.html', {'form': form})


@login_required
@user_passes_test(is_staff)
def return_circulation_confirm(request):
    """View to confirm book circulation."""

    book_copy = get_object_or_404(BookCopy, id=request.GET.get('book'))
    book_circulation = get_object_or_404(BookCirculation, book_copy=book_copy, is_returned=False)

    if request.method == 'POST':
        form = ReturnConfirmForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['returned_on'] < book_circulation.issued_on:
                messages.add_message(request, messages.ERROR, 'Return date should not be before issue date.')
            else:
                book_circulation.returned_on = form.cleaned_data['returned_on']
                book_circulation.returned_by = request.user
                book_circulation.is_returned = True
                book_circulation.save()
                messages.add_message(request, messages.SUCCESS, 'Success.')
                return redirect(reverse('circulations:return_circulation'))
    else:
        form = ReturnConfirmForm()

    context = {
        'form': form,
        'book_copy': book_copy,
        'book_circulation': book_circulation,
        'return_date': timezone.now().date(),
    }
    return render(request, 'circulations/return-circulation-confirm.html', context)
