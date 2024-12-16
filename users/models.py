from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email address')
    phone = models.CharField(max_length=45, verbose_name='Phone number', blank=True)
    country = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='users/avatars/%(user_id)s/', verbose_name='Avatar', blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def __str__(self):
        return self.email




