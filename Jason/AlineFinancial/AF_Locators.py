from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



class AF_Admin_Login_Objects(object):
    #objects on login page
    By_username_field = (By.ID, "username")
    By_password_field = (By.ID, "password")
    By_sign_in = (By.XPATH, "//*[@id='root']/div/div/div/div/form/input")
    By_sign_in_error = (By.ID, "LoginError")


class AF_Admin_Home_Objects(object):
    By_sidebar_menu = (By.ID, "SidebarContent")
    By_settings_menu = (By.ID, "navProfileDropdown")
    #dependent on settings menu
    By_profile_link = (By.XPATH, "//*[@id='SidebarContent']/div[2]/ul/li[1]/a")
    By_signout = (By.XPATH, "//*[@id='SidebarContent']/div[2]/ul/li[3]/button")


class AF_Member_Login_Objects(object):
    #objects on login page
    By_username_field = (By.ID, "username")
    By_password_field = (By.ID, "password")
    By_remember_me = (By.ID, "rememberMe")
    By_forgot_password_link = (By.XPATH, "/html/body/app-root/app-login/div[2]/div/div/app-login-form/form/div[3]/div[2]/div/a")
    By_log_in = (By.XPATH, "/html/body/app-root/app-login/div[2]/div/div/app-login-form/form/div[4]/button")
    By_sign_in_error = (By.XPATH, "/html/body/app-root/app-login/div[2]/div/div/div[2]")
    By_sign_up = (By.XPATH, "/html/body/app-root/app-login/div[2]/div/div/div[2]/button")

class AF_Member_Dashboard_Objects(object):
    #full screen stuff
    By_user_dropdown_f = (By.XPATH, "//*[@id='user-menu-link']")
    By_signout_f = (By.XPATH, "/html/body/app-root/app-dashboard/app-dashboard-nav/div[2]/div/ul/li[4]/div/div/button[5]")
    #compact screen stuff
    By_user_dropdown_c = (By.XPATH, "/html/body/app-root/app-dashboard/app-dashboard-nav/div[1]/div[1]/div/div[2]/button")
    By_signout_c = (By.XPATH, "//*[@id='dashboard-nav-drawer']/div[3]/button")
    


class AF_Member_ForgotPassword_Objects(object):
    #objects on login page
    By_username_field = (By.ID, "username")
    By_username_error = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/form/div[1]/div/div[2]")
    By_phone_radio = (By.ID, "phone")
    By_email_radio = (By.ID, "email")
    By_send_code = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/form/div[3]")

    #one time code page
    By_code_1 = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[1]/ng-component[1]/input")
    By_code_2 = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[1]/ng-component[2]/input")
    By_code_3 = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[1]/ng-component[3]/input")
    By_code_4 = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[1]/ng-component[4]/input")
    By_code_5 = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[1]/ng-component[5]/input")
    By_code_6 = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[1]/ng-component[6]/input")
    By_verify = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[2]")
    By_verify_error = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/p[2]")
    By_resend = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[3]/button")

    #reset password page
    By_password_field = (By.ID, "newPassword")
    By_confirm_password_field = (By.ID, "confirmNewPassword")
    By_reset_password = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/form/div[3]")
    By_reset_password_button = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/form/div[3]/button")

    By_password_field_error = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/form/div[1]/app-form-control-validation-indicator/app-form-control-indicator/div/fa-icon")
    By_confirm_password_field_error = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/form/div[2]/app-form-control-validation-indicator/app-form-control-indicator/div/fa-icon")

    By_new_password_error = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/form/div[2]/app-form-control-validation-indicator")

    #confirmation page
    By_success_text = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[1]/p[1]")
    By_log_in_link = (By.XPATH, "/html/body/app-root/app-forgot-password/div[2]/div/div/div[2]/app-password-reset-form/div[2]/button")

