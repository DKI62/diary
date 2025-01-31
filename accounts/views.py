from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm


# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get("password")
            user.set_password(password)  # Применяем хеширование пароля
            user.save()
            login(request, user)  # Входим в систему после регистрации
            return redirect('journal:entry_list')  # Перенаправляем на страницу записей
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Вход
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Авторизуем пользователя
            return redirect('journal:entry_list')  # Перенаправляем на страницу дневников
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# Выход
def user_logout(request):
    logout(request)
    return redirect('accounts:login')  # Перенаправляем на страницу входа
