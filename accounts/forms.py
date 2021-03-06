from django import forms

from .models import GENDER_CHOICES


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First name:', max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(label='Last name:', max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Last name'
    }))
    username = forms.SlugField(label='Username:', max_length=16, min_length=4, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
        'placeholder': 'Username'
    }))
    email = forms.EmailField(label='Email:', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }), required=False)
    password = forms.CharField(label='Password:', max_length=32, min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'password',
        'required': 'required',
    }))
    confirm_password = forms.CharField(label='Retype password:', max_length=32, min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password', 'required': 'required',}
    ))


class LoginForm(forms.Form):
    """ Form to handle login.
    """

    username = forms.SlugField(label='Username:', max_length=32, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username', 'required': 'required', }))
    password = forms.CharField(label='Password:', max_length=64, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password', 'required': 'required', }))


class ProfileForm(forms.Form):

    first_name = forms.CharField(label='First name*:', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'First name', 'required': 'required', }))
    last_name = forms.CharField(label='Last name*:', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Last name', 'required': 'required', }))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'}, choices=GENDER_CHOICES))
    email = forms.EmailField(label='Email:', required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email', }))
    birthday = forms.DateField(label='Birthday (YYYY-MM-DD):', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Birthday', }))
    phone = forms.CharField(label='Phone:', max_length=20, min_length=6, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone', }))
    city = forms.CharField(label='City:', max_length=150, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'City', }))
    state = forms.CharField(label='State:', max_length=150, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'State', }))
    country = forms.CharField(label='Country:', max_length=150, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Country', }))
    zip_code = forms.CharField(label='Zip code:', max_length=8, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Zip code', }))


class AddUserForm(forms.Form):
    first_name = forms.CharField(label='First name:', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'First name', 'required': 'required', }))
    last_name = forms.CharField(label='Last name:', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Last name', 'required': 'required', }))
    username = forms.SlugField(label='Username:', max_length=32, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username', 'required': 'required', }))
    password = forms.CharField(label='Password:', min_length=6, max_length=64, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password', 'required': 'required', }))


class RemoveUserForm(forms.Form):
    username = forms.SlugField(label='Username:', max_length=32, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username', 'required': 'required', }))
