import os

print(os.name)

if(os.name=='nt'):
    os.system("taskkill /f /im geckodriver.exe /T")
if(os.name=='posix'):
    os.system("sudo pkill -9 firefox")


#sudo pkill -9 firefox
