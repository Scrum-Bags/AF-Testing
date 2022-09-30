from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time, random, traceback, logging

from AF_Locators import *

class BasePage:
    def __init__(self, driver):
        self.driver = driver

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

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.getstarted_btn = self.driver.find_element(*HomePageLocators.By_getstarted_btn)
        logging.getLogger(self.driver.loggingID).info("Loaded Home page")

    def click_getstarted(self):
        self.getstarted_btn.click()
        self.wait_for_element(self, SignupLocators_1.By_last_name_field)
        logging.getLogger(self.driver.loggingID).info("Clicked signup button")

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
        logging.getLogger(self.driver.loggingID).info("Set " + element.get_attribute('id') + " to " + str(value))

    def select_from_dropdown(self, element, index):
        select = Select(element)
        select.select_by_index(int(index))
        logging.getLogger(self.driver.loggingID).info("Set " + element.get_attribute('id') + " to " + select.first_selected_option.text)

    def click_next(self):
        if self.driver.responsive == True:
            #self.driver.execute_script("arguments[0].scrollIntoView(true)", self.next_btn)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.3)
        self.driver.find_element(*BaseSignupPageLocators.By_next_btn).click()
        logging.getLogger(self.driver.loggingID).info("Clicked next button")
    
    def click_back(self, locatorToWaitFor):
        self.driver.find_element(*BaseSignupPageLocators.By_back_btn).click()
        self.wait_for_element(self, locatorToWaitFor)
        logging.getLogger(self.driver.loggingID).info("Clicked back button")

class SignupPage_1(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, driver.find_element(*SignupLocators_1.By_first_name_field))
        super().__init__(driver)
        self.first_name = self.driver.find_element(*SignupLocators_1.By_first_name_field)
        self.last_name = self.driver.find_element(*SignupLocators_1.By_last_name_field)
        self.email = self.driver.find_element(*SignupLocators_1.By_email_field)
        logging.getLogger(self.driver.loggingID).info("Loaded Signup page 1")

class SignupPage_2(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, driver.find_element(*SignupLocators_2.By_spending_btn))
        super().__init__(driver)
        self.spending_btn = self.driver.find_element(*SignupLocators_2.By_spending_btn)
        self.stashing_btn = self.driver.find_element(*SignupLocators_2.By_stashing_btn)
        self.both_btn = self.driver.find_element(*SignupLocators_2.By_both_btn)
        logging.getLogger(self.driver.loggingID).info("Loaded Signup page 2")

    def select_account_type(self, value):
        match str(value):
            case "STASHING":
                self.stashing_btn.click()
                logging.getLogger(self.driver.loggingID).info("Selected STASHING account type")
            case "SPENDING":
                self.spending_btn.click()
                logging.getLogger(self.driver.loggingID).info("Selected SPENDING account type")
            case "BOTH":
                self.both_btn.click()
                logging.getLogger(self.driver.loggingID).info("Selected BOTH account type")

class SignupPage_3(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, driver.find_element(*SignupLocators_3.By_DOB_field))
        super().__init__(driver)
        self.DOB_field = self.driver.find_element(*SignupLocators_3.By_DOB_field)
        self.gender_select = self.driver.find_element(*SignupLocators_3.By_gender_select)
        self.phone_field = self.driver.find_element(*SignupLocators_3.By_phone_field)
        logging.getLogger(self.driver.loggingID).info("Loaded Signup page 3")

class SignupPage_4(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, driver.find_element(*SignupLocators_4.By_SSN_field))
        super().__init__(driver)
        self.SSN_field = self.driver.find_element(*SignupLocators_4.By_SSN_field)
        self.drivers_field = self.driver.find_element(*SignupLocators_4.By_drivers_field)
        logging.getLogger(self.driver.loggingID).info("Loaded Signup page 4")

class SignupPage_5(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, driver.find_element(*SignupLocators_5.By_income_field))
        super().__init__(driver)
        self.income_field = self.driver.find_element(*SignupLocators_5.By_income_field)
        self.pay_freq_select = self.driver.find_element(*SignupLocators_5.By_pay_freq_select)
        logging.getLogger(self.driver.loggingID).info("Loaded Signup page 5")

class SignupPage_6(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, driver.find_element(*SignupLocators_6.By_address_field))
        super().__init__(driver)
        self.address_field = self.driver.find_element(*SignupLocators_6.By_address_field)
        self.city_field = self.driver.find_element(*SignupLocators_6.By_city_field)
        self.state_select = self.driver.find_element(*SignupLocators_6.By_state_select)
        self.zipcode_field = self.driver.find_element(*SignupLocators_6.By_zipcode_field)
        logging.getLogger(self.driver.loggingID).info("Loaded Signup page 6")

class SignupPage_7(BaseSignupPage):
    def __init__(self, driver):
        self.wait_for_element(self, driver.find_element(*SignupLocators_7.By_yes_radio))
        super().__init__(driver)
        self.yes_radio = self.driver.find_element(*SignupLocators_7.By_yes_radio)
        self.no_radio = self.driver.find_element(*SignupLocators_7.By_no_radio)
        logging.getLogger(self.driver.loggingID).info("Loaded Signup page 7")

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

class ApprovalPage(BasePage):
    pass
    

