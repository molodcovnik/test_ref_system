from rest_framework import serializers

from user.models import RefUser
from referral.models import InviteCodeUser, InviteCode, ActiveUserInviteCode


class InviteUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='invited.id')
    invite_code = serializers.CharField(source='invite_code.code')
    invited = serializers.CharField(source='invited.phone_number')

    class Meta:
        model = InviteCodeUser
        fields = ('id', 'invite_code', 'invited', )


class ProfileSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(source='invitecode.code')
    active_invite_code = serializers.SerializerMethodField()
    invited_users = InviteUserSerializer(many=True, read_only=True, source='invitecode.invited_users')

    class Meta:
        model = RefUser
        fields = ('id', 'phone_number', 'full_name', 'invite_code', 'active_invite_code', 'invited_users', )

    def get_active_invite_code(self, obj):
        active_invite = getattr(obj, 'active_invite', None)
        print(active_invite, flush=True)
        if active_invite:
            return active_invite.active_invite_code.code
        return None


class ActivateInviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField()

    def validate_invite_code(self, value):
        if not InviteCode.objects.filter(code=value).exists():
            raise serializers.ValidationError('Инвайт-код не существует.')
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        invite_code = InviteCode.objects.get(code=self.validated_data['invite_code'])
        if invite_code.user == user:
            raise serializers.ValidationError('Вы не можете использовать свой инвайт код.')

        if InviteCodeUser.objects.filter(invited=user).exists():
            raise serializers.ValidationError('Вы уже активировали инвайт-код.')

        InviteCodeUser.objects.create(invite_code=invite_code, invited=user)
        ActiveUserInviteCode.objects.create(
            active_invite_code=invite_code,
            user=user
        )
        return invite_code
