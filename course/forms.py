from django import forms

from course.models import Email, Course, Subject, Lecture, Section
from django_select2.forms import ModelSelect2Widget as MS2W


class SectionForm(forms.Form):
    # subject_list = [(i + 1, sub.name) for i, sub in enumerate(Subject.objects.all())]
    # course_list = ((i + 1, c.title) for i, c in enumerate(Course.objects.all()))
    # lecture_list = ((i + 1, lec.name) for i, lec in enumerate(Lecture.objects.all()))
    # section_list = ((i + 1, sect.name) for i, sect in enumerate(Section.objects.all()))
    email = forms.CharField()
    # subject = forms.ChoiceField(choices=[subject_list])
    # course = forms.CharField(widget=forms.ModelChoiceField(queryset=Course.objects.none()))
    # lecture = forms.CharField(widget=forms.ModelChoiceField(queryset=Lecture.objects.none()))
    # section = forms.CharField(widget=forms.ModelChoiceField(queryset=Section.objects.none()))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    lecture = forms.ModelChoiceField(queryset=Lecture.objects.all())
    section = forms.ModelChoiceField(queryset=Section.objects.all())

    # subject = forms.ChoiceField(choices=subject_list)
    # course = forms.ChoiceField(choices=course_list)
    # lecture = forms.ChoiceField(choices=lecture_list)
    # section = forms.ChoiceField(choices=section_list)

    # class Meta:
    #      fields = ('name', 'section')

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