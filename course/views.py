from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SectionForm
from .models import Email, Course, Subject, Lecture, Section
from django.views import generic
from django.views.generic.list import ListView


class EmailListView(ListView):
	template_name = 'email_list.html'
	queryset = Email.objects.all()


def course_detail_view(request):
	c = Course.objects.all()
	context = {
		'courses': c
	}
	return render(request, "course_detail.html", context)


def course_add_view(request):
	form = SectionForm()
	if request.method == 'POST':
		# subject = request.POST.get('subject')
		# course = request.POST.get('course')
		# lecture = request.POST.get('lecture')
		# section = request.POST.get('section')
		form = SectionForm(request.POST, request=request)
		# form.fields['subject'].choices = [(subject, subject)]
		# print(form.fields['course'].choices)
		# form.fields['course'].choices = [(course, course)]
		# form.fields['lecture'].choices = [(lecture, lecture)]
		# form.fields['section'].choices = [(section, section)]
		if form.is_valid():
			email = request.POST.get('email')
			section = request.POST.get('section')
			user = Email.objects.update_or_create(name=email)[0]
			user.section.add(section)
			form = SectionForm()

	context = {
		'form': form
	}
	return render(request, 'course_add.html', context)


def course_update_view(request):
	pass


def ajax_load_courses(request):
	subject_id = request.GET.get('subject_pk')
	courses = Course.objects.filter(subject_id=subject_id)
	return render(request, 'course_dropdown_list_options.html', {'courses': courses})


def ajax_load_lectures(request):
	course_id = request.GET.get('course_pk')
	lectures = Lecture.objects.filter(course_id=course_id)
	return render(request, 'lecture_dropdown_list_options.html', {'lectures': lectures})


def ajax_load_sections(request):
	lecture_id = request.GET.get('lecture_pk')
	sections = Section.objects.filter(lecture_id=lecture_id)
	return render(request, 'section_dropdown_list_options.html', {'sections': sections})


# class CourseTrackView(generic.CreateView):
# 	model = Subject
# 	form_class = SectionForm
# 	success_url = '/'


# def course_add_view(request):
# 	form = EmailCreationForm()
# 	if request.method == 'POST':
# 		form = EmailCreationForm(request.POST)
# 		if form.is_valid():
# 			Email.objects.create(**form.cleaned_data)
# 		else:
# 			print(form.errors)
# 	context = {
# 		'form': form
# 	}
# 	return render(request, 'course_add.html', context)


	# form = EmailCreationForm()
	# if request.method == 'POST':
	# 	form = EmailCreationForm(request.POST)
	# 	if form.is_valid():
	# 		form.save()
	# 		return redirect('course_add')
	# return render(request, 'course_home.html', {'form': form})
