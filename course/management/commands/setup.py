from django.core.management.base import BaseCommand
from selenium import webdriver
import os
import time
from course.models import Course, Subject, Lecture, Section
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

START_SUB = 'Molecular, Cellular, and Integrative Physiology (MC&IP)'

def is_over_300(lec_name):
    digits = [int(c) for c in lec_name if c.isdigit()]
    digits.reverse()
    cur_digit = 1
    for i in digits:
        if cur_digit == 3:
            if i > 2: return True
            else: return False
        cur_digit += 1
    return False

def process_results_table(table, subject, wait):
    # get courses
    heads = table.find_elements_by_class_name('row-fluid.class-title')
    for head in heads:
        abbrev = head.get_attribute('id')
        title = head.find_element_by_tag_name('h3').find_element_by_tag_name('a').text
        course = Course.objects.update_or_create(abbrev=abbrev, title=title, subject=subject)[0]
        print(abbrev)
        # get lectures
        lec_divs = head.find_elements_by_class_name('row-fluid.data_row.primary-row.class-info.class-not-checked')
        num_lec = 0
        for lec_div in lec_divs:
            lec_sub_divs = lec_div.find_elements_by_class_name('sectionColumn')
            lec_names = []
            for lec_sub_div in lec_sub_divs:    # for each lecture
                lec_names.append(lec_sub_div.find_element_by_tag_name('a').text)
            print(lec_names)
            num_lec += 1
            if num_lec > 7:
                print("Stop searching this class. Too many lecs.")
                if is_over_300(abbrev):
                    print("Course number bigger than 300. Next subject.")
                    return
                break
            if len(lec_names) == 1:
                new_lec = Lecture.objects.update_or_create(course=course, name=lec_names[0])[0]
                Section.objects.update_or_create(lecture=new_lec, name='No Section')
            else:
                # pop off the first name, the rest is section names
                new_lec = Lecture.objects.update_or_create(course=course, name=lec_names.pop(0))[0]
                for sect_name in lec_names:     # for each section
                    Section.objects.update_or_create(lecture=new_lec, name=sect_name)


def get_course_info(subject, driver, wait):
    # go to result page
    driver.get("https://sa.ucla.edu/ro/public/soc")
    input_box = wait.until(EC.presence_of_element_located((By.ID, 'select_filter_subject')))

    ActionChains(driver).move_to_element(input_box).click(input_box).perform()
    time.sleep(2)
    ActionChains(driver).send_keys(subject.name).perform()
    time.sleep(2)
    ActionChains(driver).send_keys(Keys.DOWN).perform()
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    time.sleep(4)

    try:
        expand_btn = wait.until(EC.element_to_be_clickable((By.ID, 'expandAll')))
    except:
        print('Expand button not found')
    else:
        # get courses on the first page
        ActionChains(driver).move_to_element(expand_btn).click(expand_btn).perform()
        time.sleep(7)
        table = wait.until(EC.presence_of_element_located((By.ID, 'resultsTitle')))
        process_results_table(table, subject, wait)

        # get num of pages
        try:
            ul_pages = driver.find_element_by_class_name('jPag-pages')
        except NoSuchElementException:
            pass
        else:
            # get courses on other pages
            li_pages = ul_pages.find_elements_by_tag_name('li')
            num_pages = len(li_pages)
            for j in range(num_pages - 1):
                # find courses
                next_page = driver.find_element_by_xpath('//*[@id="divPagination"]/div/div/div[3]/span')
                webdriver.ActionChains(driver).move_to_element(next_page).click(next_page).perform()
                time.sleep(2)
                expand_btn = wait.until(EC.element_to_be_clickable((By.ID, 'expandAll')))
                ActionChains(driver).move_to_element(expand_btn).click(expand_btn).perform()
                time.sleep(5)
                table = wait.until(EC.presence_of_element_located((By.ID, 'resultsTitle')))
                process_results_table(table, subject, wait)


class Command(BaseCommand):
    help = "collect courses"

    # define logic of command
    def handle(self, *args, **options):
        # prepare driver
        op = webdriver.ChromeOptions()
        op.add_argument("--headless")
		# see if the script is being run on cloud or local
        if os.environ.get("GOOGLE_CHROME_BIN") is None:
			# if on local
            print('Go local.')
            driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=op) 
        else:
			# if on cloud
            print('Go cloud.')
            op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            op.add_argument("--no-sandbox")  # required by heroku
            op.add_argument("--disable-dev-sh-usage")        
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op) # on cloud

        # op = webdriver.ChromeOptions()
        # op.add_argument("--headless")  # set headless chrome
        # # op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # # op.add_argument("--no-sandbox")  # required by heroku
        # # op.add_argument("--disable-dev-sh-usage")
        
        # # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)  # on cloud
        # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=op)  # on local
        driver.set_window_size(1920, 1000)
        wait = WebDriverWait(driver, 10, poll_frequency=1)

        # get subjects
        # driver.get("https://sa.ucla.edu/ro/public/soc")
        # time.sleep(3)
        # input_box = driver.find_element_by_xpath('//*[@id="select_filter_subject"]')
        # ActionChains(driver).move_to_element(input_box).click(input_box).perform()
        # time.sleep(1)
        # ul = driver.find_element_by_id('dropdownitems')
        # subjects = ul.find_elements_by_tag_name("div")
        # for subject in subjects:
        #     print(subject.text)
        #     Subject.objects.update_or_create(name=subject.text)

        # get courses
        subjects = Subject.objects.order_by('name')
        should_start = False
        for i, subject in enumerate(subjects):
            print('##########################################################')
            print(subject.name)

            if should_start:
                get_course_info(subject, driver, wait)
            elif subject.name == START_SUB:
                should_start = True
                get_course_info(subject, driver, wait)

            if i == -1:
                break
        time.sleep(4)
