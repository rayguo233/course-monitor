from django.core.management.base import BaseCommand
from course.models import Email


class Command(BaseCommand):
    help = "remove all tracked courses"

    # define logic of command
    def handle(self, *args, **options):
        for email in Email.objects.all():
            email.section.clear()
