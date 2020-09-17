from django.db import models

class Subject(models.Model):
	subject = models.CharField(max_length=30)
	def __str__(self):
		return self.subject # this is what shows up in the admin page
							# otherwise it would be "subject(1)"

class Course(models.Model):
	abbrev = models.CharField(max_length=30)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	def __str__(self):
		return self.abbrev

class Email(models.Model):
	email = models.CharField(max_length=30)	
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	def __str__(self):
		return self.email
	