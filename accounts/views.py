from hashlib import md5

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError

from .models import UserProfile
from circulations.models import BookCirculation
from .forms import LoginForm, ProfileForm, AddUserForm, RemoveUserForm, RegisterForm
from .helpers import is_staff, is_admin
from livre.config import ALLOW_USER_REGISTRATION


def login_user(request):
    """ View to log user in
    """

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    try:
                        return redirect(request.GET.get('next'))
                    except:
                        return redirect(reverse('index'))

            messages.add_message(request, messages.ERROR, "Incorrect username password combination.")
    else:
        form = LoginForm()

    context = {
        'form': form,
        'page': 'account',
        'next': request.GET.get('next'),
    }
    return render(request, 'accounts/login.html', context)


def register(request):
    """ View to register a normal user account.
    """

    if not ALLOW_USER_REGISTRATION:
        return render(request, 'accounts/registration-not-allowed.html')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username'].lower()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password == confirm_password:
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )
                except IntegrityError:
                    messages.add_message(request, messages.ERROR, "This username is not available.")
                else:
                    messages.add_message(request, messages.SUCCESS,
                                         "Registration successful. Please log in to continue")
                    return redirect(reverse('login'))
            else:
                messages.add_message(request, messages.ERROR, "Password do not match. Please check.")
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


@login_required
def profile(request):
    """View to display user profile."""

    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
        'gravathar_hash': md5(request.user.email.encode()).hexdigest(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """View to edit user profile."""

    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

            user_profile.gender = form.cleaned_data['gender']
            user_profile.email = form.cleaned_data['email']
            user_profile.birthday = form.cleaned_data['birthday']
            user_profile.phone = form.cleaned_data['phone']
            user_profile.city = form.cleaned_data['city']
            user_profile.state = form.cleaned_data['state']
            user_profile.country = form.cleaned_data['country']
            user_profile.zip_code = form.cleaned_data['zip_code']
            user_profile.save()

            messages.add_message(request, messages.SUCCESS, 'Details Updated')
        else:
            messages.add_message(request, messages.ERROR, 'There were errors. Please check')
    else:
        form = ProfileForm()

    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/edit-profile.html', context)


@login_required
@user_passes_test(is_staff)
def add_user(requst):
    """View to add a new user."""

    if requst.method == 'POST':
        form = AddUserForm(requst.POST)
        if form.is_valid():
            try:
                User.objects.create_user(
                    username=form.cleaned_data['username'].lower(),
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                )
                messages.add_message(requst, messages.SUCCESS, 'User added.')
                return redirect(reverse('accounts:list_users'))
            except IntegrityError:
                messages.add_message(requst, messages.ERROR, 'Username already exists.')
    else:
        form = AddUserForm()

    return render(requst, 'accounts/add-user.html', {'form': form})


@login_required
@user_passes_test(is_staff)
def list_users(request):
    """View to show all users."""

    users = User.objects.all()
    paginator = Paginator(users, 50)
    try:
        users = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'accounts/list-users.html', {'users': users})


@login_required
@user_passes_test(is_staff)
def view_user_profile(request, username):
    """View to display a user profile."""

    user_detail = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user_detail)

    context = {
        'user_detail': user_detail,
        'user_profile': user_profile,
        'is_admin': is_admin(user=request.user),
    }
    return render(request, 'accounts/view-user-profile.html', context)


@login_required
@user_passes_test(is_staff)
def remove_user(request, username):
    """View to remove a user."""

    user_detail = User.objects.get(username=username)

    if request.method == 'POST':
        form = RemoveUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['username'] == user_detail.username:
                user_detail.delete()
                messages.add_message(request, messages.SUCCESS, 'User removed.')
                return redirect(reverse('accounts:list_users'))
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username.')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username.')
    else:
        form = RemoveUserForm()

    return render(request, 'accounts/remove-user.html', {'form': form, 'user_detail': user_detail})


@login_required
@user_passes_test(is_admin)
def change_staff_status(request, username):
    """View to change the is_staff field in user model."""

    user_detail = User.objects.get(username=username)

    if user_detail.is_superuser:
        messages.add_message(request, messages.ERROR, "This user is an admin. Please remove from admins first.")
    else:
        user_detail.is_staff = not user_detail.is_staff
        user_detail.save()
        messages.add_message(request, messages.SUCCESS, "Status updated.")

    return redirect(reverse('accounts:view_user_profile', kwargs={'username': username}))


@login_required
@user_passes_test(is_admin)
def change_admin_status(request, username):
    """View to change the is_superuser field in user model."""

    user_detail = User.objects.get(username=username)

    if user_detail.username == request.user.username:
        messages.add_message(request, messages.ERROR, "You cannot update your status.")
    else:
        user_detail.is_superuser = not user_detail.is_superuser
        user_detail.is_staff = user_detail.is_superuser
        user_detail.save()
        messages.add_message(request, messages.SUCCESS, "Status updated.")

    return redirect(reverse('accounts:view_user_profile', kwargs={'username': username}))


@login_required
def my_books(request):
    """View to display all books issued to a user."""

    circulations = BookCirculation.objects.filter(user=request.user)
    paginator = Paginator(circulations, 50)
    try:
        circulations = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        circulations = paginator.page(1)
    except EmptyPage:
        circulations = paginator.page(paginator.num_pages)

    return render(request, 'accounts/my-books.html', {'circulations': circulations})
