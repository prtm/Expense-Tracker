# stdlib
from datetime import date

# core django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage


# project
from .forms import ExpenseForm
from .models import Expense, Budget


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
    else:
        form = ExpenseForm()
    top_10 = Expense.manager.top_10_month_expenses(request.user)
    all_expenses = Expense.manager.all_expenses(request.user)[:10]

    # report summary
    total_expense = Expense.manager.total_expense(
        request.user, date.today().month)['total_expense']
    budget = Budget.objects.filter(
        user=request.user, month=date.today().month)
    if budget:
        budget = budget[0].get('budget')
    else:
        budget = 0
    remaining = total_expense - budget
    return render(request, 'expense_manager/dashboard/dashboard.html', {'form': form, 'top_10': top_10,
                                                                        'all_expenses': all_expenses,
                                                                        'total_expense': total_expense,
                                                                        'budget': budget,
                                                                        'remaining': budget-total_expense})


@login_required
def uploadImage(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        uploaded_file_url = fs.url(filename)
        return JsonResponse({
            'uploaded_file_url': uploaded_file_url[1:]
        })
    print(request.Files)
    return JsonResponse('Error Not Found!')
