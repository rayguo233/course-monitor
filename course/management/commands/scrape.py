from django.core.management.base import BaseCommand
from selenium import webdriver
import os
import time
# local
from course.models import Subject, Course, Lecture, Section, Email, WhenToRemind
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def keep_awake(driver):
	# only pin the website if it's before 37 minutes into the hour
	if (time.localtime() > 37):
		return
	driver.get("https://course-monitor.herokuapp.com/")
	print("Pin the website.")
	time.sleep(90) # wait for 1.5 minutes
	print("Finished pinning.")

def clear_status_info(section):
	section.status = ''
	section.num_spots_taken = ''

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


def check_section(sections, driver, wait):
	lectures = Lecture.objects.none()
	for section in sections:
		lecture_id = section.lecture.id
		lectures |= Lecture.objects.filter(id=lecture_id)
	lectures = lectures.distinct()
	courses = Course.objects.none()
	for lecture in lectures:
		course_id = lecture.course.id
		courses |= Course.objects.filter(id=course_id)
	courses = courses.distinct()
	subjects = Subject.objects.none()
	for course in courses:
		subject_id = course.subject.id
		subjects |= Subject.objects.filter(id=subject_id)
	subjects = subjects.distinct()
	driver.get("https://sa.ucla.edu/ro/public/soc")
	for cur_subject in subjects:
		print('###########################')
		print('Subject: ' + cur_subject.name)
		input_box = wait.until(EC.presence_of_element_located((By.ID, 'select_filter_subject')))
		ActionChains(driver).move_to_element(input_box).click(input_box).perform()
		time.sleep(2)
		ActionChains(driver).send_keys(cur_subject.name).perform()
		time.sleep(2)
		item_in_dropdown = driver.find_element_by_class_name('ui-menu-item')
		ActionChains(driver).move_to_element(item_in_dropdown).click(item_in_dropdown).perform()
		time.sleep(1)
		go_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_go')))
		ActionChains(driver).move_to_element(go_button).click(go_button).perform()
		time.sleep(4)
		# get courses to search in this subject
		cur_courses = courses.filter(subject=cur_subject).order_by()
		print(cur_courses)
		for cur_course in cur_courses:
			# find to the right page
			while True:
				try:
					course_div = driver.find_element_by_id(cur_course.abbrev)
				except NoSuchElementException:
					# go to next page
					next_btn = driver.find_element_by_class_name('jPag-snext-img')
					ActionChains(driver).move_to_element(next_btn).click(next_btn).perform()
					time.sleep(3)
				else:
					break
			time.sleep(3)
			course_link = course_div.find_element_by_class_name('head').find_element_by_tag_name('a')
			course_link.location_once_scrolled_into_view
			course_link.click()
			time.sleep(3)
			# get lectures to search for cur_course
			cur_lectures = [lecture for lecture in lectures if lecture.course == cur_course]
			print(cur_lectures)
			for cur_lecture in cur_lectures:
				lec_divs = course_div.find_elements_by_class_name(
					'row-fluid.data_row.primary-row.class-info.class-not-checked')
				for lec_div in lec_divs:
					if cur_lecture.name == lec_div.find_element_by_class_name('sectionColumn').find_element_by_tag_name('a').text:
						cur_sections = [section for section in sections if section.lecture == cur_lecture]
						print(cur_sections)
						if cur_sections[0].name == 'No Section':
							cur_section = cur_sections[0]
							section_info = lec_div.find_element_by_class_name('statusColumn').find_element_by_tag_name(
								'p').text.split('\n')
							section_status = section_info[0]
							cur_section.status = '(' + section_status + ')'
							num_spots_taken = section_info[1] if len(section_info) >= 2 else ''
							num_spots_left = section_info[2] if len(section_info) >= 3 else ''
							cur_section.num_spots_taken = num_spots_taken + ' | ' + num_spots_left
							print(str(cur_section) + ': ' + cur_section.num_spots_taken)
							cur_section.save()
							# send emails
							if section_status == 'Open' or section_status == 'Waitlist':
								emails_to_send = cur_section.email_set.all()
								for email in emails_to_send:
									if WhenToRemind.objects.get(section=cur_section, email=email).only_remind_when_open:
										if section_status == 'Open':
											send_reminder(email.__str__(), cur_section.__str__())
											email.section.remove(cur_section)
											clear_status_info(cur_section)
									else:
										send_reminder(email.__str__(), cur_section.__str__())
										email.section.remove(cur_section)
										clear_status_info(cur_section)
						else:
							# expand sections
							expand_sect_link = lec_div.find_element_by_class_name('toggle')
							ActionChains(driver).move_to_element(expand_sect_link).click(expand_sect_link).perform()
							time.sleep(3)
							cur_sections = [section for section in sections if section.lecture == cur_lecture]
							# find section
							for cur_section in cur_sections:
								sect_divs = lec_div.find_elements_by_class_name(
									'row-fluid.data_row.secondary-row.class-info.class-not-checked')
								for sect_div in sect_divs:
									if cur_section.name == sect_div.find_element_by_class_name('sectionColumn').find_element_by_tag_name(
											'a').text:
										section_info = sect_div.find_element_by_class_name('statusColumn').find_element_by_tag_name(
											'p').text.split('\n')
										section_status = section_info[0]
										cur_section.status = '(' + section_status + ')'
										num_spots_taken = section_info[1] if len(section_info) >= 2 else ''
										num_spots_left = section_info[2] if len(section_info) >= 3 else ''
										cur_section.num_spots_taken = num_spots_taken + ' | ' + num_spots_left
										print(str(cur_section) + ': ' + cur_section.num_spots_taken)
										cur_section.save()
										# send emails
										if section_status == 'Open' or section_status == 'Waitlist':
											emails_to_send = cur_section.email_set.all()
											for email in emails_to_send:
												if WhenToRemind.objects.get(section=cur_section, email=email).only_remind_when_open:
													if section_status == 'Open':
														send_reminder(email.__str__(), cur_section.__str__())
														email.section.remove(cur_section)
														clear_status_info(cur_section)
												else:
													send_reminder(email.__str__(), cur_section.__str__())
													email.section.remove(cur_section)
													clear_status_info(cur_section)
							ActionChains(driver).move_to_element(expand_sect_link).click(expand_sect_link).perform()
							time.sleep(2)

		search_btn = wait.until(EC.element_to_be_clickable((By.ID, 'btn_start_search')))
		ActionChains(driver).move_to_element(search_btn).click(search_btn).perform()
		time.sleep(2)


class Command(BaseCommand):
	help = "scrape courses"

	# define logic of command
	def handle(self, *args, **options):
		# get all sections needed to check
		emails = Email.objects.all()
		sections = Section.objects.none()
		for email in emails:
			sections |= email.section.all()
		sections = sections.distinct()

		# prepare driver
		op = webdriver.ChromeOptions()
		op.add_argument("--headless")
		# see if the script is being run on cloud or local
		if os.environ.get("GOOGLE_CHROME_BIN") is None:
			# if on local
			print('Go local.')
			driver = webdriver.Chrome(chrome_options=op) 
		else:
			# if on cloud
			print('Go cloud.')
			op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
			op.add_argument("--no-sandbox")  # required by heroku
			op.add_argument("--disable-dev-sh-usage")        
			driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op) # on cloud

		# pin the website to keep it from idling
		keep_awake(driver)

		# check the sections
		if len(sections) == 0:
			print('0 sections to search.')
		else:
			print(str(len(sections)) + ' sections to search.')

			# search
			# op = webdriver.ChromeOptions()
			# op.add_argument("--headless")  # set headless chrome
			# op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
			# op.add_argument("--no-sandbox")  # required by heroku
			# op.add_argument("--disable-dev-sh-usage")
			
			# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op) # on cloud
			# # driver = webdriver.Chrome(chrome_options=op)  # on local
			driver.set_window_size(1920, 1000)
			wait = WebDriverWait(driver, 10, poll_frequency=1)
			check_section(sections, driver, wait)
