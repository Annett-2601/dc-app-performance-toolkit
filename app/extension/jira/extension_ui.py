import random

from selenium.webdriver.common.keys import Keys

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
#     NOTE:If app_specific_action is running as specific user, make sure that app_specific_action is running
#     just before test_2_selenium_z_log_out action
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

             # wait for summary field visible
             page.wait_until_present((By.ID, 'summary-val'))
             summary_val_text = page.get_element((By.ID, 'summary-val')).text
             assert summary_val_text == "SEL-1"

             # click on Edit button on  our issue
             page.wait_until_present((By.ID, 'edit-issue'))
             edit_button_text = page.get_element((By.ID, 'edit-issue')).text
             assert edit_button_text == "Edit"
             page.get_element((By.ID, 'edit-issue')).click()

             # input 42 into smart field
             page.wait_until_present((By.CSS_SELECTOR, '.field-group > .select2'))
             page.get_element((By.CSS_SELECTOR, '.field-group > .select2')).click()
             page.wait_until_present((By.CSS_SELECTOR, '.select2-dropdown > .select2-search > input'))
             page.get_element((By.CSS_SELECTOR, '.select2-dropdown > .select2-search > input')).send_keys('42')
             page.get_element((By.CSS_SELECTOR, '.select2-dropdown > .select2-search > input')).send_keys(Keys.ENTER)
             input_field_text = page.get_element((By.ID, 'select2-customfield_11100-container')).text
             assert input_field_text == '42'

             # click on button "Update"
             update_button_text = page.get_element((By.ID, 'edit-issue-submit')).get_attribute('value')
             assert update_button_text == "Update"
             page.get_element((By.ID, 'edit-issue-submit')).click()

         sub_measure()
    measure()
