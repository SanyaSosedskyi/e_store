from django.db import models
from django.contrib.auth.models import User
from django.core import validators


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,
                             validators=[validators.RegexValidator(
                                 regex=r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')])

    def __str__(self):
        return 'id_' + str(self.user.id) + ' ' + self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
