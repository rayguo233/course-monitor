from django.shortcuts import render

from .models import Course
# Create your views here.
def course_detail_view(request):
	c = Course.objects.all()
	context = {
		'courses': c
	}
	return render(request, "course/detail.html", context)