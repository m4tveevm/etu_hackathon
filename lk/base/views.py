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
from .logic import foreign_lk, kudago_api
from .forms import UserProfileForm
from django.shortcuts import render, redirect
from .models import UserProfile


@login_required(login_url='login')
def home(request):
    try:
        items = [
            {"title": "Название события", "price": '10', "place": '10', "tags": '1',
             "time": "time",
             'maps': 'https://yandex.ru/maps/2/saint-petersburg/?mode=routes&rtext=~59.971716%2C30.321735'},
            {"title": "Название события", "price": '10', "place": '10', "tags": '1',
             "time": "time",
             'maps': 'https://yandex.ru/maps/2/saint-petersburg/?mode=routes&rtext=~59.971716%2C30.321735'},
        ]
        context = {"list_events": items}
        return render(request, 'base/index.html', context=context)
    except UserProfile.DoesNotExist:
        return redirect('profile/')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm


@login_required
def lk_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    context = {'form': form}
    return render(request, 'base/profile.html', context)


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
