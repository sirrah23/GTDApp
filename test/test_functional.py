import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from GTDApp import app
from GTDApp.repo import UserRepo
from utils import drop_db


URL = "http:localhost:5000"  # Location of our application
DB = app.config["DBNAME"]  # Database containing our test data


# Headless browser options
opts = Options()
opts.add_argument("--headless")

class TestMainPage:

    def setup_method(self, method):
        self.driver = webdriver.Firefox(firefox_options=opts)

    def test_can_hit_main_page(self):
        self.driver.get(URL)
        assert "GTD App" in self.driver.title

    def teardown_method(self, method):
        self.driver.quit()


class TestLoginAndGo:

    def setup_method(self, method):
        # User details
        self.username = "user1"
        self.password = "mypass"
        self.email = "user@gtd.com"
        # Create a user id that we can use to log in
        UserRepo.connect(DB)
        UserRepo.add_user(username=self.username, password=self.password, email=self.email)
        # Set up the driver so we can use the browser
        self.driver = webdriver.Firefox(firefox_options=opts)

    def test_log_in_and_add_item(self):
        self.driver.get(URL)
        # Get username and password elements
        userelem = self.driver.find_element_by_name("username")
        passwordelem = self.driver.find_element_by_name("password")
        # Type in username and password so we can log in
        userelem.clear()
        userelem.send_keys(self.username)
        passwordelem.clear()
        passwordelem.send_keys(self.password)
        passwordelem.send_keys(Keys.RETURN)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "app"))
            )
        except:
            self.driver.quit()
            drop_db(DB)
            assert False  # Website did not load upon clicking link
        # Find the input where we can enter items 
        input_box = self.driver.find_element_by_tag_name("input")
        input_box.send_keys("Item 1")
        input_box.send_keys(Keys.RETURN)
        time.sleep(0.5) # Let the post request go through
        # Make sure the item is in the list of items
        item_list_content = [el.text for el in self.driver.find_elements_by_class_name("gtd-item")]
        assert len(item_list_content) == 1
        assert item_list_content[0] == "Item 1"

    def test_log_in_and_add_task(self):
        self.driver.get(URL)
        # Get username and password elements
        userelem = self.driver.find_element_by_name("username")
        passwordelem = self.driver.find_element_by_name("password")
        # Type in username and password so we can log in
        userelem.clear()
        userelem.send_keys(self.username)
        passwordelem.clear()
        passwordelem.send_keys(self.password)
        passwordelem.send_keys(Keys.RETURN)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "app"))
            )
        except:
            self.driver.quit()
            drop_db(DB)
            assert False  # Website did not load upon clicking link
        # Find the button to change screens and go to the task screen
        screenforward_elem = self.driver.find_element_by_id("screenforward")
        screenforward_elem.click()
        screenforward_elem.click()
        # Find the input where we can enter tasks
        input_box = self.driver.find_element_by_tag_name("input")
        input_box.send_keys("Task 1")
        input_box.send_keys(Keys.RETURN)
        time.sleep(0.5) # Let the post request go through
        # Make sure we have zero items and one task
        item_list_content = [el.text for el in self.driver.find_elements_by_class_name("gtd-item")]
        task_list_content = [el.text for el in self.driver.find_elements_by_class_name("gtd-task")]
        assert len(item_list_content) == 0
        assert len(task_list_content) == 1
        assert task_list_content[0].startswith("Task 1") == True

    def teardown_method(self, method):
        # Closer the browser
        self.driver.quit()
        # Dump the test database contents
        drop_db(DB)
