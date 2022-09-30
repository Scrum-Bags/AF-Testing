from selenium.webdriver.common.by import By

class HomePageLocators(object):
    By_getstarted_btn = (By.XPATH, '//*[@id="root"]/div/div[2]/div/div[1]/div[1]/div[1]/form/div/button')


class BaseSignupPageLocators(object):
    #back button won't exist on first page
    #next button will be submit button on last page, but shares xpath
    By_back_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[2]/button')
    By_next_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[1]/button')

class SignupLocators_1(object):
    #fields
    By_first_name_field = (By.ID, 'firstName')
    By_last_name_field = (By.ID, 'lastName')
    By_email_field = (By.ID, 'email')

    #error messages
    By_first_name_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div[1]/div/div[2]')
    By_last_name_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div/div[2]')
    By_email_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[3]/div/div/div[2]')

    By_back_btn = (By.XPATH, '') #doesn't exist, used to not throw error in BaseSignupPage.click_back()
    By_next_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div/button')

class SignupLocators_2(object):
    By_spending_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div/div[1]/div')
    By_stashing_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div/div[2]/div')
    By_both_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div/div[3]/div')

    By_back_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[2]/button')
    By_next_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[1]/button')

class SignupLocators_3(object):
    #fields
    By_DOB_field = (By.ID, 'dateOfBirth')
    By_gender_select = (By.ID, 'gender')
    By_phone_field = (By.ID, 'phone')

    #error messages
    By_DOB_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div[1]/div/div[2]')
    By_gender_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div/div[2]')
    By_phone_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[3]/div/div/div[2]')

    #buttons
    By_back_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[2]/button')
    By_next_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[1]/button')

class SignupLocators_4(object):
    #fields
    By_SSN_field = (By.ID, 'socialSecurity')
    By_drivers_field = (By.ID, 'driversLicense')

    #errors
    By_SSN_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div[1]/div/div[2]')
    #note - drivers license has no error message

    #buttons
    By_back_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[2]/button')
    By_next_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[1]/button')

class SignupLocators_5(object):
    #fields
    By_income_field = (By.ID, 'income')
    By_pay_freq_select = (By.ID, 'incomeFrequency')

    #errors
    By_income_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div[1]/div/div[2]')
    #note - pay frequency has no error message

    #buttons
    By_back_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[2]/button')
    By_next_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[1]/button')


class SignupLocators_6(object):
    #fields
    By_address_field = (By.ID, 'address')
    By_city_field = (By.ID, 'city')
    By_state_select = (By.ID, 'state')
    By_zipcode_field = (By.ID, 'zipcode')

    #errors
    By_address_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div[1]/div/div[2]')
    By_city_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div/div[2]')
    By_state_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[3]/div[1]/div/div[2]')
    By_zipcode_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[3]/div[2]/div/div[2]')

    #buttons
    By_back_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[2]/button')
    By_next_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[1]/button')


class SignupLocators_7(object):
    #buttons
    By_yes_radio = (By.ID, 'sameAs')
    By_no_radio = (By.ID, 'notSameAs')

    #fields (only appear if 'No' is selected)
    By_mailing_address_field = (By.ID, 'mailingAddress')
    By_mailing_city_field = (By.ID, 'mailingCity')
    By_mailing_state_field = (By.ID, 'mailingState')
    By_mailing_zip_field = (By.ID, 'mailingZipcode')

    #error messages (only appear with fields and 'No' selected)
    By_address_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[3]/div[2]/div[1]/div/div[2]')    
    By_city_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[3]/div[2]/div[2]/div/div[2]')
    By_state_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[3]/div[3]/div[1]/div/div[2]')
    By_zipcode_error = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[2]/div[3]/div[3]/div[2]/div/div[2]')

    #buttons
    By_back_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[2]/button')
    By_next_btn = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/form/div[3]/div/div[1]/button')

class ApprovalPageLocators(object):
    By_thank_you_message = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/div/div/h3')
    By_approval_text = (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[2]/div/div/div[1]/p[1]')