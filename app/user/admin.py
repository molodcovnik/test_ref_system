from django.contrib import admin

from user.models import RefUser, CodeAuth


@admin.register(RefUser)
class BonusBalanceAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', )
    search_fields = ("phone_number", )


@admin.register(CodeAuth)
class BonusBalanceAdmin(admin.ModelAdmin):
    list_display = ('code', 'user__full_name',)
    search_fields = ("code", )
