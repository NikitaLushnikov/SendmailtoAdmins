# This Python file uses the following encoding: utf-8
import smtplib
import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version
#pip install linecache2
import linecache
#=====global values======
global ORA_errors
ORA_errors=""
global add_text_to_mail
add_text_to_mail=""
# russion symboll -error in linux! -> wright at 1 line: # This Python file uses the following encoding: utf-8
# ============================================#
# Script for sending information on the HDI   #
# Created at 2022.04.29                       #
# From server          : smtp.mail.ru         #
# From mailbox         : crocscript@mail.ru   #
# Project serverIP     : 10.210.11.50 (oracle)#
# Project Test servrIP : 172.26.7.225 (oracle)# alfabipublisher2  
# ============================================#
def Func_add_text_to_mail1(FilePath):
    print("=================Func_chek_for_ORA_errors=================")
    whole_str=""
    with open(FilePath, 'r') as file_output:
        for n, stroka in enumerate(file_output, 1):
            #print(n)
            #print(stroka)
            whole_str+=stroka
    print("=================Func_add_text_to_mail END=================")
    return whole_str 

    
def Func_add_text_to_mail(FilePath,number_of_lines_from_end):#2022.05.02 в планах дописать функцию, которая 
    #будет принимать на вход файл и колличество строк которые нужно с конца продублировать в теле письма +
    #будет принимать на вход файл и строки до определенной строки например с даты 
    print("=================Func_add_text_to_mail=================")
    count_strings=0
    string=""           #each string that i will add to text
    Add_text_to_html="" #whole string at finish 
    with open(FilePath, 'r') as file_output:
                for count_strings, stroka in enumerate(file_output, 1):#cчитаем строки
                    count_strings=count_strings        
                #print(count_strings)
                for i in range(count_strings-number_of_lines_from_end,count_strings+1,1):#с 3(включая) по 14(не включая) с шагом 1 @ начало конец шаг 
                    string = (linecache.getline(FilePath, i))
                    #print (string)
                    Add_text_to_html+=string
    print(Add_text_to_html)
    print("=================Func_add_text_to_mail END=================")
    return Add_text_to_html
    

def Func_chek_for_ORA_errors(massiveFilePathsCheckORA,required_errors): #1 massive files that you wont to chek for errors
    
    print("=================Func_chek_for_ORA_errors=================")
    global ORA_errors
    for FilePath in massiveFilePathsCheckORA: #for ech file
        print(FilePath)
        ORA_errors=" "
        with open(FilePath, 'r') as file_output: #for ech file - open file for reading
            for n, stroka in enumerate(file_output, 1): #stroka - whole string / n -number of string
                if (stroka.find(required_errors)==0 or stroka.find(required_errors)>0): #stroka.find(ORA-) return -1 if there's no ORA-
                    print(n)
                    print(stroka)
                    ORA_errors += str(n) + " " + str(stroka) + '\n'
                    
def Func_SendMail(massiveFilePaths,recipients): #1 massive files that you wont deliver to recipients
    print("=================Start Func_SendMail=================")

    dt_relese = datetime.datetime(2022,4,29)
    dt_now = datetime.datetime.today()
    dt_now_str=str(dt_now)
    Numofdays = dt_now - dt_relese
    Numofdays_str = str(Numofdays)
        
    #print(dt_relese)
    #print(dt_now)
    #print(Numofdays)
    spase=Numofdays_str.find(" ")
    #print(Numofdays_str[:spase])  

    server   = 'smtp.mail.ru'
    user     = 'crocscript@mail.ru'   # mailbox
    password = 'zHXiewnvcys0jBjsAxc9' # encrypted in the mailbox

    sender     = 'crocscript@mail.ru'
    subject    = 'Daily report HDI project'
    #text       = '<h1> Hi! This is a report from HDI #'+Numofdays_str[:spase]+'</h1>'
    #html       = '<html><head></head><body><p>' + text + '</p></body></html>'
    text       = '<table border="0" cellspacing="0" cellpadding="0"><td width="648" valign="top"><p> <font face="Arial"> Good morning, colleagues! There is the daily Oracle server report #'+Numofdays_str[:spase]+' <br><br>From server <strong>.10.210.11.50 (OL11DIAP)</strong><br>Test server <strong>.172.26.7.225 (alfabipublisher2)</strong></font><p></tr></table>'  
    
    ORA_text   = "There are some problems in alert logs: " + ORA_errors
    ORA_text_no= "There are no problems in alert logs"
    print("ORA_errors: "+"["+ ORA_errors +"]")

    if (ORA_errors == " "):
        html       = '<html><head></head><body><p>' + text + '<span style="color: green;">' + ORA_text_no + '</span>'+ add_text_to_mail + '</span></p></body></html>'
        print("ok!")
    else:
        html       = '<html><head></head><body><p>' + text + '<br>' +'<span style="color: red;">'+ ORA_text + '</span>' + add_text_to_mail + '</p></body></html>'
        print("errors")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'CheckHDIscript <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To']    = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    for FilePath in massiveFilePaths: 
        #print(FilePath)
        basename = os.path.basename(FilePath)
        filesize = os.path.getsize(FilePath)
        part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
        part_file.set_payload(open(FilePath, "rb").read())
        part_file.add_header('Content-Description', basename)
        part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
        encoders.encode_base64(part_file)
        msg.attach(part_file)
    ###oshibka at 2022.05.01 Lushnikov Nikita
    mail = smtplib.SMTP_SSL(server)  #an error may appear due to the crocVpn - everything is fine with HDI vpn
    #ping to post-server
    #ping smtp.mail.ru from  hdi.vpn    Y
    #ping smtp.mail.ru from croc.vpn    Y
    #ping smtp.mail.ru from homeNetwork Y

    # Exception has occurred: TimeoutError
    # [WinError 10060] The attempt to establish a connection was unsuccessful, because the desired response was not received from another computer in the required time, or an already established connection was terminated due to an incorrect response from an already connected computer
    #   File "C:\Users\NLushnikov\Desktop\jobConspects\TXT\workscripts\HDI\2022_04_29_HDI_mailsender\2022_04_29_HDImailSender.py", line 60, in <module>
    #     mail = smtplib.SMTP_SSL(server)
    ### It seems to me thet the reason in 2 part 
    ### "Or an already established connection was terminated due to an incorrect response from an already connected computer"

    mail.login(user, password) #an error may appear due to the password
    # Exception has occurred: SMTPAuthenticationError
    # (535, b'5.7.0 NEOBHODIM parol prilozheniya https://help.mail.ru/mail/security/protection/external / Application password is REQUIRED')
    #   File "C:\Users\NLushnikov\Desktop\jobConspects\TXT\workscripts\HDI\2022_04_29_HDI_mailsender\test.py", line 48, in <module>
    #     mail.login(user, password)# error apparently invalid password

    # the password must use the password of a third-party application that is made for the mailbox
    #=========passwords======================= #
    # mailbox  crocscript@mail.ru              #
    #    # password     :9Mm-u6i-eHz-RYN       #
    # for a third-party application            #
    #    # for me       :ParolForIP102101150hdi#
    #    # encoded      :zHXiewnvcys0jBjsAxc9  # +
    #========================================= #
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()
    
    recipients_str=str(recipients)
    print("send it to "+recipients_str+" !")
    
if __name__ == '__main__':
    
    #input recipients              
    #recipients = ['Nlushnikov@croc.ru'] #ABitelev@croc.ru MVaisov@croc.ru
    recipients = ['Nlushnikov@croc.ru','ABitelev@croc.ru', 'MVaisov@croc.ru'] 
    #input file paths, that you would like to atach
    massiveFilePaths   = ['/home/oracle/scripts/python/OL11DIAPBCKUP_cut.log',
                          '/home/oracle/scripts/python/alert_OL11DIAP_cut.log',
                          '/home/oracle/scripts/python/free_space_cut.log',
                          '/home/oracle/tablespace.html']
    #input file paths, that you would like to test for ORA errors
    massiveFilePathsCheckORA =['/home/oracle/scripts/python/alert_OL11DIAP_cut.log']
    #input required_errors 
    required_errors="ORA-"
    Func_chek_for_ORA_errors(massiveFilePathsCheckORA,required_errors)

    add_text_to_mail=Func_add_text_to_mail1('/home/oracle/tablespace.html')
    Func_SendMail(massiveFilePaths,recipients)
    print(ORA_errors)   
