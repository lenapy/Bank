from django.shortcuts import render, redirect, get_object_or_404

from bank.achievement.forms import AchievementForm, CardForm
from bank.models import Achievement, Card


def card_new(request):
    if request.method == 'POST':
        form = CardForm(data=request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('user:profile')
    else:
        form = CardForm()
    return render(request, 'achievement/achievement_edit.html', context={'form': form})


def card_edit(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = CardForm(data=request.POST, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('user:profile')
    else:
        form = CardForm(instance=card)
    return render(request, 'achievement/card_edit.html', context={'form': form})


def achievement_new(request):
    if request.method == 'POST':
        form = AchievementForm(data=request.POST)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.user = request.user
            achievement.save()
            return redirect('user:profile')
    else:
        form = AchievementForm()
    return render(request, 'achievement/achievement_edit.html', context={'form': form})


def achievement_edit(request, pk):
        achievement = get_object_or_404(Achievement, pk=pk)
        if request.method == "POST":
            form = AchievementForm(request.POST, instance=achievement)
            if form.is_valid():
                achievement = form.save(commit=False)
                achievement.user = request.user
                achievement.save()
                return redirect('user:profile')
        else:
            form = AchievementForm(instance=achievement)
        return render(request, 'achievement/achievement_edit.html', {'form': form})



