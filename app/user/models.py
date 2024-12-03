from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Телефон обязателен для пользователя.')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class RefUser(AbstractUser):
    username = None
    email = None
    full_name = models.CharField(max_length=64, verbose_name='Имя и фамилий', blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=12, verbose_name='Телефон')

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number}'


class CodeAuth(models.Model):
    code = models.SmallIntegerField(verbose_name='Код')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    user = models.ForeignKey(RefUser, related_name='codes', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user.phone_number} - {self.code}'
