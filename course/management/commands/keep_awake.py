from django.core.management.base import BaseCommand
from selenium import webdriver
import os
import time

class Command(BaseCommand):
    help = "collect courses"

    # define logic of command
    def handle(self, *args, **options):
        op = webdriver.ChromeOptions()
        op.add_argument("--headless")  # set headless chrome
        # op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # op.add_argument("--no-sandbox")  # required by heroku
        # op.add_argument("--disable-dev-sh-usage")
        
        # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)  # on cloud
        driver = webdriver.Chrome(chrome_options=op) # on local

        for i in range(3):
            driver.get("https://course-monitor.herokuapp.com/")
            print("Pin the website the " + str(i+1) + " time.")
            time.sleep(1020) # 17 minutes
