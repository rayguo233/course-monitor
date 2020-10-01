"""course_monitor URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path
from course.views import *
from user.views import *

urlpatterns = [
    # path('', home_view, name='home'),
    path('', course_add_view, name='course_add'),
    path('ray/', admin.site.urls),  # admin view
    path('course/detail/', course_detail_view),  # see all courses
    path('register/', user_register_view, name='register'),
    path('profile/', user_profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),

    # add tracking course
    path('emmmail/', EmailListView.as_view(), name='email_list'),
    path('add/', course_add_view, name='course_add'),
    path('load-courses/', ajax_load_courses, name='ajax_load_courses'),
    path('load-lectures/', ajax_load_lectures, name='ajax_load_lectures'),
    path('load-sections/', ajax_load_sections, name='ajax_load_sections'),
]
