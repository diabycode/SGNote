"""sg_note URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import django.contrib.auth.views

from .views import index, edit_now_academic_year

urlpatterns = [
    path('', index, name='index'),
    path('edit_now_academic_year', edit_now_academic_year, name='edit_now_academic_year'),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('departs_and_mod/', include('departements_and_modules.urls')),
    path('marks_and_results/', include('marks_and_results.urls')),
    path('admin/', admin.site.urls),
]
