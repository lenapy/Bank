from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from datetime import datetime, timedelta

from bank.managers import UserManager, BlogManager, CommentManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    login = models.CharField(max_length=50, unique=True)
    date_of_birth = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    about_user = models.TextField(null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    avatar = models.ImageField()
    level_points = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = ('username', 'email')
    USERNAME_FIELD = 'login'

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

    def get_full_name(self):
        pass

    def get_short_name(self):
        pass

    def get_url_avatar(self):
        path = self.avatar.path
        url = (path.partition('Bank/bank'))[2]
        return url


class Card(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, null=True, blank=True)
    update_data = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'card'

    def __str__(self):
        return self.name


class Achievement(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    update_data = models.DateTimeField(auto_now=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    class Meta:
        db_table = 'achievement'

    def __str__(self):
        return self.name


class AchievementResource(models.Model):
    resource_id = models.IntegerField(auto_created=True)
    resource_type = models.IntegerField(choices=(
        (1, 'file'),
        (2, 'link')))
    update_data = models.DateTimeField(auto_now=True)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    class Meta:
        db_table = 'achievement_resource'

    def __str__(self):
        return '{}, {}'.format(self.resource_type, self.achievement)


class Links(models.Model):
    link = models.URLField()
    achievement_resource = models.ForeignKey(AchievementResource, on_delete=models.CASCADE)

    class Meta:
        db_table = 'link'

    def __str__(self):
        return '{}, {}'.format(self.link, self.achievement_resource)


class File(models.Model):
    file = models.FileField(upload_to='resource/%Y/%m/%d/')
    achievement_resource = models.ForeignKey(AchievementResource, on_delete=models.CASCADE)

    class Meta:
        db_table = 'file'


class Label(models.Model):
    text = models.CharField(max_length=30)
    color = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        db_table = 'label'

    def __str__(self):
        return '{}'.format(self.text)


class AchievementLabel(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    class Meta:
        db_table = 'achievement_label'

    def __str__(self):
        return '{}, {}, {}'.format(self.label, self.user, self.achievement)


class Observer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    class Meta:
        db_table = 'observer'

    def __str__(self):
        return '{}, {}'.format(self.user, self.card)


class Session(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=36)
    date_expired = models.DateTimeField(default=datetime.now() + timedelta(days=7))

    class Meta:
        db_table = 'session'


class Blog(models.Model):
    user = models.ForeignKey(User)
    post = models.TextField()
    name = models.CharField(max_length=50)
    edit_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = BlogManager()

    class Meta:
        db_table = 'blog'


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    class Meta:
        db_table = 'comment'


