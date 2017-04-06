from django.shortcuts import render, redirect

from bank.achievement.forms import AchievementForm, CardFormName
from bank.models import Achievement, Card


def card_new(request):
    if request.method == 'POST':
        form = CardFormName(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            new_card = Card.objects.create(name=name, user_id=request.user.id)
            new_card.save()
            return redirect('user:profile')
    else:
        form = CardFormName()
    return render(request, 'achievement/card_edit.html', context={'form': form})


def card_edit(request, pk):
    card = Card.objects.get(pk=pk)
    data = {'name': card.name}
    if request.method == 'POST':
        form = CardFormName(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            card.name = name
            card.save()
            return redirect('user:profile')
    else:
        form = CardFormName(data)
    return render(request, 'achievement/card_edit.html', context={'form': form})


def add_color_to_card(request, pk, color):
            card = Card.objects.filter(pk=pk)
            card.update(color=color)
            return redirect('user:profile')


def achievement_new(request):
    cards = Card.objects.all()
    if request.method == 'POST':
        form = AchievementForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            card_id = form.cleaned_data['card']
            achievement = Achievement.objects.create(name=name,
                                                     text=text,
                                                     card=card_id)
            achievement.save()
            return redirect('user:profile')
    else:
        form = AchievementForm()
    return render(request, 'achievement/achievement_edit.html', context={'form': form,
                                                                         'cards': cards})


def achievement_edit(request, pk):
        achievement = Achievement.objects.get(pk=pk)
        cards = Card.objects.all()
        data = {
                'name': achievement.name,
                'text': achievement.text
        }
        if request.method == "POST":
            form = AchievementForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                text = form.cleaned_data['text']
                card_id = form.cleaned_data['card']
                achievement.name = name
                achievement.text = text
                achievement.card_id = card_id
                achievement.save()
                return redirect('user:profile')
        else:
            form = AchievementForm(data)
        return render(request, 'achievement/achievement_edit.html', {'form': form,
                                                                     'cards': cards})



