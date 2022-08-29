from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url


class CustomLoginView(LoginView):
    redirect_authenticated_user = 'index'


class CustomLogoutView(LogoutView):
    pass




