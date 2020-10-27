from django.core.management.base import BaseCommand
from course.models import Subject


class Command(BaseCommand):
    help = "remove all tracked courses"

    # define logic of command
    def handle(self, *args, **options):
        for subject in Subject.objects.all():
            print('Deleting ' + str(subject))
            subject.delete()
