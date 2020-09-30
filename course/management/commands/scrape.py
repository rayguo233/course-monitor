from django.core.management.base import BaseCommand
from selenium import webdriver
import os
import time
# local
from course.models import Section, Email, WhenToRemind
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def send_reminder(email, section):
	message = Mail(
		from_email='siruiguo@outlook.com',
		to_emails=email,
		subject='Your ' + section + ' has an available spot',
		html_content='<strong>Your class has an available spot (see title).</strong>\
					 <br><br>\
					 <p>Add the class to your email again on the website if you wish to keep receiving reminder \
					 for this class</p>')
	try:
		sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		sg.send(message)
	except Exception as e:
		print(e.message)


def check_section(cur_section, driver, wait):
	input_box = wait.until(EC.presence_of_element_located((By.ID, 'select_filter_subject')))
	ActionChains(driver).move_to_element(input_box).click(input_box).perform()
	time.sleep(2)
	ActionChains(driver).send_keys(cur_section.lecture.course.subject.name).perform()
	time.sleep(2)
	item_in_dropdown = driver.find_element_by_class_name('ui-menu-item')
	ActionChains(driver).move_to_element(item_in_dropdown).click(item_in_dropdown).perform()
	time.sleep(1)
	go_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_go')))
	ActionChains(driver).move_to_element(go_button).click(go_button).perform()
	# expand_btn = wait.until(EC.element_to_be_clickable((By.ID, 'expandAll')))
	# ActionChains(driver).move_to_element(expand_btn).click(expand_btn).perform()
	time.sleep(3)
	while True:
		try:
			cur_course_div = driver.find_element_by_id(cur_section.lecture.course.abbrev)
		except NoSuchElementException:
			# go to next page
			next_btn = driver.find_element_by_class_name('jPag-snext-img')
			ActionChains(driver).move_to_element(next_btn).click(next_btn).perform()
			time.sleep(3)
			# expand_btn = wait.until(EC.element_to_be_clickable((By.ID, 'expandAll')))
			# ActionChains(driver).move_to_element(expand_btn).click(expand_btn).perform()
			# time.sleep(7)
		else:
			break
	time.sleep(3)
	course_link = cur_course_div.find_element_by_class_name('head').find_element_by_tag_name('a')
	course_link.location_once_scrolled_into_view
	course_link.click()
	time.sleep(3)
	lec_divs = cur_course_div.find_elements_by_class_name(
		'row-fluid.data_row.primary-row.class-info.class-not-checked')
	cur_lecture = cur_section.lecture
	for lec_div in lec_divs:
		if cur_lecture.name == lec_div.find_element_by_class_name('sectionColumn').find_element_by_tag_name(
				'a').text:
			if cur_section.name == 'No Section':
				print(cur_section.__str__() + ' found.')
				section_status = lec_div.find_element_by_class_name('statusColumn').find_element_by_tag_name('p')\
						.text.partition('\n')[0]
				cur_section.status = '(' + section_status + ')'
				cur_section.save(update_fields=['status'])
				print(cur_section)
				if section_status == 'Open' or section_status == 'Waitlist':
					emails_to_send = cur_section.email_set.all()
					for email in emails_to_send:
						if WhenToRemind.objects.get(section=cur_section, email=email).only_remind_when_open:
							if section_status == 'Open':
								send_reminder(email.__str__(), cur_section.__str__())
								email.section.remove(cur_section)
						else:
							send_reminder(email.__str__(), cur_section.__str__())
							email.section.remove(cur_section)
			else:
				# expand sections
				expand_sect_link = lec_div.find_element_by_class_name('toggle')
				ActionChains(driver).move_to_element(expand_sect_link).click(expand_sect_link).perform()
				time.sleep(3)
				# find section
				sect_divs = lec_div.find_elements_by_class_name(
					'row-fluid.data_row.secondary-row.class-info.class-not-checked')
				for sect_div in sect_divs:
					if cur_section.name == sect_div.find_element_by_class_name('sectionColumn').find_element_by_tag_name(
							'a').text:
						section_status = sect_div.find_element_by_class_name('statusColumn').find_element_by_tag_name(
							'p').text.partition('\n')[0]
						cur_section.status = '(' + section_status + ')'
						if section_status == 'Open' or section_status == 'Waitlist':
							emails_to_send = cur_section.email_set.all()
							for email in emails_to_send:
								if WhenToRemind.objects.get(section=cur_section, email=email).only_remind_when_open:
									if section_status == 'Open':
										send_reminder(email.__str__(), cur_section.__str__())
										email.section.remove(cur_section)
								else:
									send_reminder(email.__str__(), cur_section.__str__())
									email.section.remove(cur_section)
						break
			break
	print(cur_section)


class Command(BaseCommand):
	help = "collect courses"

	# define logic of command
	def handle(self, *args, **options):
		emails = Email.objects.all()
		sections = Section.objects.none()
		for email in emails:
			sections |= email.section.all()
		sections = sections.distinct()
		if len(sections) == 0:
			print('0 sections to search.')
		else:
			print(str(len(sections)) + ' sections to search.')

			# search
			op = webdriver.ChromeOptions()
			# op.add_argument("--headless")  # set headless chrome
			# op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
			# op.add_argument("--no-sandbox")  # required by heroku
			# op.add_argument("--disable-dev-sh-usage")
			#
			# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op) # on cloud
			driver = webdriver.Chrome(chrome_options=op)  # on local
			driver.set_window_size(1920, 1000)
			wait = WebDriverWait(driver, 10, poll_frequency=1)

			print('Checking ' + sections[0].__str__())
			cur_section = sections[0]
			driver.get("https://sa.ucla.edu/ro/public/soc")
			check_section(cur_section, driver, wait)
			if len(sections) > 1:
				print('Prev: ' + str(len(sections)) + ' sections left.')
				sections = sections.exclude(id=cur_section.id)
				print('Now: ' + str(len(sections)) + ' sections left.')
				for cur_section in sections:
					print('Checking ' + cur_section.__str__())
					search_btn = wait.until(EC.element_to_be_clickable((By.ID, 'btn_start_search')))
					ActionChains(driver).move_to_element(search_btn).click(search_btn).perform()
					time.sleep(2)
					check_section(cur_section, driver, wait)
