# core django
from django import forms


# user registration form

class UserRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
    username = forms.CharField(max_length=254)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, max_length=32)
