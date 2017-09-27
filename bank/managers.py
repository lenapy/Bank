import os
from django.db import models
from django.contrib.auth.hashers import make_password
from hashlib import md5
from django.conf import settings
import time

from bank import utils


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

    def change_password(self, password, user_id):
        password_hash = make_password(password, hasher='md5')
        user = self.filter(id=user_id)
        user.update(password=password_hash)

    def upload_avatar(self, file, user_id):
        user = self.filter(id=user_id)
        original_image_name, original_image_ext = os.path.splitext(file.name)
        m = md5(str('%s:%s' % (original_image_name, time.time())).encode())
        new_image_name = m.hexdigest()
        image_path = os.path.join(settings.UPLOAD_IMAGE_PATH, '%s%s' % (new_image_name, original_image_ext))
        if utils.handle_uploaded_file(file, image_path):
            user.update(avatar=image_path)

    def change_user_data(self, user_id, username, surname, date_of_birth, phone_number,
                         email, about_user):
        user = self.filter(id=user_id)
        user.update(username=username, surname=surname,
                    date_of_birth=date_of_birth, phone_number=phone_number, email=email, about_user=about_user)

    def add_info(self, info, user_id):
        user = self.filter(id=user_id)
        user.update(about_user=info)


class BlogManager(models.Manager):
    def crate_new_post(self, name, post, user):
        post = self.create(name=name,
                           post=post,
                           user_id=user)
        post.save()
        return post.pk

    def edit_post(self, post, name, text):
        post.name = name
        post.post = text
        post.save()

    def delete_post(self, post_id):
        post = self.get(pk=post_id)
        post.delete()


class CommentManager(models.Manager):
    def crate_new_comment(self, text, user, post):
        comment = self.create(text=text, user_id=user, post_id=post)
        comment.save()
        return comment.pk
