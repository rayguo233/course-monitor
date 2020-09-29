from django import forms

from course.models import Email, Course, Subject, Lecture, Section
from django_select2.forms import ModelSelect2Widget as MS2W


class SectionForm(forms.Form):
    email = forms.CharField()
    subject = forms.ModelChoiceField(queryset=Subject.objects.all().order_by('name'))
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    lecture = forms.ModelChoiceField(queryset=Lecture.objects.all())
    section = forms.ModelChoiceField(queryset=Section.objects.all())
    only_remind_when_open = forms.BooleanField(label='Only remind me when it is "Open" '
                                                     '(i.e. don\'t remind me when it is "Waitlist").')

    def __init__(self, *args, **kwargs):
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

    # # the following is needed to hide courses before subjects are selected
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs) # calling ModelForm's init
    #     self.fields['course'].queryset = Course.objects.none()
    #
    #     if 'subject' in self.data:
    #         try:
    #             subject_id = int(self.data.get('subject'))
    #             self.fields['course'].queryset = Course.objects.filter(subject_id=subject_id).order_by('abbrev')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty course queryset
    #     elif self.instance.pk:
    #         self.fields['course'].queryset = self.instance.subject.course_set.order_by('abbrev')