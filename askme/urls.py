"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('questions/', views.get_questions, name='questions'),
    path('question/<int:qid>/', views.question, name='question'),
    path('tag/<slug:tag_name>/', views.tag_page, name='tag'),
    path('ask/', views.ask, name='ask'),
    path('signup/', views.register, name='signup'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
]