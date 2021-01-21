################################################################
# Purpose: Script for object level launch for workorder
#          (after commit) 
# Author : Pankaj Bhide
#
# Date    : Aug 19, 2015
#
# Revision
# History : 
#
######################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import Date
from java.text import SimpleDateFormat



logger = mbo.getMboLogger()

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def getPersonname(strPersonid):
    strPersonname=None
    personSet = MXServer.getMXServer().getMboSet("PERSON", mbo.getUserInfo())
    personSet.setUserWhere("personid='" + strPersonid +"'")
    if (not personSet.isEmpty()):
                strPersonname=personSet.getMbo(0).getString("displayname")
    personSet=None      
    return strPersonname

def getWorktypedesc(strWorktype):
    strWorktypedesc=None
    worktypeSet = MXServer.getMXServer().getMboSet("WORKTYPE", mbo.getUserInfo())
    worktypeSet.setUserWhere("worktype='" + strWorktype +"' and woclass='WORKORDER' ")
    if (not worktypeSet.isEmpty()):
                strWorktypedesc=worktypeSet.getMbo(0).getString("wtypedesc")
    worktypeSet=None      
    return strWorktypedesc

def getWostatusdesc(strWostatus):
    strWostatusdesc=None
    synonymSet = MXServer.getMXServer().getMboSet("SYNONYMDOMAIN", mbo.getUserInfo())
    synonymSet.setUserWhere("value='" + strWostatus +"' and domainid='WOSTATUS' ")
    if (not synonymSet.isEmpty()):
                strWostatusdesc=synonymSet.getMbo(0).getString("description")
    synonymSet=None      
    return strWostatusdesc

def getLblmaxvarvalue(strVarname):
    strLblvarvalue=None
    lblmaxvarSet = MXServer.getMXServer().getMboSet("LBL_MAXVARS", mbo.getUserInfo())
    lblmaxvarSet.setUserWhere("varname='" + strVarname +"' and orgid='LBNL' and siteid='FAC' ")
    if (not lblmaxvarSet.isEmpty()):
                strLblvarvalue=lblmaxvarSet.getMbo(0).getString("varvalue")
    lblmaxvarSet=None      
    return strLblvarvalue

def getPropertyvalue(strProperty):
    strPropertyValue=None
    maxpropvalueSet = MXServer.getMXServer().getMboSet("maxpropvalue", mbo.getUserInfo())
    maxpropvalueSet.setUserWhere("propname='" + strProperty +"'")
    if (not maxpropvalueSet.isEmpty()):
                strPropertyValue=maxpropvalueSet.getMbo(0).getString("propvalue")
    maxpropvalueSet=None      
    return strPropertyValue

def getEmailaddress(strPersonid):
    strEmail=None
    emailSet = MXServer.getMXServer().getMboSet("email", mbo.getUserInfo())
    emailSet.setUserWhere("personid='" + strPersonid +"' and isprimary=1 ")
    if (not emailSet.isEmpty()):
                strEmail=emailSet.getMbo(0).getString("emailaddress")
    emailSet=None      
    return strEmail



if (jIOrgid=="LBNL" and jISiteid=="FAC"):
   
   wo=mbo
   
   if (jIStatus_modified == True and (jIStatus=="WREL" or jIStatus=="REL" or jIStatus=="RFI" or jIStatus=="WCOMP")):
       
       # Get the values for various properties from lbl_maxvars and system properties
       strEnvironment=getLblmaxvarvalue("APPLICATION_ENV")
       strWorelurl=getLblmaxvarvalue("WOREL_URL")
       strWpcemail=getLblmaxvarvalue("FACWPC_EMAIL")
       strAdminemail=getPropertyvalue("mxe.adminEmail")
       strTawdhelpurl=getLblmaxvarvalue("TAWDHELP_URL")
       strMailhost=getPropertyvalue("mail.smtp.host")
       strFooter=""
       strSubjectline=""
    
       if (isBlank(jIMemo) == True):
           strWostatusmemo=" "
       else:
            strWostatusmemo=jIMemo        
       
                  
       strReleaseStatus=wo.getString("LBL_RELEASE_STATUS")
              
       if (wo.getDate("targstartdate") is not None):
           strTargStartDate = SimpleDateFormat("MM/dd/yyyy").format(wo.getDate("targstartdate")) 
       else:
           strTargStartDate=""
       if (wo.getDate("targcompdate") is not None):
           strTargCompDate = SimpleDateFormat("MM/dd/yyyy").format(wo.getDate("targcompdate"))
       else:
           strTargCompDate =""
           
       # Get supervisor, reportedby and lead name
       strSupervisorname=getPersonname(wo.getString("supervisor"))
       strReportedbyname=getPersonname(wo.getString("reportedby"))
       strLead=wo.getString("lead")
       if (isBlank(strLead) == True):
           strLead=""
           strLeadName=""
       else:
           strLeadName=getPersonname(wo.getString("lead")) 
       
       strMemo=wo.getString("LBL_CONDITION_REL_LONGDESCRIPTION")
       if (isBlank(strMemo)== True):
            strMemo=""
       strLongdesc=wo.getString("description_longdescription")
       if (isBlank(strLongdesc)== True):   
              strLongdesc=""
       
       if (strEnvironment !="PRODUCTION"):
           strSubjectline="[TEST] "   
           strFooter ="<TR><TD>&nbsp;</TD></TR><TR><TD><B>[This email is generated from the TEST data and it does not represent the actual data.]</TD></TR>" 
           
       # Work order status is changed to request for information or released
       if (jIStatus=="RFI" or jIStatus=="REL"):
           strSubjectline +="Facilities Work Order " + wo.getString("wonum")+ " status is changed to " +  jIStatus  +"."

           strBody  ="<HTML><HEAD><TITLE>Work order status changed</TITLE></HEAD>"
           strBody +="<BODY>"
           strBody +="<TABLE>"
           strBody +="<TR><TD>"
           strBody +="<TR><TD>Dear " + strSupervisorname + "</TD><TR>"
           strBody +="<TR><TD>&nbsp;</TD></TR>"
           strBody += " The status of Facilities Work order" + " "
           strBody +=   wo.getString("wonum") + "  is changed to " + jIStatus+ "."
           strBody +=" Given below are the details of the work order: "
           strBody +="<TR><TD>"
           strBody +="<TABLE BORDER=1 ALIGN=LEFT>"
           strBody +="<TR><TD><B>Work Order Number</B></TD><TD><B>"  + wo.getString("wonum") +"</B></TD></TR>"
           strBody +="<TR><TD><B>Requested work</B></TD><TD><B>" + wo.getString("description")  +"</B></TD></TR>"
           strBody +="<TR><TD><B>Long Description</B></TD><TD><B>" + wo.getString("description_longdescription")  +"</B></TD></TR>"
           strBody +="<TR><TD><B>Work type</B></TD><TD><B>"          + wo.getString("worktype")  + " - " + getWorktypedesc(wo.getString("worktype")) +"</B></TD></TR>"
           strBody +="<TR><TD><B>Reported By</B></TD><TD><B>" +wo.getString("reportedby")  + " - " + strReportedbyname +"</B></TD></TR>"
           strBody +="<TR><TD><B>Date Reported</B></TD><TD><B>" + SimpleDateFormat("MM/dd/yyyy").format(wo.getDate("reportdate"))+"</B></TD></TR>"
           strBody +="<TR><TD><B>Lead</B></TD><TD><B>"  + wo.getString("lead")  + " - " + strLeadName +"</B></TD></TR>"
           strBody +="<TR><TD><B>Supervisor</B></TD><TD><B>"  + wo.getString("supervisor")  + " - " + strSupervisorname +"</B></TD></TR>"
           strBody +="<TR><TD><B>Location</B></TD><TD><B>"  + wo.getString("location")  +"</B></TD></TR>"
           strBody +="<TR><TD><B>Current Status</B></TD><TD><B>"  + jIStatus + " - " + getWostatusdesc(jIStatus)
           strBody +="<TR><TD><B>Status memo</B></TD><TD><B>" + strWostatusmemo +"</B></TD></TR>"
           strBody +="<TR><TD><B>Status Date</B></TD><TD><B>" + SimpleDateFormat("MM/dd/yyyy").format(mbo.getDate("changedate"))+"</B></TD></TR>"
           strBody +="<TR><TD><B>Target Start Date</B></TD><TD><B>" +strTargStartDate+"</B></TD></TR>"
           strBody +="<TR><TD><B>Target Completion Date</B></TD><TD><B>" +strTargCompDate +"</B></TD></TR>"
           strBody +="<TR><TD><B>Comments about conditional release</B></TD><TD><B>" + strMemo +"</B></TD></TR>"
           strBody +="</TABLE>"
           strBody +="</TD></TR>"
    
           strBody +="<TR><TD>&nbsp;</TD></TR>"
           strBody +="<TR><TD>"
           strBody +=" Please contact the concerned authorizer/s in case the status of the work order is changed to Request for Information (RFI) </TD.</TR> "
           strBody +="</TD></TR>"
           strBody +="<TR><TD>&nbsp;</TD></TR>"
           strBody += strFooter 
           strBody +="</TD></TR>"
           strBody += "</TABLE></BODY></HTML>"
           
           strToEmail=""
           
           # Email to supervisor and WPC 
           if (strEnvironment =="PRODUCTION"):
               strToEmail=getEmailaddress(wo.getString("supervisor")) + "," + strWpcemail
           else:
                strWhere  = " persongroup='FASUPERTEST'" 
                mbosetremote = MXServer.getMXServer().getMboSet("persongroupteam", mbo.getUserInfo())
                mbosetremote.setUserWhere(strWhere)
                
                if (not mbosetremote.isEmpty()):
                    
                    intCount=mbosetremote.count()                                       
                    for i in xrange(intCount):                             
                        if (mbosetremote.getMbo(i) is not None ):                                           
                            thismbo=mbosetremote.getMbo(i)
                                                                                    
                            if (isBlank(strToEmail) == True):
                                strToEmail=getEmailaddress(thismbo.getString("resppartygroup")) 
                            else:
                                strToEmail = strToEmail +"," + getEmailaddress(thismbo.getString("resppartygroup"))
                                
                                                           
           if (isBlank(strToEmail) == False):
               wo.LblSendMail(strMailhost, strWpcemail, strToEmail, "", strSubjectline,  "HTML", strBody)
                     
               
              
           # ***************************************************************************************************
           # Now start preparing to send email to all authorizers of that location indicated on the work order
           #***************************************************************************************************
                               
           strBody10=""
           strBody30=""
                                          
           strBody10  ="<HTML><HEAD><TITLE>Work order status changed to "+ jIStatus + "  </TITLE></HEAD>"
           strBody10 +="<BODY>"
           strBody10 +="<TABLE>"               
           strBody10 +="<TR><TD>"
         
           strBody30 ="<TR><TD>&nbsp; </TD></TR>"
           strBody30 += " The status of Facilities Work order" + " "
           strBody30 +=   wo.getString("wonum") + "  is changed to " + jIStatus + "."
           strBody30  +=" Given below are the details of the work order: "
           strBody30 +="<TR><TD>"
           strBody30 +="<TABLE BORDER=1 ALIGN=LEFT>"
           strBody30 +="<TR><TD><B>Work Order Number</B></TD><TD><B>"  + wo.getString("wonum") +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Requested work</B></TD><TD><B>" + wo.getString("description")  +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Long Description</B></TD><TD><B>" + strLongdesc  +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Work type</B></TD><TD><B>"          + wo.getString("worktype")  + "-" + getWorktypedesc(wo.getString("worktype")) +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Reported By</B></TD><TD><B>" +wo.getString("reportedby")  + " - " + strReportedbyname +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Date Reported</B></TD><TD><B>" + SimpleDateFormat("MM/dd/yyyy").format(wo.getDate("reportdate")) +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Lead</B></TD><TD><B>"  + strLead  + " - " + strLeadName +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Supervisor</B></TD><TD><B>"  + wo.getString("supervisor")  + " - " + strSupervisorname +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Location</B></TD><TD><B>"  + wo.getString("location")  +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Current Status</B></TD><TD><B>"  + jIStatus + " - " + getWostatusdesc(jIStatus)  +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Status memo</B></TD><TD><B>" + strWostatusmemo +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Status Date</B></TD><TD><B>" + SimpleDateFormat("MM/dd/yyyy").format(wo.getDate("changedate")) +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Target Start Date</B></TD><TD><B>" +strTargStartDate+"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Target Completion Date</B></TD><TD><B>" +strTargCompDate+"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Comments about conditional release</B></TD><TD><B>" +strMemo+"</B></TD></TR>"
           strBody30 +="</TABLE>"
           strBody30 +="</TD></TR>"
           strBody30 +="<TR><TD>&nbsp; </TD></TR>"
           strBody30 +="<TR><TD>&nbsp; </TD></TR>"
           strBody30 += strFooter 
           strBody30 +="</TD></TR>"
           strBody30 += "</TABLE></BODY></HTML>"
           
           # Now start getting authorizers based upon environment variable
  
           if (strEnvironment =="PRODUCTION"):
               strWhere  = " location='"   +  wo.getString("location") +"'"
               strWhere +="  and siteid='" +  wo.getString("siteid") +"'"
               strWhere +="  and receive_email='Y' "
               mbosetremote = MXServer.getMXServer().getMboSet("LBL_AUTH_RELEASE", mbo.getUserInfo())
           else:
               strWhere  = " persongroup='FASUPERTEST' " 
               mbosetremote = MXServer.getMXServer().getMboSet("persongroupteam", mbo.getUserInfo())
                        
           
           mbosetremote.setUserWhere(strWhere)
           
           if (not mbosetremote.isEmpty()):
                                      
                   intCount=mbosetremote.count()                                          
                   for i in xrange(intCount):
                                                    
                        if (mbosetremote.getMbo(i) is not None ):                                           
                            thismbo=mbosetremote.getMbo(i)
                            if (strEnvironment !="PRODUCTION"):
                               strPersonid=thismbo.getString("resppartygroup") 
                            else:
                               strPersonid=thismbo.getString("personid") 
                          
                            # Get employee name
                            strDisplayname=getPersonname(strPersonid) 
                            strBody20  ="<TR><TD>Dear " + strDisplayname + "</TD><TR>" 
    
                            strEmail=getEmailaddress(strPersonid) 
                                                                       
                            if (isBlank(strEmail)==False):                              
                         
                                  strBody=strBody10 + strBody20+ strBody30
                                  
                                                            
                                  #Now send the actual email using HTML as content type
                                  wo.LblSendMail(strMailhost, strAdminemail, strEmail, "", strSubjectline,  "HTML", strBody)
                                   
                            
         
            
       # Work order status changed to Waiting to be released
       if (jIStatus=="WREL"):
           strSubjectline +="Facilities Work Order " + wo.getString("wonum") + " is waiting for your release" 
           strBody10  ="<HTML><HEAD><TITLE>Work order Waiting for release</TITLE></HEAD>" 
           strBody10 +="<BODY>" 
           strBody10 +="<TABLE>" 
           strBody10 +="<TR><TD>" 
    
           strBody30  ="<TR><TD>&nbsp; </TD></TR>" 
           strBody30 += " The status of Facilities Work order " 
           strBody30 +=   wo.getString("wonum") + " is changed to waiting for release (WREL).&nbsp; " 
           strBody30 +=" Given below are the details of the work order: " 
           strBody30 +="<TR><TD>" 
           strBody30 +="<TABLE BORDER=1 ALIGN=LEFT>" 
           strBody30 +="<TR><TD><B>Work Order Number</B></TD><TD><B>"  + wo.getString("wonum") +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Requested work</B></TD><TD><B>" + wo.getString("description")  +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Long Description</B></TD><TD><B>" + wo.getString("description_longdescription")  +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Work type</B></TD><TD><B>"          + wo.getString("worktype")  + "-" + getWorktypedesc(wo.getString("worktype")) +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Reported By</B></TD><TD><B>" +wo.getString("reportedby") + "  -  " + strReportedbyname +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Date Reported</B></TD><TD><B>" + SimpleDateFormat("MM/dd/yyyy").format(wo.getDate("reportdate")) +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Lead</B></TD><TD><B>"  + strLead  + " - " + strLeadName +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Supervisor</B></TD><TD><B>"  + wo.getString("supervisor")  + " - " + strSupervisorname +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Location</B></TD><TD><B>"  + wo.getString("location")  +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Current Status</B></TD><TD><B>"  + jIStatus + " - " + getWostatusdesc(jIStatus) +"</B></TD></TR>"
           strBody30 +="<TR><TD><B>Status memo</B></TD><TD><B>" + strWostatusmemo +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Status Date</B></TD><TD><B>" +SimpleDateFormat("MM/dd/yyyy").format(mbo.getDate("changedate")) +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Target Start Date</B></TD><TD><B>" +strTargStartDate +"</B></TD></TR>" 
           strBody30 +="<TR><TD><B>Target Completion Date</B></TD><TD><B>" +strTargCompDate+"</B></TD></TR>" 
           strBody30 +="</TABLE>" 
           strBody30 +="</TD></TR>"
    
           strBody30 +="<TR><TD>&nbsp; </TD></TR>"
           strBody30 +="<TR><TD>"
           strBody30 +=" In order for the Facilities commence work, you are requested to either change the status of the work order "
           strBody30 +=" to release. Alternatively, you can change the status of the work order to request for more information.  </TD></TR>"
           strBody30 +="</TD></TR>"
            
           strBody30 +="<TR><TD>&nbsp; </TD></TR>" 
           strBody30 +="<TR><TD>" 
           strBody30 +="<A href=" + strTawdhelpurl +">" 
           strBody30   +="<B>Click here for details on your responsibilities in releasing this work area</B>" 
           strBody30   +="</A>" 
           strBody30   +="</TD></TR>" 
                    
           strBody30 +="<TR><TD>&nbsp; </TD></TR>" 
           strBody30 +="<TR><TD>" 
           strBody30 +="<A href=" + strWorelurl +">" 
           strBody30   +="<B>Please click on this link to change the status of this work order.</B>" 
           strBody30   +="</A>" 
           strBody30   +="</TD></TR>" 
    
           strBody30   +="<TR><TD>&nbsp; </TD></TR>" 
           strBody30  +="<TR><TD>" 
               
           strBody30  +="<B>You can contact the Facilities Work Planning and Control group " + strWpcemail  + " or dial x6300 for any clarifications.</B>" 
           
           strBody30  +="</TD></TR>" 
           strBody30  += strFooter  
           strBody30  +="</TD></TR>" 
           strBody30  += "</TABLE></BODY></HTML>" 
       
           strFrom=getEmailaddress(wo.getString("supervisor"))
                
          # Now start getting authorizers based upon environment variable
           

           if (strEnvironment =="PRODUCTION"):
               strWhere  = " location='"   +  wo.getString("location") +"'"
               strWhere +="  and siteid='" +  wo.getString("siteid") +"'"
               strWhere +=" and receive_email='Y' "
           
               mbosetremote = MXServer.getMXServer().getMboSet("LBL_AUTH_RELEASE", mbo.getUserInfo())
           else:
               strWhere  = " persongroup='FASUPERTEST'" 
               mbosetremote = MXServer.getMXServer().getMboSet("persongroupteam", mbo.getUserInfo())
           
           
           mbosetremote.setUserWhere(strWhere)
           
           if (not mbosetremote.isEmpty()):
                              
               intCount=mbosetremote.count()
               
                                                      
               for i in xrange(intCount):
                  
                            
                    if (mbosetremote.getMbo(i) is not None ):                                           
                        thismbo=mbosetremote.getMbo(i)
                               
                        if (strEnvironment !="PRODUCTION"):
                               strPersonid=thismbo.getString("resppartygroup") 
                        else:
                               strPersonid=thismbo.getString("personid") 
                        # Get employee name
                        strDisplayname=getPersonname(strPersonid) 
                        strBody20  ="<TR><TD>Dear " + strDisplayname + "</TD><TR>" 
    
                        strEmail=getEmailaddress(strPersonid)
                                                                  
                                                 
                        if (isBlank(strEmail)==False):
                          
                            strBody=strBody10 + strBody20+ strBody30                   
                            # Now send the actual email using HTML as content type
                                    
                            wo.LblSendMail(strMailhost, strFrom, strEmail, "", strSubjectline,  "HTML", strBody)
                                                                                     
                                                  
       # Work order status is changed to Waiting to be completed
       
       if (jIStatus=="WCOMP"):
           if (isBlank(wo.getString("lead") == False)):
               
               strSubjectline +="Facilities Work Order " + wo.getString("wonum") + " status is changed to " +  jIStatus  +"."
               strBody  ="<HTML><HEAD><TITLE>Work order status changed</TITLE></HEAD>"
               strBody +="<BODY>"
               strBody +="<TABLE>"
               strBody +="<TR><TD>"
               strBody +="<TR><TD>Dear " + strLeadName + "</TD><TR>"
               strBody +="<TR><TD>&nbsp;</TD></TR>"
               strBody += " The status of Facilities Work order" + " "
               strBody +=   wo.getString("wonum") + "  is changed to " + jIStatus + "."
               strBody +=" Given below are the details of the work order: "
               strBody +="<TR><TD>"
               strBody +="<TABLE BORDER=1 ALIGN=LEFT>"
               strBody +="<TR><TD><B>Work Order Number</B></TD><TD><B>"  + wo.getString("wonum") +"</B></TD></TR>"
               strBody +="<TR><TD><B>Requested work</B></TD><TD><B>" + wo.getString("description")  +"</B></TD></TR>"
               strBody +="<TR><TD><B>Long Description</B></TD><TD><B>" + wo.getString("description_longdescription")  +"</B></TD></TR>"
               strBody +="<TR><TD><B>Work type</B></TD><TD><B>"          + wo.getString("worktype")  + "-" + getWorktypedesc(wo.getString("worktype")) +"</B></TD></TR>"
               strBody +="<TR><TD><B>Reported By</B></TD><TD><B>" +wo.getString("reportedby")  + " - " + strReportedbyname +"</B></TD></TR>"
               strBody +="<TR><TD><B>Date Reported</B></TD><TD><B>" + SimpleDateFormat("MM/dd/yyyy").format(wo.getDate("reportdate")) +"</B></TD></TR>"
               strBody +="<TR><TD><B>Lead</B></TD><TD><B>"  + wo.getString("lead")  + " - " + strLeadName +"</B></TD></TR>"
               strBody +="<TR><TD><B>Location</B></TD><TD><B>"  + wo.getString("location")  +"</B></TD></TR>"
               strBody +="<TR><TD><B>Current Status</B></TD><TD><B>"  + jIStatus +"</B></TD></TR>"
               strBody +="<TR><TD><B>Status memo</B></TD><TD><B>" + strWostatusmemo +"</B></TD></TR>"
               strBody +="<TR><TD><B>Status Date</B></TD><TD><B>" +SimpleDateFormat("MM/dd/yyyy").format(wo.getDate("changedate")) +"</B></TD></TR>"
               strBody +="<TR><TD><B>Target Start Date</B></TD><TD><B>" + strTargStartDate +"</B></TD></TR>"
               strBody +="<TR><TD><B>Target Completion Date</B></TD><TD><B>" + strTargCompDate +"</B></TD></TR>"
               strBody +="<TR><TD><B>Comments about conditional release</B></TD><TD><B>" +strMemo+"</B></TD></TR>"
               strBody +="</TABLE>"
               strBody +="</TD></TR>"
        
               strBody +="<TR><TD>&nbsp;</TD></TR>"
               strBody +="<TR><TD>&nbsp;</TD></TR>"
               strBody += strFooter 
               strBody +="</TD></TR>"
               strBody += "</TABLE></BODY></HTML>"
               strToEmail=""
               
            
               if (strEnvironment =="PRODUCTION"):
                    strToEmail=getEmailaddress(strLead)
               else:
                    strWhere  = " persongroup='FASUPERTEST'" 
                    mbosetremote = MXServer.getMXServer().getMboSet("persongroupteam", mbo.getUserInfo())
                    mbosetremote.setUserWhere(strWhere)
                    
                    if (not mbosetremote.isEmpty()):
                        
                        intCount=mbosetremote.count()                                         
                        for i in xrange(intCount):                             
                            if (mbosetremote.getMbo(i) is not None ):                                           
                                thismbo=mbosetremote.getMbo(i)                                                     
                                if (isBlank(strToEmail)== True):
                                    strToEmail=getEmailaddress(thismbo.getString("resppartygroup")) 
                                else:
                                     strToEmail = strToEmail +"," + getEmailaddress(thismbo.getString("resppartygroup"))
                                    
                               
                                      
               if (isBlank(strToEmail) == False):
                    emailList = strToEmail.split(",")
                    # Loop the list.
                    for strTo in emailList:
                        wo.LblSendMail(strMailhost, strAdminemail, strTo, "", strSubjectline,  "HTML", strBody)
                                   
       
       