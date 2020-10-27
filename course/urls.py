from .views import *
from django.urls import path
from django.contrib import admin

urlpatterns = [
    # add tracking course
    path('add/', course_add_view, name='course_add'),
    path('load-courses/', ajax_load_courses, name='ajax_load_courses'),
    path('load-lectures/', ajax_load_lectures, name='ajax_load_lectures'),
    path('load-sections/', ajax_load_sections, name='ajax_load_sections'),

    # untrack a course
    path('untrack/', course_untrack_view, name='course_untrack'),
    path('untrack-sections/', ajax_untrack_sections, name='ajax_untrack_sections'),
]