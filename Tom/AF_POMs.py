from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time, random, traceback, logging

from AF_Locators import *
from AF_Utilities import *
from TestSuiteReporter import TestSuiteReporter

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.testID = self.driver.testID
        self.reporter = self.driver.reporter

    @staticmethod
    def wait_for_element(self, locator, timeout = 20):
        try: 
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except:
            return False
        else:
            return True
    
    @staticmethod
    def wait_for_element_disappear(self, locator, timeout = 20):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except:
            return False
        else:
            return True

    def tab_outside(self):
        self.driver.find_element(By.XPATH, '//body').send_keys(Keys.TAB)

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.getstarted_btn = self.driver.find_element(*HomePageLocators.By_getstarted_btn)
        logging.getLogger(self.driver.loggingID).info("Loaded Home page")

    def click_getstarted(self):
        self.getstarted_btn.click()
        self.wait_for_element(self, SignupLocators_1.By_last_name_field)
        logging.getLogger(self.driver.loggingID).info("Clicked signup button")
        self.reporter[self.testID].reportEvent("Clicked signup button", False, "")


class BaseSignupPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.next_btn = self.driver.find_element(*BaseSignupPageLocators.By_next_btn)
        try:
            self.back_btn = self.driver.find_element(*BaseSignupPageLocators.By_back_btn)
        except: #will pass on first page that doesn't have back button
            pass

    def set_text_field(self, element, value):
        element.clear()
        element.click()
        element.send_keys(str(value))
        report_event_and_log(
            self.driver, 
            "Set [" + element.get_attribute('id') + "]" + " to [" + str(value) + "]",
        )


    def select_from_dropdown(self, element, index):
        select = Select(element)
        select.select_by_index(int(index))
        report_event_and_log(
            self.driver,
            "Set [" + element.get_attribute('id') + "]" + " to [" + select.first_selected_option.text + "]"
        )

    def click_next(self):
        if self.driver.responsive == True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.3)
        self.driver.find_element(*BaseSignupPageLocators.By_next_btn).click()
        report_event_and_log(
            self.driver,
            "Clicked 'next' button"
        )

    def click_back(self, locatorToWaitFor):
        self.driver.find_element(*BaseSignupPageLocators.By_back_btn).click()
        self.wait_for_element(self, locatorToWaitFor)
        logging.getLogger(self.driver.loggingID).info("Clicked back button")
        report_event_and_log(
            self.driver,
            "Clicked 'back' button"
        )

class SignupPage_1(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, SignupLocators_1.By_first_name_field)
        super().__init__(driver)
        self.first_name = self.driver.find_element(*SignupLocators_1.By_first_name_field)
        self.last_name = self.driver.find_element(*SignupLocators_1.By_last_name_field)
        self.email = self.driver.find_element(*SignupLocators_1.By_email_field)
        report_event_and_log(self.driver, "Loaded Signup page 1")

    def fill_page_and_submit(self, firstname, lastname, email):
        self.set_text_field(self.first_name, firstname)
        self.set_text_field(self.last_name, lastname)
        self.set_text_field(self.email, email)
        if self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is enabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
            self.click_next()
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is disabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

    def fill_page_negative(self, firstname, lastname, email):
        self.set_text_field(self.first_name, firstname)
        self.set_text_field(self.last_name, lastname)
        self.set_text_field(self.email, email)
        if not self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is not enabled",
                "Next button is not enabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is enabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

        

class SignupPage_2(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, SignupLocators_2.By_spending_btn)
        super().__init__(driver)
        self.spending_btn = self.driver.find_element(*SignupLocators_2.By_spending_btn)
        self.stashing_btn = self.driver.find_element(*SignupLocators_2.By_stashing_btn)
        self.both_btn = self.driver.find_element(*SignupLocators_2.By_both_btn)
        report_event_and_log(self.driver, "Loaded Signup page 2")

    def fill_page_and_submit(self, account_type):
        self.select_account_type(account_type)
        if self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is enabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
            self.click_next()
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is disabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

    def fill_page_negative(self):
        if not self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled without selecting account type",
                "Next button is disabled",
                "Next button is disabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled without selecting account type",
                "Next button is disabled",
                "Next button is enabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            ) 

    def select_account_type(self, value):
        match str(value):
            case "STASHING":
                self.stashing_btn.click()
                report_event_and_log(self.driver, "Selected STASHING account type")
            case "SPENDING":
                self.spending_btn.click()
                report_event_and_log(self.driver, "Selected SPENDING account type")
            case "BOTH":
                self.both_btn.click()
                report_event_and_log(self.driver, "Selected BOTH account type")


class SignupPage_3(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, SignupLocators_3.By_DOB_field)
        super().__init__(driver)
        self.DOB_field = self.driver.find_element(*SignupLocators_3.By_DOB_field)
        self.gender_select = self.driver.find_element(*SignupLocators_3.By_gender_select)
        self.phone_field = self.driver.find_element(*SignupLocators_3.By_phone_field)
        report_event_and_log(self.driver, "Loaded Signup page 3")

    def fill_page_and_submit(self, DOB, gender, phone):
        self.set_text_field(self.DOB_field, DOB)
        self.select_from_dropdown(self.gender_select, gender)
        self.set_text_field(self.phone_field, phone)
        if self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is enabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
            self.click_next()
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is disabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

    def fill_page_negative(self, DOB, gender, phone):
        self.set_text_field(self.DOB_field, DOB)
        self.select_from_dropdown(self.gender_select, 1) #to trigger error if we're testing gender field
        self.select_from_dropdown(self.gender_select, gender)
        self.set_text_field(self.phone_field, phone)
        if not self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled after filling fields", 
                "Next button is disabled",
                "Next button is disabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled after filling fields", 
                "Next button is disabled",
                "Next button is enabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

class SignupPage_4(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, SignupLocators_4.By_SSN_field)
        super().__init__(driver)
        self.SSN_field = self.driver.find_element(*SignupLocators_4.By_SSN_field)
        self.drivers_field = self.driver.find_element(*SignupLocators_4.By_drivers_field)
        report_event_and_log(self.driver, "Loaded Signup page 4")

    def fill_page_and_submit(self, SSN, drivers):
        self.set_text_field(self.SSN_field, SSN)
        self.set_text_field(self.drivers_field, drivers)
        if self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is enabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
            self.click_next()
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is disabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

    def fill_page_negative(self, SSN, drivers):
        self.set_text_field(self.SSN_field, SSN)
        self.set_text_field(self.drivers_field, drivers)
        if not self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled after filling fields", 
                "Next button is disabled",
                "Next button is disabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled after filling fields", 
                "Next button is disabled",
                "Next button is enabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )


class SignupPage_5(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, SignupLocators_5.By_income_field)
        super().__init__(driver)
        self.income_field = self.driver.find_element(*SignupLocators_5.By_income_field)
        self.pay_freq_select = self.driver.find_element(*SignupLocators_5.By_pay_freq_select)
        report_event_and_log(self.driver, "Loaded Signup page 5")

    def fill_page_and_submit(self, income, pay_freq):
        self.set_text_field(self.income_field, income)
        self.select_from_dropdown(self.pay_freq_select, pay_freq)
        if self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is enabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
            self.click_next()
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is disabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

    def fill_page_negative(self, income, pay_freq):
        self.set_text_field(self.income_field, income)
        self.select_from_dropdown(self.pay_freq_select, pay_freq)
        if not self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled after filling fields", 
                "Next button is disabled",
                "Next button is disabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled after filling fields", 
                "Next button is disabled",
                "Next button is enabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )


class SignupPage_6(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, SignupLocators_6.By_address_field)
        super().__init__(driver)
        self.address_field = self.driver.find_element(*SignupLocators_6.By_address_field)
        self.city_field = self.driver.find_element(*SignupLocators_6.By_city_field)
        self.state_select = self.driver.find_element(*SignupLocators_6.By_state_select)
        self.zipcode_field = self.driver.find_element(*SignupLocators_6.By_zipcode_field)
        report_event_and_log(self.driver, "Loaded Signup page 6")

    def fill_page_and_submit(self, address, city, state, zip):
        self.set_text_field(self.address_field, address)
        self.set_text_field(self.city_field, city)
        self.select_from_dropdown(self.state_select, state)
        self.set_text_field(self.zipcode_field, zip)
        if self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is enabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
            self.click_next()
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is disabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

    def fill_page_negative(self, address, city, state, zip):
        self.set_text_field(self.address_field, address)
        self.set_text_field(self.city_field, city)
        self.select_from_dropdown(self.state_select, 1)
        self.select_from_dropdown(self.state_select, state)
        self.set_text_field(self.zipcode_field, zip)
        if not self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled after filling fields", 
                "Next button is disabled",
                "Next button is disabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is disabled after filling fields", 
                "Next button is disabled",
                "Next button is enabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

class SignupPage_7(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, SignupLocators_7.By_yes_radio)
        super().__init__(driver)
        self.yes_radio = self.driver.find_element(*SignupLocators_7.By_yes_radio)
        self.no_radio = self.driver.find_element(*SignupLocators_7.By_no_radio)
        report_event_and_log(self.driver, "Loaded Signup page 7")

    def click_yes_no(self, value):
        match value:
            case "YES":
                pass
            case "NO":
                self.no_radio.click()
                self.address = self.driver.find_element(*SignupLocators_7.By_mailing_address_field)
                self.city = self.driver.find_element(*SignupLocators_7.By_mailing_city_field)
                self.state = self.driver.find_element(*SignupLocators_7.By_mailing_state_field)
                self.zipcode = self.driver.find_element(*SignupLocators_7.By_mailing_zip_field)
                report_event_and_log(self.driver, "Selected NO for 'same mailing address'")

    def fill_page_and_submit(self, radio_op, address, city, state, zip):
        self.click_yes_no(radio_op)
        if radio_op == "NO":
            self.set_text_field(self.address, address)
            self.set_text_field(self.city, city)
            self.select_from_dropdown(self.state, state)
            self.set_text_field(self.zipcode, zip)
        if self.next_btn.is_enabled():
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is enabled",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
            self.click_next()
        else:
            self.driver.reporter[self.driver.testID].reportStep(
                "Check if next button is enabled after filling fields", 
                "Next button is enabled",
                "Next button is disabled",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )

    def fill_page_negative(self, radio_op, address, city, state, zip):
        pass

class ApprovalPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_element(self, ApprovalPageLocators.By_thank_you_message, 120)
        report_event_and_log(self.driver, "Loaded Approval Page")

    def check_approval_message(self):
        print(self.driver.find_element(*ApprovalPageLocators.By_approval_text).get_attribute('textContent'))

    
    

