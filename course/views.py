from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SectionForm
from .models import Email, Course, Lecture, Section
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
		form = SectionForm(request.POST, request=request)
		if form.is_valid():
			email = request.POST.get('email')
			section_id = request.POST.get('section')
			only_remind_when_open = request.POST.get('only_remind_when_open')
			if only_remind_when_open is None:
				only_remind_when_open = False
			else:
				only_remind_when_open = True
			email_query = Email.objects.filter(name=email)
			if email_query.count():
				user = Email.objects.filter(name=email)[0]
			else:
				user = Email.objects.create(name=email)
			user.section.add(Section.objects.get(id=section_id),
							 through_defaults={'only_remind_when_open': only_remind_when_open})
			form = SectionForm()

	context = {
		'form': form
	}
	return render(request, 'course_add.html', context)


def course_update_view(request):
	pass


def ajax_load_courses(request):
	subject_id = request.GET.get('subject_pk')
	courses = Course.objects.filter(subject_id=subject_id).order_by('abbrev')
	return render(request, 'course_dropdown_list_options.html', {'courses': courses})


def ajax_load_lectures(request):
	course_id = request.GET.get('course_pk')
	lectures = Lecture.objects.filter(course_id=course_id).order_by('name')
	return render(request, 'lecture_dropdown_list_options.html', {'lectures': lectures})


def ajax_load_sections(request):
	lecture_id = request.GET.get('lecture_pk')
	sections = Section.objects.filter(lecture_id=lecture_id).order_by('name')
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
