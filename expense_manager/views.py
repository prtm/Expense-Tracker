# stdlib
import json
import math
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
    datefilter = 1

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
        param_created = request.GET.get('created__range')
        param_date = request.GET.get('date')
        param_offset = request.GET.get('offset')
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

        if param_created:
            show_expense_tab = True
            if param_date:
                datefilter = param_date

        if param_offset:
            show_expense_tab = True

    # report summary
    total_expense = Expense.manager.total_expense(
        request.user, date.today().month,date.today().year)['total_expense']
    budget = Budget.objects.filter(
        user=request.user, month=date.today().month)
    if budget:
        budget = budget[0].get('budget')
    else:
        budget = 0
    remaining = total_expense - budget

    # all expenses including filter
    all_expenses = json.loads(resource.render_list(request))
    # all_expenses = Expense.manager.all_expenses(request.user)

    # top 10 including filter
    top_10 = Expense.manager.top_10_month_expenses(
        request.user, date.today().month, date.today().year)

    # pagination footer details
    offset = all_expenses['meta']['offset']

    total_page_number = math.ceil(
        all_expenses['meta']['total_count']/all_expenses['meta']['limit'])
    page_number = math.ceil(
        all_expenses['meta']['offset']/all_expenses['meta']['limit'])+1

    if page_number > total_page_number:
        page_number = total_page_number

    has_previous = (page_number != 1)
    has_next = (page_number != total_page_number)

    return render(request, 'expense_manager/dashboard/dashboard.html', {'form': form, 'top_10': top_10,
                                                                        'all_expenses': all_expenses.get('objects'),
                                                                        'total_expense': total_expense,
                                                                        'budget': budget,
                                                                        'month' : date.today().strftime("%B"),
                                                                        'remaining': budget-total_expense,
                                                                        'show_expense_tab': show_expense_tab,
                                                                        'imagefilter': imagefilter,
                                                                        "datefilter": datefilter,
                                                                        "offset": offset,
                                                                        "has_previous": has_previous,
                                                                        "has_next": has_next,
                                                                        "total_page_number": total_page_number,
                                                                        "page_number": page_number})

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
