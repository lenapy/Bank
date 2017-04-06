from django import forms
from bank.models import Achievement, Card


class AchievementForm(forms.Form):
    name = forms.CharField(max_length=50, initial='')
    text = forms.CharField(widget=forms.Textarea, initial='')
    card = forms.ModelChoiceField(queryset=Card.objects.all(),
                                  empty_label="Выберите карточку")

    def clean(self):

        cleaned_data = super().clean()
        name= cleaned_data['name']
        text = cleaned_data['text']
        card = cleaned_data['card']
        return cleaned_data


class CardFormName(forms.Form):

    name = forms.CharField(max_length=50, initial='')

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        return cleaned_data

