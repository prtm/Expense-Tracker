# core django
from django import forms

# project
from .models import Expense


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Expense
        fields = ['name', 'price', 'photo']
