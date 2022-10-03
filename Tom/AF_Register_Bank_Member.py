from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time, random, unittest, logging, sys

from openpyxl import load_workbook

from AF_POMs import *

from TestSuiteReporter import TestSuiteReporter
from ExcelReader import excelReader
from Outlook import Outlook_App

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
        cls.driver.currentExcelRow = 1

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("http://uftcapstone-dev-landing.s3-website-us-east-1.amazonaws.com/")
        logging.getLogger(self.driver.loggingID).info("Waiting for home page to load")
        BasePage.wait_for_element(self, HomePageLocators.By_getstarted_btn, 30)
        self.driver.currentExcelRow += 1
        self.driver.reporter = self.reporter

        #Load excel row
        wb = load_workbook(filename = 'AF_Register_Bank_Member.xlsx', data_only=True)
        sheet = wb['TH_TC001']
        self.driver.data = {}
        for i in range (1, 21):
            self.driver.data[sheet.cell(column=i, row=1).value] = sheet.cell(column=i, row=self.driver.currentExcelRow).value
        logging.getLogger(self.driver.loggingID).info("Loaded excel data")

    def tearDown(self):
        self.driver.reporter = None

    def test_TH_TC001(self):
        logging.getLogger(self.driver.loggingID).info("***BEGINNING TH_TC001 [Non-responsive]***")
        self.driver.testID = "TC001_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC001", "Test signup using valid data [Non-responsive]")
        self.TH_TC001()

    def test_TH_TC001_responsive(self):
        logging.getLogger(self.driver.loggingID).info("***BEGINNING TH_TC001 [Responsive]***")
        self.driver.testID = "TC001_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC001_R", "Test signup using vaid data [Responsive]")
        self.driver.set_window_size(500, 900)
        self.TH_TC001()
        
    def TH_TC001(self):
        logging.getLogger(self.driver.loggingID).info("Entered TH_TC001 main test logic")
        driver = self.driver
        testID = self.driver.testID

        logging.getLogger(driver.loggingID).info("Checking for responsive webpage")
        if driver.get_window_size()['width'] < 550:
            driver.responsive = True
            logging.getLogger(driver.loggingID).info("Detected responsive")
        else:
            driver.responsive = False
            logging.getLogger(driver.loggingID).info("Didn't detect responsive")

        find_and_update_email(driver, driver.data["DT_email"])

        page = HomePage(driver)
        page.click_getstarted()

        #Page 1
        page = SignupPage_1(driver)
        page.fill_page_and_submit(driver.data["DT_firstname"], driver.data["DT_lastname"], driver.data["DT_email"])

        #Page 2
        page = SignupPage_2(driver)
        page.fill_page_and_submit(driver.data["DT_account_type"])

        #Page 3
        page = SignupPage_3(driver)
        page.fill_page_and_submit(
            driver.data["DT_DOB"], 
            driver.data["DT_gender"],
            driver.data["DT_phone"]
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_and_submit(str(driver.data["DT_SSN"]), driver.data["DT_drivers"])

        #Page 5
        page = SignupPage_5(driver)
        page.fill_page_and_submit(driver.data["DT_income"], driver.data["DT_pay_freq"])

        #Page 6
        page = SignupPage_6(driver)
        page.fill_page_and_submit(
            driver.data["DT_address"],
            driver.data["DT_city"],
            driver.data["DT_state"],
            driver.data["DT_zip"]
        )

        #Page 7
        page = SignupPage_7(driver)
        page.fill_page_and_submit(
            driver.data["DT_alternate_address"],
            driver.data["DT_mailing_address"],
            driver.data["DT_mailing_city"],
            driver.data["DT_mailing_state"],
            driver.data["DT_mailing_zip"]
        )

        #Approval page
        page = ApprovalPage(driver)

        #TODO Approval page
        #TODO check email
        '''
        obj = Outlook_App()
        msg = obj.search_by_subject("Welcome", 6)
        print(msg)
        print(obj.get_body(msg))
        '''
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()