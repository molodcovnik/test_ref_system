from django.contrib import admin

from referral.models import InviteCode, InviteCodeUser, ActiveUserInviteCode


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user__phone_number',)
    search_fields = ("code", )


@admin.register(InviteCodeUser)
class InviteCodeUserAdmin(admin.ModelAdmin):
    list_display = ('invite_code__code', 'invited__phone_number', )
    search_fields = ("invite_code__code", )


@admin.register(ActiveUserInviteCode)
class ActiveUserInviteCodeAdmin(admin.ModelAdmin):
    list_display = ('active_invite_code__code', )
    search_fields = ("active_invite_code__code", )
