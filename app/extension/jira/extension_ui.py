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
            
             # account login
             # input data into username field(admin)
             #page.get_element((By.ID, "login-form-username")).send_keys("admin")
             #attr_username = page.get_element((By.ID, "login-form-username")).get_attribute('value')
             #assert attr_username == "admin"

             # input data into password field(admin)
             #page.get_element((By.ID, "login-form-password")).send_keys("admin")
             #attr_password = page.get_element((By.ID, "login-form-password")).get_attribute('value')
             #assert attr_password == "admin"

             # click button "Login In"
             #attr_button_login = page.get_element((By.ID, "login-form-submit")).get_attribute('value')
             #assert attr_button_login == "Log In"
             #page.get_element((By.ID, "login-form-submit")).click()

             # wait for summary field visible
             page.wait_until_present((By.ID, 'summary-val'))
             summary_val_text = page.get_element((By.ID, 'summary-val')).text
             assert summary_val_text == "SEL-1"

             # click on dropdown menu Jira Administration
             page.wait_until_present((By.ID, 'admin_menu'))
             page.get_element((By.ID, 'admin_menu')).click()

             # click on admin plugins menu(Manage apps)
             page.wait_until_present((By.ID, 'admin_plugins_menu'))
             page.get_element((By.ID, "admin_plugins_menu")).click()

             # input password(admin) into Administrator Access
             #page.get_element((By.ID, "login-form-authenticatePassword")).send_keys("admin")
             #attr_password_auth = page.get_element((By.ID, "login-form-authenticatePassword")).get_attribute('value')
             #assert attr_password_auth == 'admin'

             # click on button Confirm
             #attr_button_auth = page.get_element((By.ID, "login-form-submit")).get_attribute('value')
             #assert attr_button_auth == "Confirm"
             #page.get_element((By.ID, "login-form-submit")).click()

             # click on link Smart Field Configuration
             configuration_text = page.get_element((By.ID, "smart-fields-config-link")).text
             assert configuration_text == "Configuration"
             page.get_element((By.ID, "smart-fields-config-link")).click()


             # click on link of our new smart field
             text_name_sf = page.get_element((By.CSS_SELECTOR, "#smart-fields-list > tbody > tr > td:nth-child(2) > a")).text
             assert text_name_sf == "Single Buffered"
             page.get_element((By.CSS_SELECTOR, "#smart-fields-list > tbody > tr > td:nth-child(2) > a")).click()

             # fill out Datasourse URL field
             url_attr = page.get_element((By.ID, 'datasource-url')).get_attribute('value')
             assert url_attr == 'https://jsonplaceholder.typicode.com/posts'

             # fill out Datasource Timeout field
             timeout_attr = page.get_element((By.ID, 'datasource-request-timeout')).get_attribute('value')
             assert timeout_attr == '1'

             # fill out Key element field
             key_el_attr = page.get_element((By.ID, 'datasource-json-element-id')).get_attribute('value')
             assert key_el_attr == 'id'

             # fill out View template field
             view_template_attr = page.get_element((By.ID, 'datasource-json-template-element-value')).get_attribute('value')
             assert view_template_attr == '{id}'

             # click on button Check connection

             chk_conn_btn_text = page.get_element((By.ID, 'check-connection')).text
             assert chk_conn_btn_text == 'Check connection'
             page.get_element((By.ID, 'check-connection')).click()

             # check that connection - success
             page.wait_until_any_ec_text_presented_in_el((By.ID, 'check-connection-success'),  'SUCCESS')
             success_text = page.get_element((By.ID, 'check-connection-success')).text
             assert success_text == 'SUCCESS'

             # fill out Input prompt field
             input_prompt_attr = page.get_element((By.ID, 'field-placeholder')).get_attribute('value')
             assert input_prompt_attr == 'enter 42'

             # fill out No result text
             no_result_text_attr = page.get_element((By.ID, 'field-no-results-massage')).get_attribute('value')
             assert no_result_text_attr == 'No result'

             # click on button Update values
             update_values_btn_text = page.get_element((By.ID, 'put-data-items-in-buffer')).text
             assert update_values_btn_text == 'Update values'
             page.get_element((By.ID, 'put-data-items-in-buffer')).click()

             # check that Data Loaded
             page.wait_until_any_ec_text_presented_in_el((By.CSS_SELECTOR, '#check-buffering-success'), 'DATA LOADED')
             data_loaded_text = page.get_element((By.CSS_SELECTOR, '#check-buffering-success')).text
             assert data_loaded_text == 'DATA LOADED'

             # click on button Run test
             run_test_btn_text = page.get_element((By.ID, 'run-test-smart-field')).text
             assert run_test_btn_text == 'Run test'
             page.get_element((By.ID, 'run-test-smart-field')).click()

             # check information in result
             # url
             page.wait_until_any_ec_text_presented_in_el((By.ID, 'link-url-request'), 'https://jsonplaceholder.typicode.com/posts')
             url_text = page.get_element((By.ID, 'link-url-request')).text
             assert url_text == 'https://jsonplaceholder.typicode.com/posts'

             # status 200
             page.wait_until_any_ec_text_presented_in_el((By.ID, 'test-request-status'), '200')
             status_text = page.get_element((By.ID, 'test-request-status')).text
             assert status_text == '200'

             # response phrase
             page.wait_until_any_ec_text_presented_in_el((By.ID, 'test-request-response-phrase'), 'OK')
             response_text = page.get_element((By.ID, 'test-request-response-phrase')).text
             assert response_text == 'OK'

             # input 42 into test field
             page.wait_until_present((By.CSS_SELECTOR, '.select2-selection__placeholder'))
             page.get_element((By.CSS_SELECTOR, '.select2-selection__placeholder')).click()
             page.wait_until_present((By.CSS_SELECTOR, '.select2-search__field'))
             page.get_element((By.CSS_SELECTOR, '.select2-search__field')).send_keys('42')
             page.get_element((By.CSS_SELECTOR, '.select2-search__field')).send_keys(Keys.ENTER)
             input_text = page.get_element((By.CSS_SELECTOR, '.select2-selection__rendered')).text
             assert input_text == '42'

             # click on save button
             save_btn_text = page.get_element((By.ID, 'save-smart-field-configuration')).get_attribute('value')
             assert save_btn_text == 'Save'
             page.get_element((By.ID, 'save-smart-field-configuration')).click()

             # notification "success"
             page.wait_until_present((By.CSS_SELECTOR, '#smart-field-massage-bar > div'))
             notif = page.get_element((By.CSS_SELECTOR, '#smart-field-massage-bar > div')).text
             assert notif == 'Configuration was successfully saved!'


             # click on link "Projects"
             projects_text = page.get_element((By.ID, 'browse_link')).text
             assert projects_text == "Projects"
             page.get_element((By.ID, 'browse_link')).click()

             # click on "View All Projects"
             page.wait_until_present((By.ID, 'project_view_all_link_lnk'))
             view_all_text = page.get_element((By.ID, 'project_view_all_link_lnk')).text
             assert view_all_text == "View All Projects"
             page.get_element((By.ID, 'project_view_all_link_lnk')).click()

             # input name of our project
             page.wait_until_present((By.ID, 'project-filter-text'))
             page.get_element((By.ID, 'project-filter-text')).send_keys('SeleniumTest')
             attr_project_sel = page.get_element((By.ID, 'project-filter-text')).get_attribute('value')
             assert attr_project_sel == "SeleniumTest"

             # click on link SeleniumTest
             page.wait_until_any_ec_text_presented_in_el((By.CSS_SELECTOR, '#projects > div > table > tbody > tr > td.cell-type-name > a'), 'SeleniumTest')
             project_sel_text = page.get_element((By.CSS_SELECTOR, '#projects > div > table > tbody > tr > td.cell-type-name > a')).text
             assert project_sel_text == "SeleniumTest"
             page.get_element((By.CSS_SELECTOR, '#projects > div > table > tbody > tr > td.cell-type-name > a')).click()

             # click on Edit button on  our issue
             page.wait_until_present((By.ID, 'edit-issue'))
             edit_button_text = page.get_element((By.ID, 'edit-issue')).text
             assert edit_button_text == "Edit"
             page.get_element((By.ID, 'edit-issue')).click()

             # click on Configure Fields
             page.wait_until_present((By.ID, 'qf-field-picker-trigger'))
             config_fields_text = page.get_element((By.ID, 'qf-field-picker-trigger')).text
             assert config_fields_text == "Configure Fields"
             page.get_element((By.ID, 'qf-field-picker-trigger')).click()


             # click on checkbox Single Buffered
             page.get_element((By.CSS_SELECTOR, '#qf-fieldpicker-inline > div > div > div.qf-picker-content > fieldset > ul > li:nth-child(13) > label > input[type=checkbox]')).click()

             # input 42 into smart field
             page.wait_until_present((By.CSS_SELECTOR, '.select2-selection__placeholder'))
             page.get_element((By.CSS_SELECTOR, '.select2-selection__placeholder')).click()
             page.wait_until_present((By.CSS_SELECTOR, '.select2-search__field'))
             page.get_element((By.CSS_SELECTOR, '.select2-search__field')).send_keys('42')
             page.get_element((By.CSS_SELECTOR, '.select2-search__field')).send_keys(Keys.ENTER)
             input_field_text = page.get_element((By.CSS_SELECTOR, '.select2-selection__rendered')).text
             assert input_field_text == '42'

             # click on button "Update"
             update_button_text = page.get_element((By.ID, 'edit-issue-submit')).get_attribute('value')
             assert update_button_text == "Update"
             page.get_element((By.ID, 'edit-issue-submit')).click()

             # check title of our new smart filed
             page.wait_until_present((By.CSS_SELECTOR, '#rowForcustomfield_11133 > div > strong'))
             sf_text = page.get_element((By.CSS_SELECTOR, '#rowForcustomfield_11133 > div > strong')).text
             assert sf_text == 'Single Buffered:'

             # check custom field value
             page.wait_until_present((By.ID, 'customfield_11133-val'))
             value_text = page.get_element((By.ID, 'customfield_11133-val')).text
             assert value_text == '42'

             # change value of custom field
             page.get_element((By.ID, 'customfield_11133-val')).click()
             page.wait_until_present((By.ID, 'select2-customfield_11133-container'))
             page.get_element((By.ID, 'select2-customfield_11133-container')).click()
             page.wait_until_present((By.CSS_SELECTOR, '.select2-search__field'))
             page.get_element((By.CSS_SELECTOR, '.select2-search__field')).send_keys('97')
             page.get_element((By.CSS_SELECTOR, '.select2-search__field')).send_keys(Keys.ENTER)
             page.get_element((By.CSS_SELECTOR, '#customfield_11133-form > div.save-options > button.aui-button.submit')).click()
             page.wait_until_any_ec_text_presented_in_el((By.ID, 'customfield_11133-val'), '97')
         
         sub_measure()
    measure()
