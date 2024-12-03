from django.db import models

from user.models import RefUser


class InviteCode(models.Model):
    code = models.CharField(max_length=7, unique=True, verbose_name='Инвайт код юзера')
    user = models.OneToOneField(RefUser, verbose_name='Юзер', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code} - {self.user.phone_number}'


class ActiveUserInviteCode(models.Model):
    active_invite_code = models.ForeignKey(InviteCode, on_delete=models.CASCADE, verbose_name='Активированный инвайт-код')
    user = models.OneToOneField(RefUser, verbose_name='Юзер', on_delete=models.CASCADE, related_name='active_invite')

    def __str__(self):
        return f'{self.active_invite_code.code} - {self.user.phone_number}'


class InviteCodeUser(models.Model):
    invite_code = models.ForeignKey(InviteCode, on_delete=models.CASCADE, related_name='invited_users', verbose_name='Инвайт код')
    invited = models.ForeignKey(RefUser, on_delete=models.CASCADE, verbose_name='Приглашенный')

    def __str__(self):
        return f'{self.invite_code.code} - {self.invited.phone_number}'
