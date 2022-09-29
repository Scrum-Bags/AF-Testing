from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time, random, unittest, logging

from AF_POMs import *

class AF_Register_Bank_Member(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AF_Register_Bank_Member, self).__init__(*args, **kwargs)
        self.timestr = time.strftime("%Y-%m-%d--%I_%M_%S%p")
        #TODO reporting
        logging.basicConfig(level=logging.INFO,
                            handlers=[
                                logging.FileHandler("AO_Browse_Store" + self.timestr + ".log"),
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
        BasePage.wait_for_element(self, HomePageLocators.By_signup_btn, 30)

    def test_TH_TC001(self):
        logging.getLogger(self.driver.loggingID).info("***BEGINNING TH_TC001 [Non-responsive]***")
        self.TH_TC001()
        
    def TH_TC001(self):
        logging.getLogger(self.driver.loggingID).info("Entered TH_TC001 main test logic")

if __name__ == "__main__":
    unittest.main()