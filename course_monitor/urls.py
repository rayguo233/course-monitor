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
from django.urls import path

from pages.views import home_view
from course.views import course_detail_view, course_add_view,\
    course_update_view, load_courses

urlpatterns = [
	path('', home_view, name='home'),
    path('ray/', admin.site.urls), # admin view
	path('course/detail/', course_detail_view), # see all courses

    # add tracking course
    path('add/', course_add_view, name='course_add'),
    path('<int:pk>/', course_update_view, name='course_change'),
    path('ajax/load-courses/', load_courses, name='ajax_load_courses'),


]
