import time

from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework import views, status
from rest_framework.response import Response
from user.backends.auth_backend import PasswordlessAuthBackend
from django.contrib.auth import logout as auth_logout

from user.api.v1.services.code_gen import get_four_code
from user.models import CodeAuth
from user.models import RefUser

from referral.api.v1.services.generate_invite import get_or_create_invite_code

from user.api.v1.serializers import AuthSerializer, CodeSerializer, LoginSerializer, TokenSerializer


class AuthView(views.APIView):
    http_method_names = ['post']
    auth_backend = PasswordlessAuthBackend()

    @extend_schema(
        request=AuthSerializer,
        responses={
            200: CodeSerializer,
        },
        summary='Аутентификация пользователя',
        description='Метод проверяет наличие пользователя, если нет, то создаст нового и вернет смс-код(имитация) в своем ответе',
    )
    def post(self, request, format=None):
        phone_number = request.data.get('phone_number', None)
        is_user = RefUser.objects.filter(phone_number=phone_number).exists()

        if not is_user:
            RefUser.objects.create(phone_number=phone_number)

        user = self.auth_backend.authenticate(phone_number=phone_number)
        code = get_four_code()
        get_or_create_invite_code(user)
        if user is not None:
            CodeAuth.objects.create(
                code=code,
                user=user
            )
            time.sleep(2)
            return Response(data={"code": code}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    http_method_names = ['post']
    auth_backend = PasswordlessAuthBackend()

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: TokenSerializer,
        },
        summary='Логин',
        description='Логиним пользователя через номер телефона и смс-код, в ответ получаем токен аутентификации',
    )
    def post(self, request, format=None):
        phone_number = request.data.get('phone_number', None)
        auth_code = request.data.get('code', None)
        user = self.auth_backend.authenticate(phone_number=phone_number)
        last_code = user.codes.last()

        if user is not None and last_code.code == auth_code:
            token, _ = Token.objects.get_or_create(user=user)

            login(request, user)
            return Response(data={"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class Logout(views.APIView):

    @extend_schema(
        responses={
            200: {},
        },
        summary='Выход из системы',
        description='Выход из системы',
    )
    def get(self, request, format=None):
        auth_logout(request)
        return Response(status=status.HTTP_200_OK)
