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
        self.signup_btn = self.driver.find_elements(*HomePageLocators.By_signup_btn)

