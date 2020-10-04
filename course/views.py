from django.shortcuts import render, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SectionForm
from .models import Email, Course, Lecture, Section, WhenToRemind


@staff_member_required(login_url='login')
def email_list_view(request):
	emails = Email.objects.all()
	return render(request, "course/email_list.html", {'emails': emails})


def course_detail_view(request):
	c = Course.objects.all()
	context = {
		'courses': c
	}
	return render(request, "course/course_detail.html", context)


def course_add_view(request):
	if request.user.is_authenticated:
		email_address = request.user.email
	else:
		email_address =''
	form = SectionForm(email_address=email_address)
	if request.method == 'POST':
		form = SectionForm(email_address, request.POST, request=request)
		if form.is_valid():
			email_address = request.POST.get('email')
			section_id = request.POST.get('section')
			only_remind_when_open = request.POST.get('only_remind_when_open')
			if only_remind_when_open is None:
				only_remind_when_open = False
			else:
				only_remind_when_open = True
			email_query = Email.objects.filter(name=email_address)
			if email_query.count():
				email = Email.objects.filter(name=email_address)[0]
			else:
				email = Email.objects.create(name=email_address)
			section = Section.objects.get(id=section_id)
			email.section.add(section)
			WhenToRemind.objects.update_or_create(email=email, section=section,
												  defaults={"only_remind_when_open": only_remind_when_open})
			form = SectionForm(email_address=email_address)

	context = {
		'form': form
	}
	return render(request, 'course/course_add.html', context)


def ajax_load_courses(request):
	subject_id = request.GET.get('subject_pk')
	courses = Course.objects.filter(subject_id=subject_id).order_by('abbrev')
	return render(request, 'course/course_dropdown_list_options.html', {'courses': courses})


def ajax_load_lectures(request):
	course_id = request.GET.get('course_pk')
	lectures = Lecture.objects.filter(course_id=course_id).order_by('name')
	return render(request, 'course/lecture_dropdown_list_options.html', {'lectures': lectures})


def ajax_load_sections(request):
	lecture_id = request.GET.get('lecture_pk')
	sections = Section.objects.filter(lecture_id=lecture_id).order_by('name')
	return render(request, 'course/section_dropdown_list_options.html', {'sections': sections})


def course_untrack_view(request):
	pass
