import random
import string

from user.models import RefUser
from referral.models import InviteCode


def get_or_create_invite_code(user: RefUser) -> str:
    """Функция генерирует инвайт-код и возвращает его"""

    try:
        return user.invitecode.code
    except InviteCode.DoesNotExist:
        code = (''.join(random.choices(string.ascii_letters + string.digits, k=3)) + '-' +
                ''.join(random.choices(string.ascii_letters + string.digits, k=3)))

        invite_cod = InviteCode.objects.create(code=code, user=user)

        return invite_cod.code
