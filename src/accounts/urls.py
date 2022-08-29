from django.urls import path, include

import django.contrib.auth.urls

from .views import CustomLoginView, CustomLogoutView

app_name = "accounts"

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', CustomLogoutView.as_view(), name="logout"),

]


