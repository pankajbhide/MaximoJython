#######################################################
# Purpose: Library script for sending email
#
#          
# Author : Pankaj Bhide
#
# Date    : Aug 18, 2015
#
# Revision
# History : 
#
######################################################
import sys



# Extend the sys Path

foundJython = False
#jythonLibPath = "c:\\jython\\lib"
jythonLibPath = "\/apps\/mxes\/mmofacn\/IBM\/WebSphere\/AppServer\/lbljython\/Lib"



for path in sys.path:
    if (path.find(jythonLibPath) != -1) :
        
        foundJython = True
    if (foundJython == False):
        
        sys.path.append(jythonLibPath)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



################################################################
# Expected Arguments -- 
# emailFrom, emailTo, emailCc, emailBcc, emailSubject, emailBody
#################################################################

# Create message container - the correct MIME type is 
# multipart/alternative.

global emailSubject, emailFrom, emailTo, emailCc, emailBcc, emailBody, emailSmtp

msg = MIMEMultipart('alternative')
msg['Subject'] = emailSubject
msg['From']    = emailFrom
msg['To']      = emailTo
msg['Cc']      = emailCc
msg['Bcc']     = emailBcc
rcpt = emailCc.split(",") + emailBcc.split(",") + [emailTo]

part2 = MIMEText(emailBody, 'html')
msg.attach(part2)

# Send the message via local SMTP server.
s = smtplib.SMTP(emailSmtp)
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(emailFrom, rcpt, msg.as_string())
s.quit()