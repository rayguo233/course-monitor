from django import forms

from course.models import Email, Course


class EmailCreationForm(forms.ModelForm):
    class Meta:
        model = Email # we will be creating a new Email object
        fields = '__all__'

    # the following is needed to hide courses before subjects are selected
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # calling ModelForm's init
        self.fields['course'].queryset = Course.objects.none()

        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['course'].queryset = Course.objects.filter(subject_id=subject_id).order_by('abbrev')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty course queryset
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.subject.course_set.order_by('abbrev')