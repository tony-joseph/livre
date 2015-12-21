from django import forms


class CirculationForm(forms.Form):
    username = forms.SlugField(label='Username:', max_length=32, min_length=4, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username', 'required': 'required', }))
    book_id = forms.IntegerField(label='Book ID:', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Book ID', 'required': 'required', }))


class CirculationConfirmForm(forms.Form):
    issued_on = forms.DateField(label='Issued date:', widget=forms.DateInput(attrs={
        'class': 'form-control', 'placeholder': 'Issue date', 'required': 'required', }))
    due_date = forms.DateField(label='Due date:', widget=forms.DateInput(attrs={
        'class': 'form-control', 'placeholder': 'Due date', 'required': 'required', }))


class ReturnForm(forms.Form):
    book_id = forms.IntegerField(label='Book ID:', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Book ID', 'required': 'required', }))


class ReturnConfirmForm(forms.Form):
    returned_on = forms.DateField(label='Return date:', widget=forms.DateInput(attrs={
        'class': 'form-control', 'placeholder': 'Return date', 'required': 'required', }))
