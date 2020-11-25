from django.contrib.auth import login, logout, authenticate
from django.db import transaction
from django.shortcuts import render, redirect

from pythons_auth.forms import RegisterForm, ProfileForm, LoginForm


@transaction.atomic
def register_user(request):
    if request.method == 'GET':
        context = {
            'user_form': RegisterForm(),
            'profile_form': ProfileForm(),
        }
        return render(request, 'auth/register.html', context)
    user_form = RegisterForm(request.POST)
    profile_form = ProfileForm(request.POST, request.FILES)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        login(request, user)
        return redirect('index')

    context = {
        'user_form': RegisterForm(),
        'profile_form': ProfileForm(),
    }
    return render(request, 'auth/register.html', context)


def login_user(request):
    if request.method == 'GET':
        context = {
            'login_form': LoginForm(),
        }
        return render(request, 'auth/login.html', context)
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
    context = {
        'login_form': login_form,
    }
    return render(request, 'auth/login.html', context)


def get_redirect_url(params):
    redirect_url = params.get('return_url')
    return redirect_url if redirect_url else 'index'


@login_user
def logout_user(request):
    logout(request)
    return redirect('index')
