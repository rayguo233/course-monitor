from django.core.management.base import BaseCommand
from selenium import webdriver
import os
import time

class Command(BaseCommand):
    help = "collect courses"

    # define logic of command
    def handle(self, *args, **options):
        op = webdriver.ChromeOptions()
        op.add_argument("--headless")
        # see if the script is being run on cloud or local
        if os.environ.get("GOOGLE_CHROME_BIN") is None:
            # on local
            print('Go local.')
            driver = webdriver.Chrome(chrome_options=op) 
        else:
            # on cloud
            print('Go cloud.')
            op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            op.add_argument("--no-sandbox")  # required by heroku
            op.add_argument("--disable-dev-sh-usage")        
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op) # on cloud
        
        # op = webdriver.ChromeOptions()
        # op.add_argument("--headless")  # set headless chrome
        

        driver.get("https://course-monitor.herokuapp.com/")
        print("Pin the website.")
        time.sleep(1800) # 30 minutes
        print("Finished pinning.")
