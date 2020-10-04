from django import forms

from course.models import Email, Course, Subject, Lecture, Section
from django.core.exceptions import ObjectDoesNotExist


class SectionForm(forms.Form):
    email = forms.EmailField()
    subject = forms.ModelChoiceField(queryset=Subject.objects.all().order_by('name'))
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    lecture = forms.ModelChoiceField(queryset=Lecture.objects.all())
    section = forms.ModelChoiceField(queryset=Section.objects.all())
    only_remind_when_open = forms.BooleanField(label='Only remind me when it is "Open" '
                                                     '(i.e. don\'t remind me when it is "Waitlist").',
                                               required=False)

    def __init__(self, email_address='', *args, **kwargs):
        course_list = Course.objects.none()
        lecture_list = Lecture.objects.none()
        section_list = Section.objects.none()
        self.request = kwargs.pop('request', None)
        request = self.request
        if request is None:
            pass
        elif request.method == 'POST':
            subject_id = request.POST.get('subject')
            course_id = request.POST.get('course')
            lecture_id = request.POST.get('lecture')
            # section_id = request.POST.get('section')
            if subject_id != 'None':
                course_list = Course.objects.filter(subject=subject_id)
                if course_id != 'None':
                    lecture_list = Lecture.objects.filter(course=course_id)
                    if lecture_id != 'None':
                        section_list = Section.objects.filter(lecture=lecture_id)
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = course_list
        self.fields['lecture'].queryset = lecture_list
        self.fields['section'].queryset = section_list
        self.fields['email'] = forms.EmailField(initial=email_address)
        if email_address != '':
            self.fields['email'].widget.attrs['readonly'] = True


class SectionUntrackForm(forms.Form):
    email = forms.EmailField()
    section = forms.ModelChoiceField(queryset=Section.objects.all())

    def __init__(self, email_address='', *args, **kwargs):
        if email_address != '':
            try:
                user = Email.objects.get(name=email_address)
            except ObjectDoesNotExist:
                section_list = Section.objects.none()
            else:
                section_list = user.section.all()
        else:
            section_list = Section.objects.none()
        super().__init__(*args, **kwargs)
        self.fields['section'].queryset = section_list
        if email_address != '':
            self.fields['email'] = forms.EmailField(initial=email_address)
            self.fields['email'].widget.attrs['readonly'] = True
