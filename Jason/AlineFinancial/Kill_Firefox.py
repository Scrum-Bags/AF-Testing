import os

#print(os.name)

if(os.name=='nt'):
    os.system("taskkill /f /im geckodriver.exe /T")
    os.system("taskkill /f /im firefox.exe /T")
if(os.name=='posix'):
    os.system("sudo pkill -9 firefox")
    os.system("sudo pkill -9 geckodriver")


#sudo pkill -9 firefox
