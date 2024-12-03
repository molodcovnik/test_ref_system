from django.urls import include, path

urlpatterns = [
    path('v1/referrals/', include('referral.api.v1.urls')),

]