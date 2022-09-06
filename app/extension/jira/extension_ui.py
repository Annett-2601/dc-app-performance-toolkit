import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

#     To run action as specific user uncomment code bellow.
#     NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
#     just before test_2_selenium_z_log_out action
    
    @print_timing("selenium_app_specific_user_login")
    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.set_credentials(username=username, password=password)
            if login_page.is_first_login():
                login_page.first_login_setup()
            if login_page.is_first_login_second_page():
                login_page.first_login_second_page_setup()
            login_page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')
    measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            
            # click on link Smart Field Configuration
            configuration_text = page.get_element((By.ID, "smart-fields-config-link")).text
            assert configuration_text == "Configuration"
            page.get_element((By.ID, "smart-fields-config-link")).click()
            
            # click on button Create Smart Field
            page.get_element((By.ID, "add-new-field-button")).click()
            
            # fill out the form for creating a new smart field
            # input data into name field
            page.get_element((By.ID, "smart-field-name")).send_keys("1 Single/Buffered")
            attr_name = page.get_element((By.ID, "smart-field-name").get_attribute("value")
            assert attr_name == "1 Single/Buffered"
                                         
            # input data into description
            page.get_element((By.ID, "smart-field-description")).send_keys("Selenium Test")
            attr_description = page.get_element((By.ID, "smart-field-description")).get_attribute("value")
            assert attr_description == "Selenium Test"
            
        sub_measure()
    measure()

