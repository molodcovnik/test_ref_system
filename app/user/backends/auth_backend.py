from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User
from user.models import RefUser


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, phone_number=None):
        try:
            user = RefUser.objects.get(phone_number=phone_number)
            return user
        except RefUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return RefUser.objects.get(pk=user_id)
        except RefUser.DoesNotExist:
            return None