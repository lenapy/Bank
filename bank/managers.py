from django.db import models
from django.contrib.auth.hashers import make_password


class UserManager(models.Manager):

    def registration(self, login, password, username, surname, email):  # self - model
        password_hash = make_password(password, hasher='md5')
        user = self.create(login=login,
                           password=password_hash,
                           username=username,
                           surname=surname,
                           email=email)
        user.save()
        return user.pk

    def change_password(self, password):
        password_hash = make_password(password, hasher='md5')
        self.update(password=password_hash)


