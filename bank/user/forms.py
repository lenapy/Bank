from django import forms
from django.contrib.auth.hashers import check_password
from bank.models import User


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=50, initial='')
    username = forms.CharField(max_length=50, initial='')
    surname = forms.CharField(max_length=50, initial='')
    email = forms.EmailField(initial='')
    password = forms.CharField(min_length=6, initial='')

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(login=login).first():
            raise forms.ValidationError('login %s already exist' % login)
        return login


class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, initial='')
    password = forms.CharField(min_length=6, initial='')

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data['login']
        password = cleaned_data['password']
        self.user = User.objects.filter(login=login).first()
        if not (self.user and check_password(password, self.user.password)):
            raise forms.ValidationError('Incorrect login or password')
        return login


class PasswordChangeForm(forms.Form):
    password = forms.CharField(min_length=6, initial='')
    new_password = forms.CharField(min_length=6, initial='')
    reenter_password = forms.CharField(min_length=6, initial='')

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data['password']
        new_password = cleaned_data['new_password']
        reenter_password = cleaned_data['reenter_password']
        if not (new_password == reenter_password or new_password != password):
            raise forms.ValidationError('Incorrect password')
        else:
            return cleaned_data


class ImageUploadForm(forms.Form):
    image = forms.ImageField()

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data['image']
        if image.size > 5242880:
            raise forms.ValidationError('Размер файла не должен привышать 5 Мб')
        return cleaned_data


class UserEditForm(forms.Form):
    username = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    date_of_birth = forms.CharField(max_length=50, required=False)
    phone_number = forms.IntegerField(required=False)
    about_user = forms.CharField(widget=forms.Textarea, initial='', required=False)
    email = forms.EmailField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        surname = cleaned_data['surname']
        date_of_birth = cleaned_data['date_of_birth']
        phone_number = cleaned_data['phone_number']
        email = cleaned_data['email']
        about_user = cleaned_data['about_user']
        return cleaned_data


class AddInfoAboutUser(forms.Form):
    about_user = forms.CharField(widget=forms.Textarea, initial='', required=False)

    def clean(self):
        cleaned_data = super().clean()
        about_user = cleaned_data['about_user']
        return cleaned_data
