import time
import random
import string
import re
import win32com.client as win32
import os
from datetime import datetime, timedelta

#6 for inbox
#23 for junk
#inbox = mapi.GetDefaultFolder(6)

class Outlook_App():


    def __init__(self):
        self.outlook = win32.Dispatch('outlook.application')
        self.mapi = self.outlook.GetNamespace("MAPI")
        self.account = self.mapi.Accounts[0].DeliveryStore.DisplayName

    
    #6 for inbox
    #23 for junk
    #checks inbox and junkmail
    #
    def search_by_subject(self, subjectStr, folderNumber):
        self.recentFolder = folderNumber

        messages = self.mapi.GetDefaultFolder(folderNumber).Items
        messages.Sort("[ReceivedTime]", True)
        messages = messages.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0E1D001F"" like '%"+ subjectStr +"%' ")

        if len(messages)>0:
            return messages[0]
        else:
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

    def AF_get_reset_code(self, message):
        if (re.search("\d{6} ", message.Body) is not None):
            return re.search("\d{6} ", message.Body).group()
        else:
            return re.search("\d{6} ", message.Body)

#obj = Outlook_App()
#msg = obj.search_by_subject("Welcome", 6)
#print(msg)
#print(obj.get_body(msg))
#print(obj.get_subject(msg))
#print(obj.AF_get_reset_code(msg))
##obj.delete_emails_in_folder(23)