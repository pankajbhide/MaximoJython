##########################################################################
# Purpose: Script for creating the calendar events  

# Author : Pankaj Bhide
#
# Date    : Jan 26 2021
#
# Revision
# History : 
#
######################################################
from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
from java.util import TimeZone 
from java.text import SimpleDateFormat

# get the custom logger
logger = MXLoggerFactory.getLogger("maximo.meac")

#-------------------------------------------------------------------------------------------------------------
# global properties

emailTo = "PBhide@lbl.gov"
emailFrom = "PBhide@lbl.gov"

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
strWhere = "siteid='FAC' and wonum='W0075073'"
WOSet= MXServer.getMXServer().getMboSet("workorder", runAsUserInfo1)   
woMbo=None     
WOSet.reset() 
WOSet.setWhere(strWhere) # populate collection with new where clause
if (not WOSet.isEmpty()):
    woMbo=WOSet.getMbo(0)


emailSubject = "New calendar event for " + woMbo.getString("WONUM") + " - " + woMbo.getString("DESCRIPTION")
emailMsg = "<HTML><BODY>Please add this event to your personal calendar</BODY></HTML>"

mxHostname = MXServer.getMXServer().getProperty("mxe.hostname")
mxLink = "https://" + mxHostname + "/maximo/ui/maximo.jsp?event=loadapp&value=WOTRACK&uniqueid=W0075073" #+ mbo.getString("WORKORDERID")

#-------------------------------------------------------------------------------

# verifies that start/end dates are set

eventStart = woMbo.getDate("SCHEDSTART")
eventEnd = woMbo.getDate("SCHEDFINISH")

#if eventStart == None or eventEnd == None:
#    service.error("mxd", "Scheduled start/end dates must be set")

# build recipient list

emailToList = []

if emailTo != "":
    emailToList.append(emailTo)

'''if emailToPersonGroup != "":
    emailMboSet = mbo.getMboSet("$PG_EMAILS", "EMAIL", "personid in (select respparty from persongroupteam where persongroup='" + emailToPersonGroup + "')")

    emailMbo = emailMboSet.moveFirst()
    while (emailMbo):
        emailToList.append(emailMbo.getString("EMAILADDRESS"))
       emailMbo = emailMboSet.moveNext()
'''
#-------------------------------------------------------------------------------
# build iCal

sdf = SimpleDateFormat("yyyyMMdd'T'HHmmss'Z'")
sdf.setTimeZone(TimeZone.getTimeZone("UTC"))

dtStamp = sdf.format(MXServer.getMXServer().getDate())
dtStart = sdf.format(eventStart)
dtEnd = sdf.format(eventEnd)

# See PUBLISH event specs: https://tools.ietf.org/html/rfc5546#section-3.2.1

icalbody = (
       "BEGIN:VCALENDAR"
+"\n"+ "PRODID:-//MxDev//NONSGML Event Calendar//EN"
+"\n"+ "VERSION:2.0"
+"\n"+ "METHOD:PUBLISH"

+"\n"+ "BEGIN:VEVENT"
+"\n"+ "UID:" + woMbo.getString("WONUM")
+"\n"+ "DTSTAMP:" + dtStamp
+"\n"+ "SEQUENCE:0"

+"\n"+ "ORGANIZER:mailto:noreply@lbl.gov"
+"\n"+ "DTSTAMP:" + dtStamp
+"\n"+ "DTSTART:" + dtStart
+"\n"+ "DTEND:" + dtEnd
+"\n"+ "STATUS:CONFIRMED"
+"\n"+ "SUMMARY: Work Order " + woMbo.getString("WONUM") + " - " + woMbo.getString("DESCRIPTION")

+"\n"+ "DESCRIPTION:Work Order: " + woMbo.getString("WONUM")
+"\\n"+ "Description: " + woMbo.getString("DESCRIPTION")
+"\\n"+ "Asset: " + woMbo.getString("ASSETNUM") + " - " + woMbo.getString("ASSET.DESCRIPTION")
+"\\n"+ "Location: " + woMbo.getString("LOCATION") + " - " + woMbo.getString("LOCATION.DESCRIPTION")
+"\\n"+ "Priority: " + woMbo.getString("WOPRIORITY")
+"\\n"+ "Scheduled Start: " + woMbo.getString("SCHEDSTART")
+"\\n"+ "Scheduled End: " + woMbo.getString("SCHEDFINISH")
+"\\n"+ "<a href=" + mxLink + ">Link to Maximo</a>"

+"\n"+ "BEGIN:VALARM"
+"\n"+ "DESCRIPTION:REMINDER"
+"\n"+ "TRIGGER;RELATED=START:-PT15M"
+"\n"+ "ACTION:DISPLAY"
+"\n"+ "END:VALARM"

+"\n"+ "END:VEVENT"
+"\n"+ "END:VCALENDAR"
)

logger.debug(">>>> iCal body: " + icalbody)

#-------------------------------------------------------------------------------
# send email with attached iCal using MXServer.sendEMail function
# Parameters: to, from, subject, message, attachment, filename

MXServer.getMXServer().sendEMail(emailToList, emailFrom, emailSubject, emailMsg, icalbody, "maximo.ics")