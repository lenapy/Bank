from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from datetime import datetime, timedelta


from bank.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    login = models.CharField(max_length=50, unique=True)
    date_of_birth = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    about_user = models.TextField(null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/')
    level_points = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = ('username', 'email')
    USERNAME_FIELD = 'login'

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return '{} {}'.format(self.username, self.surname)

    def get_short_name(self):
        return self.username

    @property
    def is_auth(self, request):
        user_session = request['user-session']
        session = Session.objects.filter(token=user_session).last()
        if session:
            return True


class Card(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=6, null=True, blank=True)

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

admin.site.register(User)
admin.site.register(Card)
admin.site.register(Achievement)
admin.site.register(AchievementResource)
admin.site.register(AchievementLabel)
admin.site.register(Observer)
