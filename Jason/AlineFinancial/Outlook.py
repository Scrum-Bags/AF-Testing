import time
import string
import re
import win32com.client as win32
import os
from datetime import datetime, timedelta

#6 for inbox
#23 for junk

#inbox = mapi.GetDefaultFolder(6)

##
##outlook = win32.Dispatch('outlook.application')
##mapi = outlook.GetNamespace("MAPI")
##
##for account in mapi.Accounts:
##	print(account.DeliveryStore.DisplayName)

class Outlook_App():


    def __init__(self):
        self.outlook = win32.Dispatch('outlook.application')
        self.mapi = self.outlook.GetNamespace("MAPI")
        self.account = self.mapi.Accounts[0].DeliveryStore.DisplayName

    #6 for inbox
    #23 for junk
    #checks specified folder
    #checks for up to 90 seconds, returns the first match it gets
    def search_by_subject(self, subjectStr, folderNumber):
        self.recentFolder = folderNumber

        timer = 90

        while timer>1:
            messages = self.mapi.GetDefaultFolder(folderNumber).Items
            messages.Sort("[ReceivedTime]", True)
            messages = messages.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0E1D001F"" like '%"+ subjectStr +"%' ")
            if len(messages)>0:
                return messages[0]
            timer = timer - 1
            time.sleep(1)

        return -1

    #deletes all messages in a folder
    def delete_emails_in_folder(self, folderNumber):
        messages = self.mapi.GetDefaultFolder(folderNumber).Items
        for message in messages:
            message.Delete()
    #gets the body string
    def get_body(self, message):
        return message.Body
    #gets the subject string
    def get_subject(self, message):
        return message.Subject

    #Used for Aline Financial's password reset, returns None if not found
    def AF_get_reset_code(self, message):
        if message==-1:
            return None
        if (re.search("\d{6} ", message.Body) is not None):
            return re.search("\d{6} ", message.Body).group()
        else:
            return re.search("\d{6} ", message.Body)


##obj = Outlook_App()
##msg = obj.search_by_subject("Password Reset", 6)
###print(msg)
##print(obj.get_body(msg))
##print(obj.get_subject(msg))
##print(obj.AF_get_reset_code(msg))
####obj.delete_emails_in_folder(23)
