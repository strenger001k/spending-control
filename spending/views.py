from dateutil.relativedelta import relativedelta

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.utils import timezone

from spending.models import Spending
from spending.form import CreateSpendingForm
from spending.constants import SpendingCategory
from spending.statistics import StatisticsService


def index(requests):
    return HttpResponse("Hello, world. You're at the polls index.")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_list')
        else:
            messages.success(request, ('Помилка'))
            return redirect('login_user')
    else:
        return render(request, 'login_user.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('Logout'))
    return redirect('login_user')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('user_list')
    else:
        form = UserCreationForm()

    return render(request, 'register_user.html', {'form': form})


def UserListView(request):
    model = Spending.objects.filter(create_by=request.user)
    category = {}
    category['0'] = "Усі категорії"
    for value, label in zip(SpendingCategory.values, SpendingCategory.labels):
        category[value] = label

    query = request.GET.get('q', None)
    if query and query != '0':
        model = Spending.objects.filter(create_by=request.user, category=query)

    return render(request, 'user_list.html', {'users': model,
                                              'category': category})


def StatisticsView(request):
    now_date = timezone.now()
    category_all_time = {}
    price = {}

    category_today, price['today'] = StatisticsService(request.user,
                                                       now_date-relativedelta(days=1),
                                                       now_date).run()

    category_month, price['month'] = StatisticsService(request.user,
                                                       now_date-relativedelta(months=1),
                                                       now_date).run()

    category_year, price['year'] = StatisticsService(request.user,
                                                     now_date-relativedelta(years=1),
                                                     now_date).run()

    category_all_time, price['all_time'] = StatisticsService(request.user).run()
    print(category_all_time)
    return render(request, 'statistics.html', {'category_today': category_today,
                                               'category_month': category_month,
                                               'category_year': category_year,
                                               'category_all_time': category_all_time,
                                               'price': price})


class UserCreateView(View):
    def get(self, request):
        form = CreateSpendingForm()
        return render(request, 'user_create.html', {'form': form})

    def post(self, request):
        form = CreateSpendingForm(request.POST)
        if form.is_valid():
            spend = form.save(request.user)
            return redirect('user_list')
        return render(request, 'user_create.html', {'form': form})


class UserUpdateView(UpdateView):
    model = Spending
    context_object_name = 'user'
    template_name = 'user_update.html'
    fields = ['name', 'price', 'category', 'comment', 'date']
    success_url = reverse_lazy('user_list')


class UserDeleteView(DeleteView):
    model = Spending
    context_object_name = 'user'
    template_name = 'user_delete.html'
    success_url = reverse_lazy('user_list')


def delete_all_data(request):
    Spending.objects.filter(create_by=request.user).delete()
    return redirect('user_list')
