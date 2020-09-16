from django.core.management.base import BaseCommand
from selenium import webdriver
import os
# local
from course.models import Course

class Command(BaseCommand):
	help = "collect courses"

	# define logic of command
	def handle(self, *args, **options):
		op = webdriver.ChromeOptions()
		op.add_argument("--headless") # set headless chrome
		op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")		
		op.add_argument("--no-sandbox") # required by heroku
		op.add_argument("--disable-dev-sh-usage")

		driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),\
								  chrome_options=op) # on cloud
		# driver = webdriver.Chrome('C:/Users/Sirui/Dev/course_monitor/chromedriver.exe',\
		# 					      chrome_options=op) # on local
		driver.get("https://sa.ucla.edu/ro/public/soc")
		print(driver.title)

		Course.objects.create(abbrev=driver.title)
		print("scrape.py is working")
