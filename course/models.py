from django.db import models


class BaseModel(models.Model):
	objects = models.Manager()

	class Meta:
		abstract = True


class Subject(BaseModel):
	name = models.CharField(max_length=70)

	def __str__(self):
		return self.name  # this is what shows up in the admin page otherwise it would be "subject(1)"


class Course(BaseModel):
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	abbrev = models.CharField(max_length=30)
	title = models.CharField(max_length=200)

	def __str__(self):
		return self.title


class Lecture(BaseModel):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	name = models.CharField(max_length=15)

	def __str__(self):
		return self.course.__getattribute__('abbrev') + ' ' + self.name


class Section(BaseModel):
	lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
	name = models.CharField(max_length=15)
	status = models.CharField(max_length=50, null=True)
	num_spots_taken = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.lecture.__str__() + ' ' + self.name + ' ' + self.status


class Email(BaseModel):
	name = models.CharField(max_length=40)
	section = models.ManyToManyField(Section, blank=True, through='WhenToRemind')

	def __str__(self):
		return self.name


class WhenToRemind(BaseModel):
	email = models.ForeignKey(Email, on_delete=models.CASCADE)
	section = models.ForeignKey(Section, on_delete=models.CASCADE)
	only_remind_when_open = models.BooleanField(null=True)
