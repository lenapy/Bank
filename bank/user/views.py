from django.shortcuts import render, redirect
import uuid

from bank.user.forms import RegistrationForm, LoginForm, PasswordChangeForm
from bank.models import User, Session, Card, Achievement


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            if not User.objects.registration(
                form.cleaned_data['login'],
                form.cleaned_data['password'],
                form.cleaned_data['username'],
                form.cleaned_data['surname'],
                form.cleaned_data['email']
            ):
                pass
            return redirect('user:login')
    else:
        form = RegistrationForm()
    return render(request, 'user/registration.html',
                  context={'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            session = Session.objects.create(user=form.user, token=uuid.uuid4())
            response = redirect('/')
            response.set_cookie('user-session', session.token,
                                expires=session.date_expired)
            return response
        else:
            pass

    else:
        form = LoginForm()

    return render(request, 'user/login.html', context={'form': form})


def logout(request):
    user_session = request.COOKIES['user-session']
    session = Session.objects.filter(token=user_session).last()
    if session.delete():
        return redirect('user:login')
    else:
        pass


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST)
        if form.is_valid():
            new_pass = form.cleaned_data['new_password']
            User.objects.change_password(new_pass, request.user.id)
            return redirect('user:login')
        else:
            pass
    else:
        form = PasswordChangeForm()
    return render(request, 'user/change_password.html', context={'form': form})


def profile(request):
    cards = Card.objects.filter(user=request.user).order_by('name')
    achievements = Achievement.objects.all().order_by('name')
    return render(request, 'user/profile.html', {'cards': cards,
                                                 'achievements': achievements})
