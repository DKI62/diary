from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, ProfileUpdateForm, PasswordChangeCustomForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm


# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            send_mail(
                'Спасибо за регистрацию',
                'Спасибо за создание учётной записи на нашем сайте!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            login(request, user)  # Авторизация после регистрации
            return redirect('journal:entry_list')  # Перенаправление на страницу дневников
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


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeCustomForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('accounts:profile')  # Перенаправить на страницу профиля после обновления данных

        if 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Обновление сессии после смены пароля
                return redirect('accounts:profile')  # Перенаправить на страницу профиля после изменения пароля

    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeCustomForm(user=request.user)

    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })