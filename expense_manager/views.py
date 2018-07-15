# stdlib
import json
# import copy
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
from .resources import ExpenseResource


resource = ExpenseResource()


@login_required
def dashboard(request):
    show_expense_tab = None
    imagefilter = 1

    # add and update expense logic
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES or None)

        # validate form
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            photo = form.cleaned_data['photo']

            # if photo found then check extenstion for image file
            # in future check for signature using python-magic library
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

        # show expense tab if parameter found
        param_name = request.GET.get('name')
        param_price = request.GET.get('price')
        param_no_image = request.GET.get('photo')
        param_has_image = request.GET.get('photo__ne')
        if param_name or param_name == '' or param_price or param_price == '':
            show_expense_tab = True

        # show expense tab if parameter found
        # change image filter text if image filter applied on page refresh
        if param_no_image or param_no_image == '':
            show_expense_tab = True
            imagefilter = 2

        if param_has_image or param_has_image == '':
            show_expense_tab = True
            imagefilter = 3

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

    # all expenses including filter
    all_expenses = json.loads(resource.render_list(request)).get('objects')
    # all_expenses = Expense.manager.all_expenses(request.user)

    # top 10 including filter
    top_10 = Expense.manager.top_10_month_expenses(request.user)

    return render(request, 'expense_manager/dashboard/dashboard.html', {'form': form, 'top_10': top_10,
                                                                        'all_expenses': all_expenses,
                                                                        'total_expense': total_expense,
                                                                        'budget': budget,
                                                                        'remaining': budget-total_expense,
                                                                        'show_expense_tab': show_expense_tab,
                                                                        'imagefilter': imagefilter})

# upload image


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
