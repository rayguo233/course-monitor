from django.db import models



class Subject(models.Model):
	name = models.CharField(max_length=70)

	def __str__(self):
		return self.name  # this is what shows up in the admin page otherwise it would be "subject(1)"


class Course(models.Model):
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	abbrev = models.CharField(max_length=30)
	title = models.CharField(max_length=200)

	def __str__(self):
		return self.title


class Lecture(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	name = models.CharField(max_length=15)

	def __str__(self):
		return self.course.__getattribute__('abbrev') + ' ' + self.name


class Section(models.Model):
	lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
	name = models.CharField(max_length=15)

	def __str__(self):
		return self.lecture.__str__() + ' ' + self.name


class Email(models.Model):
	name = models.CharField(max_length=40)
	section = models.ManyToManyField(Section, blank=True)

	def __str__(self):
		return self.name

