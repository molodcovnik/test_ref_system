from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from referral.api.v1.serializers import ProfileSerializer, ActivateInviteCodeSerializer


class ProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        return user

    @extend_schema(
        responses={
            200: ProfileSerializer,
        },
        summary='Профиль пользователя',
    )
    def get(self, request, format=None):
        user = self.get_object()
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class ActivateInviteCodeView(APIView):
    http_method_names = ['post']
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ActivateInviteCodeSerializer,
        responses={
            200: {'type': 'object', 'properties': {'detail': {'type': 'string', 'example': 'Инвайт-код успешно активирован.'}}},
            400: {'type': 'object', 'properties': {'detail': {'type': 'string', 'example': 'Вы уже активировали инвайт-код.'}}},
            404: {'type': 'object', 'properties': {'detail': {'type': 'string', 'example': 'Инвайт-код не существует.'}}},
            500: {'type': 'object', 'properties': {'detail': {'type': 'string', 'example': 'Внутренняя ошибка сервера, пожалуйста попробуйте позднее.'}}},
        },
        summary='Активировать чужой инвайт код в своем профиле',
    )
    def post(self, request):
        serializer = ActivateInviteCodeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Инвайт-код успешно активирован.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
