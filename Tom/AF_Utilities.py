from selenium import webdriver
from TestSuiteReporter import TestSuiteReporter
import logging
from typing import Callable, Union
import mysql.connector
from mysql.connector import Error
import random, string

def report_event_and_log(
    driver, 
    message: str, 
):
    logging.getLogger(driver.loggingID).info(message)
    driver.reporter[driver.testID].reportEvent(message, False, "")

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
        logging.getLogger(driver.loggingID).info("MySQL Database connection sucessful")
    except Error as err:
        logging.getLogger(driver.loggingID).info(f"Error: '{err}'")

    return connection

def read_query(driver, connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        logging.getLogger(driver.loggingID).info(f"Error: '{err}'")

def execute_query(driver, connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.getLogger(driver.loggingID).info("Query successful")
    except Error as err:
        logging.getLogger(driver.loggingID).info(f"Error '{err}'")

def find_and_update_email(driver, email):
    connection = create_aline_sql_connection(driver)
    query = "SELECT * FROM applicant WHERE email='" + email + "'"
    results = read_query(driver, connection, query)
    if len(results) > 0:
        random_email = ''.join(random.choices(string.ascii_lowercase, k=12)) + '@' + ''.join(random.choices(string.ascii_lowercase, k=12)) + '.com'
        update_str = "UPDATE applicant SET email='" + random_email + "' WHERE email='" + email + "'"
        execute_query(driver, connection, update_str)
