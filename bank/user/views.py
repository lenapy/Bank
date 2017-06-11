from django.shortcuts import render, redirect
import uuid
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bank.user.forms import RegistrationForm, LoginForm, \
    PasswordChangeForm, ImageUploadForm, UserEditForm, AddInfoAboutUser
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
    users = User.objects.all()
    cards = Card.objects.filter(user=request.user).order_by('update_data')
    paginator = Paginator(cards, 3)
    page = request.GET.get('page')
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        cards = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        cards = paginator.page(paginator.num_pages)
    achievements = Achievement.objects.all().order_by('update_data')
    cards_dict = Card.objects.values().filter(user=request.user)
    ach_dict = Achievement.objects.values().filter(card__user=request.user)
    data = []
    data.extend(cards_dict.reverse())
    data.extend(ach_dict.reverse())

    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if data[i]['update_data'] < data[j]['update_data']:
                data[i], data[j] = data[j], data[i]

    return render(request, 'user/profile.html', {'users': users, 'cards': cards,
                                                 'achievements': achievements,
                                                 'data': data[:10]})


def upload_photo(request):
    if request.method == 'POST':
        form = ImageUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            User.objects.upload_avatar(image, request.user.id)
            return redirect('user:profile')
    else:
        form = ImageUploadForm()
    return render(request, 'user/profile.html', {'form': form})


def user_edit(request, pk):
    user = User.objects.get(pk=pk)
    data = {'username': user.username, 'surname': user.surname,
            'date_of_birth': user.date_of_birth,
            'phone_number': user.phone_number,
            'email': user.email,
            'about_user': user.about_user}
    if request.method == 'POST':
        form = UserEditForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            surname = form.cleaned_data['surname']
            date_of_birth = form.cleaned_data['date_of_birth']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            about_user = form.cleaned_data['about_user']
            User.objects.change_user_data(pk, username, surname, date_of_birth,
                                          phone_number, email, about_user)
            return redirect('user:profile')
    else:
        form = UserEditForm(data)
    return render(request, 'user/edit.html', context={'form': form})


def user_add_info(request, pk):
    if request.method == 'POST':
        form = AddInfoAboutUser(data=request.POST)
        if form.is_valid():
            about_user = form.cleaned_data['about_user']
            User.objects.add_info(about_user, pk)
            return redirect('user:profile')
        else:
            pass
    else:
        form = AddInfoAboutUser()
    return render(request, 'user/add_info.html', context={'form': form})
