from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from AF_Locators import AF_Member_Login_Objects
from AF_Locators import AF_Member_ForgotPassword_Objects
from AF_Locators import AF_Member_Dashboard_Objects
from Outlook import Outlook_App
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import Random_Generators
import string
import time
from selenium.webdriver.common.action_chains import ActionChains

#https://selenium-python.readthedocs.io/getting-started.html#simple-usage

class AF_MemberLogin():


    def __init__(self, driver = "default"):

        if(driver=="default"):
            self.driver = webdriver.Chrome()
        else:
            self.driver = driver


    def Launch_Login_Page(self):
        self.driver.get("http://uftcapstone-dev-member.s3-website-us-east-1.amazonaws.com/login")

    def MobileCheck(self):
        #print(self.driver.find_element(*AF_Member_Dashboard_Objects.By_summary_link).size["height"])
        return not self.driver.find_element(*AF_Member_Dashboard_Objects.By_summary_link).size["height"] > 0

    def login(self, reporter, ssPath, username, password):
        driver = self.driver
        actions = ActionChains(driver)
        print("***Logging into Aline Financial Member's Page***")
        #wait for page to load
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((AF_Member_Login_Objects.By_username_field)))
        #set username field
        userFieldObj = driver.find_element(*AF_Member_Login_Objects.By_username_field)
        userFieldObj.send_keys(username)
        if userFieldObj.get_attribute('value') == username:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username successfully placed in dialog box",True,"username = " + username, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username successfully placed in dialog box")
        else:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username not placed in dialog box",False,"username = " + username, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username not place in dialog box")
            print("Stopping test")
            return
        #set password field
        passwordFieldObj = driver.find_element(*AF_Member_Login_Objects.By_password_field)
        passwordFieldObj.send_keys(password)
        if passwordFieldObj.get_attribute('value') == password:
            reporter.reportStep("Put password in dialog box","Password should appear in the dialog box","Password successfully placed in dialog box",True,"password = " + password, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password successfully placed in dialog box")
        else:
            reporter.reportStep("Put password in dialog box","Password should appear in the dialog box","Password not place in dialog box",False,"password = " + password, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password not place in dialog box")
            print("Stopping test")
            return
        #click sign in button
        signinObj = driver.find_element(*AF_Member_Login_Objects.By_log_in)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_Login_Objects.By_log_in))
        time.sleep(1)
        signinObj.click()
        print("Clicking login button")
        #wait for login to load
        try:
            WebDriverWait(driver, 90).until(EC.url_contains("http://uftcapstone-dev-member.s3-website-us-east-1.amazonaws.com/dashboard/summary"))
            reporter.reportStep("Press submit and login","Member dashboard should appear","Login successful",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Login successful")
        except:
            reporter.reportStep("Press submit and login","Member dashboard should appear","Login unsuccessful",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Login unsuccessful")
        self.username=username
        self.password=password

    def logout(self, reporter, ssPath):
        driver = self.driver
        #click sidebar in case of responsiveness
        error = ""
        located = False
        print("Looking for dropdown button")
        mobile = self.MobileCheck()
        if not mobile:
            driver.find_element(*AF_Member_Dashboard_Objects.By_user_dropdown_f).click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((AF_Member_Dashboard_Objects.By_signout_f)))
            reporter.reportStep("Click sidebar if visible","Settings button should appear","If sidebar was visible, it was clicked successfully",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            driver.find_element(*AF_Member_Dashboard_Objects.By_signout_f).click()
            located = True
            print("Dropdown clicked successfully")
            print("Logout button clicked")
        else:
            driver.find_element(*AF_Member_Dashboard_Objects.By_user_dropdown_c).click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((AF_Member_Dashboard_Objects.By_signout_c)))
            reporter.reportStep("Click sidebar if visible","Settings button should appear","If sidebar was visible, it was clicked successfully",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            driver.find_element(*AF_Member_Dashboard_Objects.By_signout_c).click()
            located = True
            print("Dropdown clicked successfully")
            print("Logout button clicked")
        
        if not located:
            reporter.reportStep("Press logout button","Login page should appear","Unable to locate logout button",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            driver.get("http://uftcapstone-dev-member.s3-website-us-east-1.amazonaws.com/login")
            print("Unable to locate logout button")
        else:
            if driver.current_url == "http://uftcapstone-dev-member.s3-website-us-east-1.amazonaws.com/login":
                reporter.reportStep("Click logout button","Login page should appear","Navigation successful",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Logout successful")
            else:
                reporter.reportStep("Click logout button","Login page should appear","Navigation unsuccessful",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Logout unsuccessful, forced navigation required")
            
        self.username=""
        self.password=""

        
    def forgot_password(self, reporter, ssPath, username, newPassword):
        driver = self.driver
        print("***Starting Aline Finanicial's Forgot Password Process***")

        if username is None:
            username = ""
        if newPassword == "rnd":
            newPassword = Random_Generators.Random_Password_AF()

        actions = ActionChains(driver)
        #click forgot password button
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((AF_Member_Login_Objects.By_forgot_password_link)))
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_Login_Objects.By_forgot_password_link))
        time.sleep(1)
        driver.find_element(*AF_Member_Login_Objects.By_forgot_password_link).click()
        print("Clicking forgot password link")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_username_field)))
        if len(driver.find_elements(*AF_Member_ForgotPassword_Objects.By_username_field))>0:
            reporter.reportStep("Click forgot password link","Site should navigate to 'forgot password' page","Navigation successful",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Navigation successful")
        else:
            reporter.reportStep("Click forgot password link","Site should navigate to 'forgot password' page","Navigation unsuccessful",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Navigation unsuccessful")
            print("Stopping test")
            return -1
        #enter username
        username_field = driver.find_element(*AF_Member_ForgotPassword_Objects.By_username_field)
        username_field.send_keys(username)
        #check that username was entered
        if username_field.get_attribute('value') == username:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username successfully placed in dialog box",True,username, username_field.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username successfully placed in dialog box")
        else:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username not placed in dialog box",False,username, username_field.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username not placed in dialog box")
            print("Stopping test")
            return -1
        #set to email
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_email_radio).click()
        #click send code button
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_ForgotPassword_Objects.By_send_code))
        time.sleep(1)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_send_code).click()
        print("Clicking 'send code' link")
        WebDriverWait(driver, 90).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_code_1)))
        if len(driver.find_elements(*AF_Member_ForgotPassword_Objects.By_code_1))>0:
            reporter.reportStep("Click send code link","Site should navigate to 'forgot password' page","Navigation successful",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Site navigated to 'code input' page")
        else:
            reporter.reportStep("Click send code link","Site should navigate to 'forgot password' page","Navigation unsuccessful",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Site failed to navigate to 'code input' page")
            print("Stopping test")
            return -1
        #check email for reset code
        obj = Outlook_App()
        msg = obj.search_by_subject("Password Reset", 6)
        code = obj.AF_get_reset_code(msg)
        obj.delete_emails_in_folder(6)
        print("Checking email for reset code")
        if code!=-1:
            reporter.reportStep("Check email for reset code","An email containing the reset code should be locatable","Email located",True,code)
            print("Email located")
        else:
            reporter.reportStep("Check email for reset code","An email containing the reset code should be locatable","Email could not be located",False,"")
            print("Email could not be located")
            print("Stopping test")
            return -1
        #input code
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_1).send_keys(code[0])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_2).send_keys(code[1])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_3).send_keys(code[2])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_4).send_keys(code[3])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_5).send_keys(code[4])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_6).send_keys(code[5])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_verify).click()
        print("Inputting code and verifying")

        WebDriverWait(driver, 90).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_password_field)))
        if len(driver.find_elements(*AF_Member_ForgotPassword_Objects.By_password_field))>0:
            reporter.reportStep("Enter code received from email","Site should navigate to 'enter new password' page","Code accepted",True,code, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Code accepted")
        else:
            reporter.reportStep("Enter code received from email","Site should navigate to 'enter new password' page","Code not accepted",False,code, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Code not accepted")
            print("Stopping test")
            return -1

        #set new password
        print("inputting new password")
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_password_field).send_keys(newPassword)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_confirm_password_field).send_keys(newPassword)

        #time.sleep(5)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_ForgotPassword_Objects.By_reset_password))
        time.sleep(1)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_reset_password).click()

        WebDriverWait(driver, 90).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_success_text)))
        if len(driver.find_elements(*AF_Member_ForgotPassword_Objects.By_success_text))>0:
            reporter.reportStep("Enter new password and submit","Site should indicate that new password was accepted","Password accepted",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password accepted")
        else:
            reporter.reportStep("Enter new password and submit","Site should indicate that new password was accepted","Password not accepted",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password not accepted")
            print("Stopping test")
            return -1

        print("Going back to login screen")
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_ForgotPassword_Objects.By_log_in_link))
        time.sleep(1)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_log_in_link).click()

        #time.sleep(5)
        print("***End of Aline Finanicial's Forgot Password Process***")
        return newPassword

    #does negative testing, enters a new password at the end if the negative tests pass
    def forgot_password_neg(self, reporter, ssPath, username, newPassword):
        driver = self.driver
        print("***Starting Aline Finanicial's Forgot Password Process - Negative Testing***")
        #check if a fake name was generated
        neuCheck = False
        if username is None:
            username = ""
        if username == "neu":
            username = Random_Generators.Random_Name_AF()
            neuCheck = True
        if newPassword == "rnd":
            newPassword = Random_Generators.Random_Password_AF()

        actions = ActionChains(driver)
        #click forgot password button
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((AF_Member_Login_Objects.By_forgot_password_link)))
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_Login_Objects.By_forgot_password_link))
        time.sleep(1)
        driver.find_element(*AF_Member_Login_Objects.By_forgot_password_link).click()
        print("Clicking forgot password link")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_username_field)))
        if len(driver.find_elements(*AF_Member_ForgotPassword_Objects.By_username_field))>0:
            reporter.reportStep("Click forgot password link","Site should navigate to 'forgot password' page","Navigation successful",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Navigation successful")
        else:
            reporter.reportStep("Click forgot password link","Site should navigate to 'forgot password' page","Navigation unsuccessful",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Navigation unsuccessful")
            print("Stopping test")
            return -1
        #enter username
        username_field = driver.find_element(*AF_Member_ForgotPassword_Objects.By_username_field)
        username_field.send_keys(username)
        #check that username was entered
        if username_field.get_attribute('value') == username:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username successfully placed in dialog box",True,username, username_field.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username successfully placed in dialog box")
        else:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username not place in dialog box",False,username, username_field.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username not placed in dialog box")
            print("Stopping test")
            return -1
        #set to email
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_email_radio).click()

        #checks for error message before checking if navigation happens
        if (username == "" or neuCheck):
            if len(driver.find_elements(*AF_Member_ForgotPassword_Objects.By_username_error))>0:
                reporter.reportStep("Click send code link with an invalid username","Site should display a username error","Username error displayed",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Username error displayed for invalid username")
            else:
                reporter.reportStep("Click send code link with an invalid username","Site should display a username error","Username error not displayed",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))  
                print("Username error not displayed for invalid username")
        #click send code button
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_ForgotPassword_Objects.By_send_code))
        time.sleep(1)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_send_code).click()
        print("Clicking 'send code' link")
        #check if navigation happens depending on input username
        try:
            if username == "":
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_code_1)))
            else:
                 WebDriverWait(driver, 90).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_code_1)))
            if username != "" and not neuCheck:
                reporter.reportStep("Click send code link with a valid username","Site should navigate to 'forgot password' page","Navigation successful",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Navigation successful")
            else:
                reporter.reportStep("Click send code link with an invalid username","Site should not navigate to 'forgot password' page","Navigated to 'forgot password' page",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Navigated to 'forgot password' page with an invalid username")
                print("Stopping test")
                self.Launch_Login_Page()
                return -1
        except:
            if username == "" or neuCheck:
                reporter.reportStep("Click send code link with an invalid username","Site should not navigate to 'forgot password' page","Did not navigate to 'forgot password' page",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Did not navigate to 'forgot password' page with an invalid username")
                print("Stopping test")
                self.Launch_Login_Page()
                return -1
            else:
                reporter.reportStep("Click send code link with a valid username","Site should navigate to 'forgot password' page","Navigation unsuccessful",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Did not navigate to 'forgot password' page with a valid username")
                print("Stopping test")
                self.Launch_Login_Page()
                return -1

        #check email for reset code
        obj = Outlook_App()
        msg = obj.search_by_subject("Password Reset", 6)
        code = obj.AF_get_reset_code(msg)
        obj.delete_emails_in_folder(6)
        print("Checking email for reset code")
        if code is not None:
            reporter.reportStep("Check email for reset code","An email containing the reset code should be locatable","Email located",True,code)
            print("Email located")
        else:
            reporter.reportStep("Check email for reset code","An email containing the reset code should be locatable","Email could not be located",False,"")
            print("Email could not be located")
            print("Stopping test")
            return -1

        #test resend button
        print("Clicking 'resend code' button")
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_ForgotPassword_Objects.By_resend))
        time.sleep(1)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_resend).click()
        msg = obj.search_by_subject("Password Reset", 6)
        code = obj.AF_get_reset_code(msg)
        obj.delete_emails_in_folder(6)
        if code is not None:
            reporter.reportStep("Check email for resent reset code","An email containing the reset code should be locatable","Email located",True,code)
            print("Email located")
        else:
            reporter.reportStep("Check email for resent reset code","An email containing the reset code should be locatable","Email could not be located",False,"")
            print("Email could not be located")
            print("Stopping test")
            return -1

        #input fake code
        print("Inputting fake code")
        badCode = Random_Generators.Random_Number(6)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_1).send_keys(badCode[0])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_2).send_keys(badCode[1])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_3).send_keys(badCode[2])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_4).send_keys(badCode[3])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_5).send_keys(badCode[4])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_6).send_keys(badCode[5])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_verify).click()
        try:
            WebDriverWait(driver, 90).until(EC.text_to_be_present_in_element((AF_Member_ForgotPassword_Objects.By_verify_error), "One-time passcode is not correct."))
            reporter.reportStep("Enter invalid code received from email","Site should display a code error","Code not accepted and error displayed",True,badCode, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Code not accepted and error displayed")
        except:
            reporter.reportStep("Enter invalid code received from email","Site should display a code error","Code not accepted",False,badCode, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Code error not displayed")
            return -1
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_1).clear()
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_2).clear()
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_3).clear()
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_4).clear()
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_5).clear()
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_6).clear()

        #input code
        print("Inputting code")
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_1).send_keys(code[0])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_2).send_keys(code[1])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_3).send_keys(code[2])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_4).send_keys(code[3])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_5).send_keys(code[4])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_code_6).send_keys(code[5])
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_verify).click()
        try:
            WebDriverWait(driver, 90).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_password_field)))
            reporter.reportStep("Enter code received from email","Site should navigate to 'enter new password' page","Code accepted",True,code, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Code accepted")
        except:
            reporter.reportStep("Enter code received from email","Site should navigate to 'enter new password' page","Code not accepted",False,code, driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Code not accepted")
            print("Stopping test")
            return -1


        #password fields
        passwordField1=driver.find_element(*AF_Member_ForgotPassword_Objects.By_password_field)
        passwordField2=driver.find_element(*AF_Member_ForgotPassword_Objects.By_confirm_password_field)
        resetButton = driver.find_element(*AF_Member_ForgotPassword_Objects.By_reset_password_button)
        #negative password testing
        randomPassword1 = Random_Generators.Random_Password_AF()
        randomPassword2 = Random_Generators.Random_Password_AF()
        badPassword1 = Random_Generators.Random_Name_AF()
        badPassword2 = Random_Generators.Random_Name_AF()
        #blank fields
        print("Leaving password fields blank")
        passwordField1.send_keys("")
        passwordField1.send_keys("")
        if not resetButton.is_enabled():
            reporter.reportStep("Try to submit new password with missing fields","Reset button should be disabled","Reset button is disabled",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is disabled")
        else:
            reporter.reportStep("Try to submit new password with missing fields","Reset button should be disabled","Reset button is not disabled",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is not disabled")
        #one blank field
        print("Leaving first password field blank")
        passwordField1.send_keys(newPassword)
        passwordField1.send_keys("")
        if not resetButton.is_enabled():
            reporter.reportStep("Try to submit new password with missing fields","Reset button should be disabled","Reset button is disabled",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is disabled")
        else:
            reporter.reportStep("Try to submit new password with missing fields","Reset button should be disabled","Reset button is not disabled",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is not disabled")
        #one blank field
        print("Leaving second password field blank")
        passwordField1.clear()
        passwordField1.send_keys("")
        passwordField1.send_keys(newPassword)
        if not resetButton.is_enabled():
            reporter.reportStep("Try to submit new password with missing fields","Reset button should be disabled","Reset button is disabled",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is disabled")
        else:
            reporter.reportStep("Try to submit new password with missing fields","Reset button should be disabled","Reset button is not disabled",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is not disabled")
        #bad password
        print("Inputting invalid passwords")
        passwordField1.clear()
        passwordField2.clear()
        passwordField1.send_keys(badPassword1)
        passwordField2.send_keys(badPassword1)
        if not resetButton.is_enabled():
            reporter.reportStep("Try to submit new password with an invalid password","Reset button should be disabled","Reset button is disabled",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is disabled")
        else:
            reporter.reportStep("Try to submit new password with an invalid password","Reset button should be disabled","Reset button is not disabled",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is not disabled")
        #non-matching passwords
        print("Inputting valid but non-matching passwords")
        passwordField1.clear()
        passwordField2.clear()
        passwordField1.send_keys(randomPassword1)
        passwordField2.send_keys(randomPassword2)
        if not resetButton.is_enabled():
            reporter.reportStep("Try to submit new password with non-matching passwords","Reset button should be disabled","Reset button is disabled",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is disabled")
        else:
            reporter.reportStep("Try to submit new password with non-matching passwords","Reset button should be disabled","Reset button is not disabled",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is not disabled")
        #set new password
        print("Inputting valid, matching passwords")
        passwordField1.clear()
        passwordField2.clear()
        passwordField1.send_keys(newPassword)
        passwordField2.send_keys(newPassword)
        if resetButton.is_enabled():
            reporter.reportStep("Try to submit new password","Reset button should be enabled","Reset button is enabled",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is enabled")
        else:
            reporter.reportStep("Try to submit new password","Reset button should be enabled","Reset button is not enabled",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Reset button is not enabled")
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_ForgotPassword_Objects.By_reset_password))
        time.sleep(1)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_reset_password).click()

        WebDriverWait(driver, 90).until(EC.element_to_be_clickable((AF_Member_ForgotPassword_Objects.By_success_text)))
        if len(driver.find_elements(*AF_Member_ForgotPassword_Objects.By_success_text))>0:
            reporter.reportStep("Enter new password and submit","Site should indicate that new password was accepted","Password accepted",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password accepted")
        else:
            reporter.reportStep("Enter new password and submit","Site should indicate that new password was accepted","Password not accepted",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password not accepted")
            return -1
        
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*AF_Member_ForgotPassword_Objects.By_log_in_link))
        time.sleep(1)
        driver.find_element(*AF_Member_ForgotPassword_Objects.By_log_in_link).click()
        print("***End of Aline Finanicial's Forgot Password Process - Negative Testing***")
        return newPassword
