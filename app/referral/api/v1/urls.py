from django.urls import path

from referral.api.v1.views import ProfileView, ActivateInviteCodeView

urlpatterns = [
    path('profile', ProfileView.as_view()),
    path('profile/active-invite', ActivateInviteCodeView.as_view()),
]