from django.core.management.base import BaseCommand
import os
# local
from course.models import Email
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(email):
	message = Mail(
		from_email='siruiguo@outlook.com',
		to_emails=email,
		subject='Course-Monitor: New Feature Added - Untrack a Class',
		html_content="Good news, you can now untrack your classes! ≡┗( ^o^)┛≡┏( ^o^)┓≡┗( ^o^)┛ \
					  <br><br> \
					  (if there aren't any unknown bugs)"
	)
	try:
		sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		sg.send(message)
	except Exception as e:
		print(e.message)
	else:
		print('Sent to' + email)


class Command(BaseCommand):
	help = "collect courses"

	# define logic of command
	def handle(self, *args, **options):
		for email in Email.objects.all():
			send_email(email.name)