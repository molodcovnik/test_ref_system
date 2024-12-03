from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()