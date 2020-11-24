"""first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from first_app import views
urlpatterns = [
    path('',views.index, name="index"),
    path('admin/', admin.site.urls),
    path('first_app/', include("first_app.urls")),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('logout/',views.user_logout, name='logout'),
    path('special/',views.special, name='special'),
    path('accounts/', include('allauth.urls')),
    path('invitation/<slug:event_name>/<contact>/', views.invitationpoll, name='invitationpoll'),
    path('invitation/event_poll/<slug:event_name>/<int:option_num>', views.choose_option,name='choose_option')
   
]
