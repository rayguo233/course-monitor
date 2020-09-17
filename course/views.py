from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EmailCreationForm
from .models import Email, Course

def course_detail_view(request):
	c = Course.objects.all()
	context = {
		'courses': c
	}
	return render(request, "course_detail.html", context)

def course_add_view(request):
	form = EmailCreationForm()
	if request.method == 'POST':
		form = EmailCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('course_add')
	return render(request, 'course_home.html', {'form': form})

def course_update_view(request):
	email = get_object_or_404(Email, pk=pk)
	form = EmailCreationForm(instance=email)
	if request.method == 'POST':
		form = EmailCreationForm(request.POST, instance=email)
		if form.is_valid():
			form.save()
			return redirect('email_change', pk=pk)
	return render(request, 'course_home.html', {'form': form})

def load_courses(request):
	subject_id = request.GET.get('subject_id')
	courses = Course.objects.filter(subject_id=subject_id)
	return render(request, 'course_dropdown_list_options.html', {'courses': courses})
	# return JsonResponse(list(cities.values('id', 'name')), safe=False)