from django.urls import path, include

from user.api.v1.views import LoginView, Logout, AuthView

urlpatterns = [
    path('auth', AuthView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('logout', Logout.as_view()),
]