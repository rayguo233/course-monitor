from django.contrib import admin
from .models import Subject, Course, Email, Lecture, Section

admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Email)
admin.site.register(Lecture)
admin.site.register(Section)
