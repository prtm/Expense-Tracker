# stdlib
import json
import math
import os
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


# dashboard page with pagination, sort, search capabilities
@login_required
def dashboard(request):
    if request.method == "GET":
        show_expense_tab = None
        budget_id = -1
        imagefilter = 1
        datefilter = 1
        previous_page = None
        next_page = None

        form = ExpenseForm()

        # show expense tab if parameter found
        param_name = request.GET.get('name')
        param_price = request.GET.get('price')
        param_no_image = request.GET.get('photo')
        param_has_image = request.GET.get('photos')
        param_created = request.GET.get('created__range')
        param_date = request.GET.get('date')
        param_offset = request.GET.get('offset')
        param_orderby = request.GET.get('order_by')
        if param_name or param_name == '':
            show_expense_tab = True
            previous_page = "name="+param_name

        if param_price or param_price == '':
            show_expense_tab = True
            if previous_page:
                previous_page = "&price="+param_price
            else:
                previous_page = "price="+param_price

        # show expense tab if parameter found
        # change image filter text if image filter applied on page refresh
        if param_no_image or param_no_image == '':
            show_expense_tab = True
            imagefilter = 2
            if previous_page:
                previous_page = "&photo="
            else:
                previous_page = "photo="

        if param_has_image or param_has_image == '':
            show_expense_tab = True
            imagefilter = 3
            if previous_page:
                previous_page = "&photos=-1"
            else:
                previous_page = "photos=-1"

        if param_created:
            show_expense_tab = True
            if previous_page:
                previous_page = "&created__range="+param_created
            else:
                previous_page = "created__range="+param_created
            if param_date:
                datefilter = param_date

        if param_offset:
            show_expense_tab = True

        if param_orderby:
            show_expense_tab = True
            if previous_page:
                previous_page = "&order_by="+param_orderby
            else:
                previous_page = "order_by="+param_orderby

        # report summary
        total_expense = Expense.manager.total_expense(
            request.user, date.today().month, date.today().year)['total_expense']
        budget = Budget.objects.filter(
            user=request.user, month=date.today().month)
        if budget:
            budget_id = budget[0].pk
            budget = budget[0].budget
        else:
            budget = 0
        if not total_expense:
            total_expense = 0
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

        has_previous = (page_number != 1 and page_number != 0)
        has_next = (page_number != total_page_number)

        # next page & previous page url
        next_page = previous_page
        if previous_page:
            previous_page += "&offset=" + \
                (str(int(offset)-20) if (int(offset)-20) > 0 else "0")
            next_page += "&offset="+str(int(offset)+20)
        else:
            previous_page = "offset=" + \
                (str(int(offset)-20) if (int(offset)-20) > 0 else "0")
            next_page = "offset="+str(int(offset)+20)

        previous_page = "?"+previous_page
        next_page = "?"+next_page

        return render(request, 'expense_manager/dashboard/dashboard.html', {'form': form, 'top_10': top_10,
                                                                            'all_expenses': all_expenses.get('objects'),
                                                                            'total_expense': total_expense,
                                                                            'budget': budget,
                                                                            'budget_id': budget_id,
                                                                            'month': date.today().strftime("%B"),
                                                                            'remaining': budget-total_expense,
                                                                            'show_expense_tab': show_expense_tab,
                                                                            'imagefilter': imagefilter,
                                                                            "datefilter": datefilter,
                                                                            "previous_page": previous_page,
                                                                            "next_page": next_page,
                                                                            "has_previous": has_previous,
                                                                            "has_next": has_next,
                                                                            "total_page_number": total_page_number,
                                                                            "page_number": page_number,
                                                                            "username":request.user.username})
    else:
        return Http404('Error Not Found!')



# simple image upload
@login_required
def uploadImage(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']

        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        file_type = filename.split('.')[-1]
        file_type = file_type.lower()
        # [ Future changes ] python-magic library required to check correct mime type
        if file_type not in ['png', 'jpg']:
            os.remove(os.path.join(fs.location,filename))
            return JsonResponse({'error':'Image format must be png or jpg'}, status=400)
        # uploaded_file_url = fs.url(filename)
        return JsonResponse({
            'uploaded_file_url': filename
        })
    return JsonResponse({'error':'Error Not Found!'}, status=404)
