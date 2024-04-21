from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import UserProfile
# from .models import Course, Lesson, Material, Task, TaskType
from .logic import foreign_lk


@login_required(login_url='login')
def home(request):
    try:
        if not request.user.userprofile.etu_session_data:
            items = [
                {"title": "Название события", "price": '10', "place": '10', "tags": '1',
                 "time": "time"}
            ]
            context = {"list_events": items}
            return render(request, 'base/index.html', context=context)
        else:
            return redirect('admin/')
    except UserProfile.DoesNotExist:
        return redirect('admin/')


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except Exception as error:
            print(error)
            messages.error(request, 'Пользователь не существует')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                return redirect(request.GET.get('next', '/'), status=302)
            except Exception:
                return redirect('home', status=302)
        else:
            messages.error(request, 'Login ИЛИ password не верны')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    if request.method == "POST":
        firstname = request.POST.get('firstName').capitalize()
        lastname = request.POST.get('lastName').capitalize()
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            for message in e.messages:
                messages.error(request, message)
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Это имя пользователя уже занято.')
            return redirect('register')
        user = User.objects.create_user(username, email='', password=password, first_name=firstname,
                                        last_name=lastname)
        login(request, user)
        return redirect('/')
    return render(request, 'base/login_register.html')
