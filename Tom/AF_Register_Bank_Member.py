from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time, random, unittest, logging, sys

from openpyxl import load_workbook

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
                            format= '[%(asctime)s] %(levelname)s %(message)s',
                            datefmt='%H:%M:%S'
        )

    @classmethod
    def setUpClass(cls):
        cls.edge_options = Options()
        cls.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        cls.edge_options.headless = True
        cls.driver = webdriver.Edge(options=cls.edge_options)
        cls.driver.loggingID = "AF_Register_Bank_Member"
        cls.driver.currentExcelRow = 1

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("http://uftcapstone-dev-landing.s3-website-us-east-1.amazonaws.com/")
        log_wrapper(self.driver, "Waiting for home page to load")
        BasePage.wait_for_element(self, HomePageLocators.By_getstarted_btn, 30)
        self.driver.currentExcelRow += 1
        self.driver.reporter = self.reporter
        self.driver.set_window_size(945, 1012)

    def tearDown(self):
        self.driver.reporter = None

    ###
    def test_TH_TC001(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC001 [Non-responsive]***")
        self.driver.testID = "TC001_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC001", "Test signup using valid data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC001')
        self.TH_TC001()

    def test_TH_TC001_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC001 [Responsive]***")
        self.driver.testID = "TC001_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC001_R", "Test signup using vaid data [Responsive]")
        self.driver.set_window_size(500, 900)
        load_excel_sheet(self.driver, 'TH_TC001_R')
        self.TH_TC001()
        
    def TH_TC001(self):
        log_wrapper(self.driver, "Entered TH_TC001 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)
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
            str(driver.data["DT_phone"])
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_and_submit(str(driver.data["DT_SSN"]), str(driver.data["DT_drivers"]))

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
        page.check_approval_message()
        check_outlook_confirmation(driver, 120)

    ###

    ###
    def test_TH_TC002(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC002 [Non-responsive]***")
        self.driver.testID = "TC002_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC002", "Test signup usng invalid first name and valid last name and email [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC002')
        self.TH_TC002()

    def test_TH_TC002_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC002 [Responsive]***")
        self.driver.testID = "TC002_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC002_R", "Test signup usng invalid first name and valid last name and email [Responsive]")
        self.driver.set_window_size(500, 900)
        load_excel_sheet(self.driver, 'TH_TC002_R')
        self.TH_TC002()      

    def TH_TC002(self):
        log_wrapper(self.driver, "Entered TH_TC002 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)

        page = HomePage(driver)
        page.click_getstarted()

        #Page 1
        page = SignupPage_1(driver)
        page.fill_page_negative(
            driver.data['DT_firstname'], 
            driver.data['DT_lastname'], 
            driver.data['DT_email']
            )

        log_wrapper(driver, "Waiting for first_name error to appear...")
        if page.wait_for_element(page, SignupLocators_1.By_first_name_error):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

    ###
    def test_TH_TC003(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC003 [Non-responsive]***")
        self.driver.testID = "TC003_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC003", "Test signup using invalid last name and valid first name and email [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC003')
        self.TH_TC003()

    def test_TH_TC003_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC003 [Responsive]***")
        self.driver.testID = "TC003_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC003", "Test signup using invalid last name and valid first name and email [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC003')
        self.driver.set_window_size(500, 900)
        self.TH_TC003()

    def TH_TC003(self):
        log_wrapper(self.driver, "Entered TH_TC003 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)

        page = HomePage(driver)
        page.click_getstarted()

        #Page 1
        page = SignupPage_1(driver)
        page.fill_page_negative(
            driver.data['DT_firstname'], 
            driver.data['DT_lastname'], 
            driver.data['DT_email']
            )

        log_wrapper(driver, "Waiting for last_name error to appear...")
        if page.wait_for_element(page, SignupLocators_1.By_last_name_error):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

    ###
    def test_TH_TC004(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC004 [Non-responsive]***")
        self.driver.testID = "TC004_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC004", "Test signup using invalid email and valid first and last name [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC004')
        self.TH_TC004()

    def test_TH_TC004_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC004 [Responsive]***")
        self.driver.testID = "TC004_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC004", "Test signup using invalid email and valid first and last name [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC004')
        self.driver.set_window_size(500, 900)
        self.TH_TC004() 

    def TH_TC004(self):
        log_wrapper(self.driver, "Entered TH_TC004 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)

        page = HomePage(driver)
        page.click_getstarted()

        #Page 1
        page = SignupPage_1(driver)
        page.fill_page_negative(
            driver.data['DT_firstname'], 
            driver.data['DT_lastname'], 
            driver.data['DT_email']
            )
        page.tab_outside()

        log_wrapper(driver, "Waiting for email error to appear...")
        if page.wait_for_element(page, SignupLocators_1.By_email_error):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

    ###
    def test_TH_TC005(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC005 [Non-responsive]***")
        self.driver.testID = "TC005_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC005", "Test signup without clicking an account type [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC005')
        self.TH_TC005()

    def test_TH_TC005_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC005 [Responsive]***")
        self.driver.testID = "TC005_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC005", "Test signup without clicking an account type [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC005')
        self.driver.set_window_size(500, 900)
        self.TH_TC005()

    def TH_TC005(self):
        log_wrapper(self.driver, "Entered TH_TC005 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)
        find_and_update_email(driver, driver.data["DT_email"])

        page = HomePage(driver)
        page.click_getstarted()

        #Page 1
        page = SignupPage_1(driver)
        page.fill_page_and_submit(driver.data["DT_firstname"], driver.data["DT_lastname"], driver.data["DT_email"])

        #Page 2
        page = SignupPage_2(driver)
        page.fill_page_negative()
    ###

    ###
    def test_TH_TC006(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC006 [Non-responsive]***")
        self.driver.testID = "TC006_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC006", "Test signup using invalid DOB, valid gender, phone number, and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC006')
        self.TH_TC006()

    def test_TH_TC006_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC006 [Responsive]***")
        self.driver.testID = "TC006_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC006", "Test signup using invalid DOB, valid gender, phone number, and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC006')
        self.driver.set_window_size(500, 900)
        self.TH_TC006()

    def TH_TC006(self):
        log_wrapper(self.driver, "Entered TH_TC006 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)
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
        page.fill_page_negative(
            driver.data["DT_DOB"], 
            driver.data["DT_gender"],
            str(driver.data["DT_phone"])
        )

        log_wrapper(driver, "Waiting for DOB error to appear...")
        if page.wait_for_element(page, SignupLocators_3.By_DOB_error):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

    ###
    def test_TH_TC007(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC007 [Non-responsive]***")
        self.driver.testID = "TC007_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC007", "Test signup using no selected gender, valid DOB, phone, and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC007')
        self.TH_TC007()

    def test_TH_TC007_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC007 [Responsive]***")
        self.driver.testID = "TC007_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC007", "Test signup using no selected gender, valid DOB, phone, and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC007')
        self.driver.set_window_size(500, 900)
        self.TH_TC007()

    def TH_TC007(self):
        log_wrapper(self.driver, "Entered TH_TC007 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)
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
        page.fill_page_negative(
            driver.data["DT_DOB"], 
            driver.data["DT_gender"],
            str(driver.data["DT_phone"])
        )

        log_wrapper(driver, "Waiting for gender error to appear...")
        if page.wait_for_element(page, SignupLocators_3.By_gender_error):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

    ###
    def test_TH_TC008(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC008 [Non-responsive]***")
        self.driver.testID = "TC008_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC008", "Test signup using invalid phone number, valid gender, DOB, and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC008')
        self.TH_TC008()

    def test_TH_TC008_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC008 [Responsive]***")
        self.driver.testID = "TC008_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC008", "Test signup using invalid phone number, valid gender, DOB, and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC008')
        self.driver.set_window_size(500, 900)
        self.TH_TC008()

    def TH_TC008(self):
        log_wrapper(self.driver, "Entered TH_TC008 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)
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
        page.fill_page_negative(
            driver.data["DT_DOB"], 
            driver.data["DT_gender"],
            str(driver.data["DT_phone"])
        )
        page.tab_outside()

        log_wrapper(driver, "Waiting for phone error to appear...")
        if page.wait_for_element(page, SignupLocators_3.By_phone_error):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

    ###
    def test_TH_TC009(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC009 [Non-responsive]***")
        self.driver.testID = "TC009_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC009", "Test signup using invalid social security, valid drivers license and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC009')
        self.TH_TC009()

    def test_TH_TC009_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC009 [Responsive]***")
        self.driver.testID = "TC009_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC009", "Test signup using invalid social security, valid drivers license and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC009')
        self.driver.set_window_size(500, 900)
        self.TH_TC009()

    def TH_TC009(self):
        log_wrapper(self.driver, "Entered TH_TC009 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)
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
            str(driver.data["DT_phone"])
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_negative(str(driver.data["DT_SSN"]), str(driver.data["DT_drivers"]))

        log_wrapper(driver, "Waiting for SSN error to appear...")
        if page.wait_for_element(page, SignupLocators_4.By_SSN_error):
            self.reporter[testID].reportStep(
                "Check that error message appears",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=self.driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check that error message appears",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=self.driver.save_screenshot
            )


    ###

    ###
    def test_TH_TC010(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC010 [Non-responsive]***")
        self.driver.testID = "TC010_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC010", "Test signup using invalid drivers license, valid social security and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC010')
        self.TH_TC010()

    def test_TH_TC010_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC010 [Responsive]***")
        self.driver.testID = "TC010_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC010", "Test signup using invalid drivers license, valid social security and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC010')
        self.driver.set_window_size(500, 900)
        self.TH_TC010()

    def TH_TC010(self):
        log_wrapper(self.driver, "Entered TH_TC009 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)
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
            str(driver.data["DT_phone"])
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_negative(str(driver.data["DT_SSN"]), str(driver.data["DT_drivers"]))

    ###

    ###
    def test_TH_TC011(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC011 [Non-responsive]***")
        self.driver.testID = "TC011_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC011", "Test login using invalid income, valid frequency and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC011')
        self.TH_TC011()

    def test_TH_TC011_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC011 [Responsive]***")
        self.driver.testID = "TC011_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC011", "Test login using invalid income, valid frequency and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC011')
        self.driver.set_window_size(500, 900)
        self.TH_TC011()

    def TH_TC011(self):
        log_wrapper(self.driver, "Entered TH_TC011 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)

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
            str(driver.data["DT_phone"])
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_and_submit(str(driver.data["DT_SSN"]), str(driver.data["DT_drivers"]))

        #Page 5
        page = SignupPage_5(driver)
        page.fill_page_negative(driver.data["DT_income"], driver.data["DT_pay_freq"])

        log_wrapper(driver, "Waiting for income error to appear...")
        if page.wait_for_element(page, SignupLocators_5.By_income_error):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )

    ###

    ###
    def test_TH_TC012(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC012 [Non-responsive]***")
        self.driver.testID = "TC012_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC012", "Test signup using invalid address, valid city, state, zip, and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC012')
        self.TH_TC012()

    def test_TH_TC012_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC012 [Responsive]***")
        self.driver.testID = "TC012_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC012", "Test signup using invalid address, valid city, state, zip, and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC012')
        self.driver.set_window_size(500, 900)
        self.TH_TC012()

    def TH_TC012(self):
        log_wrapper(self.driver, "Entered TH_TC012 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)

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
            str(driver.data["DT_phone"])
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_and_submit(str(driver.data["DT_SSN"]), str(driver.data["DT_drivers"]))

        #Page 5
        page = SignupPage_5(driver)
        page.fill_page_and_submit(driver.data["DT_income"], driver.data["DT_pay_freq"])

        #Page 6
        page = SignupPage_6(driver)
        page.fill_page_negative(
            driver.data["DT_address"],
            driver.data["DT_city"],
            driver.data["DT_state"],
            driver.data["DT_zip"]
        )

        log_wrapper(driver, "Waiting for address error to appear...")
        if page.wait_for_element(page, SignupLocators_6.By_address_error):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )

    ###

    ###
    def test_TH_TC013(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC013 [Non-responsive]***")
        self.driver.testID = "TC013_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC013", "Test signup using invalid city, valid address, state, zip, and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC013')
        self.TH_TC013()

    def test_TH_TC013_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC013 [Responsive]***")
        self.driver.testID = "TC013_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC013", "Test signup using invalid city, valid address, state, zip, and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC013')
        self.driver.set_window_size(500, 900)
        self.TH_TC013()

    def TH_TC013(self):
        log_wrapper(self.driver, "Entered TH_TC013 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)

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
            str(driver.data["DT_phone"])
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_and_submit(str(driver.data["DT_SSN"]), str(driver.data["DT_drivers"]))

        #Page 5
        page = SignupPage_5(driver)
        page.fill_page_and_submit(driver.data["DT_income"], driver.data["DT_pay_freq"])

        #Page 6
        page = SignupPage_6(driver)
        page.fill_page_negative(
            driver.data["DT_address"],
            driver.data["DT_city"],
            driver.data["DT_state"],
            driver.data["DT_zip"]
        )

        log_wrapper(driver, "Waiting for city error to appear...")
        if page.wait_for_element(page, SignupLocators_6.By_city_error, 3):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

    ###
    def test_TH_TC014(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC014 [Non-responsive]***")
        self.driver.testID = "TC014_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC014", "Test signup with state unselected, valid address, city, zip, and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC014')
        self.TH_TC014()

    def test_TH_TC014_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC014 [Responsive]***")
        self.driver.testID = "TC014_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC014", "Test signup with state unselected, valid address, city, zip, and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC014')
        self.driver.set_window_size(500, 900)
        self.TH_TC014()

    def TH_TC014(self):
        log_wrapper(self.driver, "Entered TH_TC014 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)

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
            str(driver.data["DT_phone"])
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_and_submit(str(driver.data["DT_SSN"]), str(driver.data["DT_drivers"]))

        #Page 5
        page = SignupPage_5(driver)
        page.fill_page_and_submit(driver.data["DT_income"], driver.data["DT_pay_freq"])

        #Page 6
        page = SignupPage_6(driver)
        page.fill_page_negative(
            driver.data["DT_address"],
            driver.data["DT_city"],
            driver.data["DT_state"],
            driver.data["DT_zip"]
        )
        
        log_wrapper(driver, "Waiting for state error to appear...")
        if page.wait_for_element(page, SignupLocators_6.By_state_error, 3):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

    ###
    def test_TH_TC015(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC015 [Non-responsive]***")
        self.driver.testID = "TC015_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC015", "Test signup using invaliid zip, valid address, city, state, and preceding data [Non-responsive]")
        load_excel_sheet(self.driver, 'TH_TC015')
        self.TH_TC015()

    def test_TH_TC015_responsive(self):
        log_wrapper(self.driver, "***BEGINNING TH_TC015 [Responsive]***")
        self.driver.testID = "TC015_" + str(random.getrandbits(64))
        self.reporter.addTestCase(self.driver.testID, "TH_TC015", "Test signup using invaliid zip, valid address, city, state, and preceding data [Responsive]")
        load_excel_sheet(self.driver, 'TH_TC015')
        self.driver.set_window_size(500, 900)
        self.TH_TC015()

    def TH_TC015(self):
        log_wrapper(self.driver, "Entered TH_TC015 main test logic")
        driver = self.driver
        testID = self.driver.testID

        check_for_responsive(driver)

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
            str(driver.data["DT_phone"])
        )

        #Page 4
        page = SignupPage_4(driver)
        page.fill_page_and_submit(str(driver.data["DT_SSN"]), str(driver.data["DT_drivers"]))

        #Page 5
        page = SignupPage_5(driver)
        page.fill_page_and_submit(driver.data["DT_income"], driver.data["DT_pay_freq"])

        #Page 6
        page = SignupPage_6(driver)
        page.fill_page_negative(
            driver.data["DT_address"],
            driver.data["DT_city"],
            driver.data["DT_state"],
            driver.data["DT_zip"]
        )

        page.tab_outside()

        log_wrapper(driver, "Waiting for zipcode error to appear...")
        if page.wait_for_element(page, SignupLocators_6.By_zipcode_error, 2):
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message appears",
                True,
                "",
                screenshotCallback=driver.save_screenshot
            )
        else:
            self.reporter[testID].reportStep(
                "Check for error message to appear",
                "Error message appears",
                "Error message doesn't appear",
                False,
                "",
                screenshotCallback=driver.save_screenshot
            )
    ###

if __name__ == "__main__":
    unittest.main()