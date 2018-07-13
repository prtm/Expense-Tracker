# core django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404

# project
from .forms import ExpenseForm


@login_required
def dashboard(request):
    # add expense logic
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES or None)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            photo = form.cleaned_data['photo']
            if photo:
                file_type = expense.photo.url.split('.')[-1]
                file_type = file_type.lower()
                # python-magic library required to check correct mime type
                if file_type not in ['png', 'jpg']:
                    form.add_error('photo', 'Image format must be png or jpg')
                else:
                    expense.save()
            else:
                expense.save()
    elif request.method == "DELETE":
        uid = request.DELETE.get('uid')
        pass
    else:
        form = ExpenseForm()
    return render(request, 'expense_manager/dashboard/dashboard.html', {'form': form})
