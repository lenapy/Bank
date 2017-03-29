from django import forms
from bank.models import Achievement, Card


class AchievementForm(forms.ModelForm):
        class Meta:
            model = Achievement
            fields = ('name', 'text', 'card')


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('name', 'color')
