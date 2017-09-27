from django import forms
from bank.models import Blog


class BlogFormPost(forms.Form):

    post = forms.CharField(widget=forms.Textarea, initial='')
    name = forms.CharField(max_length=50, initial='')

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        post = cleaned_data['post']
        # if Blog.objects.filter(name=name).first():
        #     raise forms.ValidationError('Such title as %s already exist' % name)
        return cleaned_data


class CommentFormPost(forms.Form):
    text = forms.CharField(widget=forms.Textarea, initial='')

    def text_clean(self):
        cleaned_data = super().clean()
        text = cleaned_data['text']
        if text:
            return cleaned_data
        else:
            raise forms.ValidationError('Пустой комментарий')
