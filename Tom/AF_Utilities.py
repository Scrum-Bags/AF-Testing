from selenium import webdriver
from TestSuiteReporter import TestSuiteReporter
import logging
from typing import Callable, Union
import mysql.connector
from mysql.connector import Error
import random, string, time, inspect
import pathlib
from Outlook import Outlook_App
from openpyxl import load_workbook

def report_event_and_log(driver, message: str):
    driver.reporter[driver.testID].reportEvent(message, False, "")
    func = inspect.currentframe().f_back.f_code
    path = pathlib.PurePath(func.co_filename)
    logging.getLogger(driver.loggingID).info("{%s in %s:%i} - %s" % (
        func.co_name,
        path.name,
        func.co_firstlineno,
        message
    ))

def log_wrapper(driver, message):
    func = inspect.currentframe().f_back.f_code
    path = pathlib.PurePath(func.co_filename)
    logging.getLogger(driver.loggingID).info("{%s in %s:%i} - %s" % (
        func.co_name,
        path.name,
        func.co_firstlineno,
        message
    ))

def load_excel_sheet(driver, rowName):
    wb = load_workbook(filename = 'AF_Register_Bank_Member.xlsm', data_only=True)
    sheet = wb['RegisterBank']
    driver.data = {}
    for row in sheet.rows:
        if row[0].value == rowName:
            for i in range (2, 22):
                driver.data[sheet.cell(column=i, row=1).value] = sheet.cell(column=i, row=row[0].row).value
            log_wrapper(driver, "Loaded excel data")

def check_for_responsive(driver):
    log_wrapper(driver, "Checking for responsive webpage")
    if driver.get_window_size()['width'] < 550:
        driver.responsive = True
        log_wrapper(driver, "Detected responsive")
    else:
        driver.responsive = False
        log_wrapper(driver, "Didn't detect responsive")

def check_outlook_confirmation(driver, timeout=60):
    timer = 0
    obj = Outlook_App()
    while obj.search_by_subject("Welcome", 6) == -1 and timer < timeout:
        timer += 1
        time.sleep(1)
        log_wrapper(driver, 
            "Waiting for Outlook confirmation " + str(timer) + "/" + str(timeout) + "s"
        )

    if obj.search_by_subject("Welcome", 6) == -1:
        driver.reporter[driver.testID].reportStep(
            "Check if confirmation email was received",
            "Confirmation email was received",
            "Confirmation email wasn't received after " + str(timeout) + " seconds",
            False
        )
        log_wrapper(driver, "Confirmation email wasn't received after " + str(timeout) + " seconds")

    else:
        driver.reporter[driver.testID].reportStep(
            "Check if confirmation email was received",
            "Confirmation email was received",
            "Confirmation email was received after " + str(timer) + " seconds",
            True
        )
        obj.delete_emails_in_folder(6)
        log_wrapper(driver, "Confirmation email was received after " + str(timer) + " seconds")




#SQL Utilites
def create_aline_sql_connection(driver):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='uftcapstone-db.c1ddjzxizuua.us-east-1.rds.amazonaws.com',
            user='uftcapstone',
            passwd='!A&8vYOKSUO&X9Zt',
            database='alinedb'
        )
        log_wrapper(driver, "MySQL Database connection sucessful")
    except Error as err:
        log_wrapper(driver, f"Error: '{err}'")

    return connection

def read_query(driver, connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        log_wrapper(driver, f"Error: '{err}'")

def execute_query(driver, connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        log_wrapper(driver, "Query successful")
    except Error as err:
        log_wrapper(driver, f"Error '{err}'")

def find_and_update_email(driver, email):
    connection = create_aline_sql_connection(driver)
    query = "SELECT * FROM applicant WHERE email='" + email + "'"
    results = read_query(driver, connection, query)
    if len(results) > 0:
        random_email = ''.join(random.choices(string.ascii_lowercase, k=12)) + '@' + ''.join(random.choices(string.ascii_lowercase, k=12)) + '.com'
        update_str = "UPDATE applicant SET email='" + random_email + "' WHERE email='" + email + "'"
        execute_query(driver, connection, update_str)
