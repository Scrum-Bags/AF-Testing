from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time, random, unittest, logging, sys

from AF_POMs import *

from TestSuiteReporter import TestSuiteReporter
from ExcelReader import excelReader

class AF_Register_Bank_Member(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AF_Register_Bank_Member, self).__init__(*args, **kwargs)
        self.timestr = time.strftime("%Y-%m-%d--%I_%M_%S%p")
        self.reporter = TestSuiteReporter(self.timestr, "./", "Tom")
        logging.basicConfig(level=logging.INFO,
                            handlers=[
                                logging.FileHandler("AF_Register_Bank_Member" + self.timestr + ".log"),
                                logging.StreamHandler()
                            ],
                            format= '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S'
        )

    @classmethod
    def setUpClass(cls):
        cls.edge_options = Options()
        cls.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #cls.edge_options.headless = True
        cls.driver = webdriver.Edge(options=cls.edge_options)
        cls.driver.loggingID = "AF_Register_Bank_Member"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("http://uftcapstone-dev-landing.s3-website-us-east-1.amazonaws.com/")
        logging.getLogger(self.driver.loggingID).info("Waiting for home page to load")
        BasePage.wait_for_element(self, HomePageLocators.By_getstarted_btn, 30)

    def test_TH_TC001(self):
        logging.getLogger(self.driver.loggingID).info("***BEGINNING TH_TC001 [Non-responsive]***")
        self.testID = "TC001_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.testID, "TH_TC001", "Test signup using valid data [Non-responsive]")
        self.TH_TC001()

    def test_TH_TC001_responsive(self):
        logging.getLogger(self.driver.loggingID).info("***BEGINNING TH_TC001 [Responsive]***")
        self.testID = "TC001_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.testID, "TH_TC001_R", "Test signup using vaid data [Responsive]")
        self.driver.set_window_size(500, 900)
        self.TH_TC001()
        
    def TH_TC001(self):
        logging.getLogger(self.driver.loggingID).info("Entered TH_TC001 main test logic")
        driver = self.driver
        reporter = self.reporter
        testID = self.testID

        logging.getLogger(driver.loggingID).info("Checking for responsive webpage")
        if driver.get_window_size()['width'] < 550:
            driver.responsive = True
            logging.getLogger(driver.loggingID).info("Detected responsive")
        else:
            driver.responsive = False
            logging.getLogger(driver.loggingID).info("Didn't detect responsive")

        page = HomePage(driver)
        page.click_getstarted()

        page = SignupPage_1(driver)
        page.set_text_field(page.first_name, "Tom") #excel
        page.set_text_field(page.last_name, "Hennessey") #excel
        page.set_text_field(page.email, "tom@tom.com") #excel
        page.click_next()

        page = SignupPage_2(driver)
        page.select_account_type("SPENDING") #excel 
        page.click_next()

        page = SignupPage_3(driver)
        page.set_text_field(page.DOB_field, "07011990") #excel
        page.select_from_dropdown(page.gender_select, "3") #excel
        page.set_text_field(page.phone_field, "1231231234") #excel
        page.click_next()

        page = SignupPage_4(driver)
        page.set_text_field(page.SSN_field, "123456789") #excel
        page.set_text_field(page.drivers_field, "S123-1234-1234") #excel
        page.click_next()

        page = SignupPage_5(driver)
        page.set_text_field(page.income_field, "123123") #excel
        page.select_from_dropdown(page.pay_freq_select, "2") #excel
        page.click_next()

        page = SignupPage_6(driver)
        page.set_text_field(page.address_field, "123 West Street") #excel
        page.set_text_field(page.city_field, "Mycity") #excel
        page.select_from_dropdown(page.state_select, "3") #excel
        page.set_text_field(page.zipcode_field, "12345") #excel
        page.click_next()

        page = SignupPage_7(driver)
        page.click_yes_no("NO") #excel
        if True: #add check for YES or NO value above
            page.set_text_field(page.address, "123 North Street") #excel
            page.set_text_field(page.city, "Myothercity") #excel
            page.select_from_dropdown(page.state, "4") #excel
            page.set_text_field(page.zipcode, "12543") #excel
        page.click_next()

        time.sleep(3)


if __name__ == "__main__":
    unittest.main()