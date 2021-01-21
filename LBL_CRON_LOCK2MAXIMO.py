####################################################################
# Purpose: Script for synchronizing Lockshop transactions 
#          into MAXIMO 7.6
#
# Author : Pankaj Bhide
#
# Date    : Dec 13, 2015 
#
# Revision
# History : June 14, 19 Pankaj - Changed source table (local MBO)
#
#           Oct 30, 2020 Pankaj - This script only sends email to lockshop
##########################################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import Date
from java.text import SimpleDateFormat
from java.lang import System

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def getPersondivision(strPersonid):
    strPersondivision=None
    personSet = MXServer.getMXServer().getMboSet("PERSON", runAsUserInfo1)
    personSet.setUserWhere("personid='" + strPersonid +"'")
    if (not personSet.isEmpty()):
                strPersondivision=personSet.getMbo(0).getString("lbl_org_level_1")
    personSet=None      
    return strPersondivision


def getPersonname(strPersonid):
    strPersonname=None
    personSet = MXServer.getMXServer().getMboSet("PERSON", runAsUserInfo1)
    personSet.setUserWhere("personid='" + strPersonid +"'")
    if (not personSet.isEmpty()):
                strPersonname=personSet.getMbo(0).getString("displayname")
    personSet=None      
    return strPersonname

def getPhone(strPersonid):
    strPhone=None
    phoneSet = MXServer.getMXServer().getMboSet("PHONE", runAsUserInfo1)
    phoneSet.setUserWhere("isprimary=1 and personid='" + strPersonid +"'")
    if (not phoneSet.isEmpty()):
                strPhone=phoneSet.getMbo(0).getString("phonenum")
    phoneSet=None      
    return strPhone

def getGLDesc(strGlaccount):
    strGLDesc=None
    glSet = MXServer.getMXServer().getMboSet("CHARTOFACCOUNTS", runAsUserInfo1)
    glSet.setUserWhere("glaccount='" + strGlaccount +"' and orgid='LBNL' and active=1 ")
    if (not glSet.isEmpty()):
                strGLDesc=glSet.getMbo(0).getString("accountname")
    glSet=None      
    return strGLDesc

def getLblmaxvarvalue(strVarname):
    strLblvarvalue=None
    lblmaxvarSet = MXServer.getMXServer().getMboSet("LBL_MAXVARS", runAsUserInfo1)
    lblmaxvarSet.setUserWhere("varname='" + strVarname +"' and orgid='LBNL' and siteid='FAC' ")
    if (not lblmaxvarSet.isEmpty()):
                strLblvarvalue=lblmaxvarSet.getMbo(0).getString("varvalue")
    lblmaxvarSet=None      
    return strLblvarvalue

def getPropertyvalue(strProperty):
    strPropertyValue=None
    maxpropvalueSet = MXServer.getMXServer().getMboSet("maxpropvalue", runAsUserInfo1)
    maxpropvalueSet.setUserWhere("propname='" + strProperty +"'")
    if (not maxpropvalueSet.isEmpty()):
                strPropertyValue=maxpropvalueSet.getMbo(0).getString("propvalue")
    maxpropvalueSet=None      
    return strPropertyValue

def getEmailaddress(strPersonid):
    strEmail=None
    emailSet = MXServer.getMXServer().getMboSet("email", runAsUserInfo1)
    emailSet.setUserWhere("personid='" + strPersonid +"' and isprimary=1 ")
    if (not emailSet.isEmpty()):
                strEmail=emailSet.getMbo(0).getString("emailaddress")
    emailSet=None      
    return strEmail

def getClassification(strDescription):
    strClassification=None    
    strWhere="  1=1  "
    strWhere +=" and description='" + strDescription +"'"
    strWhere +=" and orgid='LBNL' "
    strWhere +=" and siteid='FAC'"
    clsSet = MXServer.getMXServer().getMboSet("classstructure",runAsUserInfo1)
    clsSet.setUserWhere(strWhere)
    if (not clsSet.isEmpty()):
                strClassification=clsSet.getMbo(0).getString("classstructureid")
    clsSet=None      
    return strClassification


mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
strLogs=[]   # Array for storing logs for sending email to lockshop(delimited by pipe)


lbl_facworkrequestRemote= MXServer.getMXServer().getMboSet("lbl_facworkrequest", runAsUserInfo1)
lbl_maxvarsRemote= MXServer.getMXServer().getMboSet("lbl_maxvars", runAsUserInfo1)


strLineSep=System.getProperty("line.separator")
strLineSep=strLineSep + System.getProperty("line.separator")


strGlobalrush=""
chrDblquote="\""

rowcnt=0
strWhere  ="requesttype in (" + "'NEWKEY'" + ","+ "'TRANSFERKEY')"
strWhere +=" and reportdate >= (select to_date(varvalue,"+ "'YYYY-MM-DD HH24:MI:SS')" + " from lbl_maxvars where varname="+ "'DT_LOCKSHOPWOEMAIL'"  +")"


lbl_facworkrequestRemote.setUserWhere(strWhere)
lbl_facworkrequestRemote.reset()

if lbl_facworkrequestRemote is not None:
    lbl_facworkrequest=lbl_facworkrequestRemote.moveFirst()
    while lbl_facworkrequest:
        rowcnt=rowcnt+1
        
        strRush="No"
        if (lbl_facworkrequest.getBoolean("isrush")== True):
            strRush="Yes"
        
        strSubmittedby=getPersonname(lbl_facworkrequest.getString("keyreceiver"))
        if (isBlank(strSubmittedby)):
            strSubmittedby=""
            
        strReqPhone=lbl_facworkrequest.getString("requestorphone")
        if (isBlank(strReqPhone)):
            strReqPhone=""
        
        strAuthorizer=getPersonname(lbl_facworkrequest.getString("keyauthorizer"))
        if (isBlank(strAuthorizer)):
            strAuthorizer=""
        
        strBuilding=lbl_facworkrequest.getString("building")
        if (isBlank(strBuilding)):
            strBuilding=""
        
        strRoom=lbl_facworkrequest.getString("room")
        if (isBlank(strRoom)):
            strRoom=""
            
        strProject=lbl_facworkrequest.getString("project_id")
        if (isBlank(strProject)):
            strProject=""
        
        strActivity=lbl_facworkrequest.getString("activity_id")
        if (isBlank(strActivity)):
            strActivity=""
            
        strDescription=lbl_facworkrequest.getString("description")
        if (isBlank(strDescription)):
            strDescription=""
            
        if (lbl_facworkrequest.getMboValueData("keydateneeded").isNull()):
            strDateNeeded=""
        else:
            strDateNeeded=SimpleDateFormat("MM/dd/yyyy").format(lbl_facworkrequest.getDate("keydateneeded"))
            
        strTemp=lbl_facworkrequest.getString("documenttype")+"|" + lbl_facworkrequest.getString("documentnumber") + "|" 
        strTemp += strDescription + "|" + strRush +"|" + strSubmittedby+"|"+  SimpleDateFormat("MM/dd/yyyy").format(lbl_facworkrequest.getDate("reportdate"))
        strTemp += "|" + lbl_facworkrequest.getString("mailstop") + "|" + strReqPhone + "|" +strAuthorizer
        strTemp += "|" + strBuilding + "|" + strRoom + "|" + strProject + "|" + strActivity
        strTemp += "|" + strDateNeeded
        strLogs.append(strTemp)
    
        lbl_facworkrequest = lbl_facworkrequestRemote.moveNext()
        
   

#Send send email only after all the transactions have been read
if (rowcnt >= 1 ):
    strLogslength=len(strLogs)
                   
    strEnvironment=getLblmaxvarvalue("APPLICATION_ENV")
    strFooter=""
    if (strEnvironment !="PRODUCTION"):
        strFooter="[TEST] This email is generated using non production data and it does not reflect the real data"        
        strSubject="[TEST] Lockshop Work orders/SR  Log"
    else:
       
        strSubject="Lockshop Work orders/SR  Log"
            
    strEmailBody="<html><head><title>Lockshop Work orders/SR  Log</title></head><body>"
    strEmailBody +="<P align=\"center\"><FONT face=\"Arial\" size=\"4\"><STRONG><U>Lawerence Berkeley Laboratory</U></STRONG></FONT></P>"
    strEmailBody +="<P align=\"center\"><FONT face=\"Arial\" size=\"4\"><STRONG><U>Log of Lockshop Work orders SR</U></STRONG></FONT></P>"
    strEmailBody +="<TABLE cellspacing=\"1\" cellpadding=\"1\" align=\"center\" border=\"2\"> "
    strEmailBody +="<TR>"  
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Number</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Description</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Rush </FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Document type</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">ID</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Submitted By</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Submitted Date</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Mailstop</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Requestor Phone</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Authorizer</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Building</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Room</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Project Id</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Acitivity Id</FONT></TD>"
    strEmailBody +="<TD align=\"center\"><FONT face=\"Arial\" size=\"4\">Date Needed</FONT></TD>"   
  
    strEmailBody +="</TR>"
    
    # Iterate array
    strLogslength=len(strLogs)
    for i in range(0,strLogslength):
        
        strLogline=strLogs[i]
        strSplitLogline=strLogline.split("|")
        strDoctype=strSplitLogline[0]
        strDocumentno=strSplitLogline[1]
        strDescription=strSplitLogline[2]
        strRush=strSplitLogline[3]
        strSubmittedby=strSplitLogline[4]
        strSubmitdate=strSplitLogline[5]
        strMailstop=strSplitLogline[6]
        strReqPhone=strSplitLogline[7]
        strAuthorizer=strSplitLogline[8]
        strBuilding=strSplitLogline[9]
        strRoom=strSplitLogline[10]
        strProject=strSplitLogline[11]
        strActivity=strSplitLogline[12]
        strDateNeeded=strSplitLogline[13]
        
               
        strEmailBody += "<TR> <TD>  <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + str(i+1)+ "</FONT> </TD>"
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strDescription + "</FONT> </TD>"
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +"  color=" + chrDblquote + "RED" + chrDblquote + ">" + strRush + "</FONT> </TD>" 
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strDoctype + "</FONT> </TD>"
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strDocumentno + "</FONT> </TD>"
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strSubmittedby + "</FONT> </TD>"
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strSubmitdate + "</FONT> </TD> "
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strMailstop + "</FONT> </TD> "
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strReqPhone + "</FONT> </TD> "
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strAuthorizer + "</FONT> </TD> "
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strBuilding + "</FONT> </TD> "
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strRoom + "</FONT> </TD> "
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strProject + "</FONT> </TD> "
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strActivity + "</FONT> </TD> "
        strEmailBody += "<TD>   <FONT face="+ chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote +"4" + chrDblquote +">" + strDateNeeded + "</FONT> </TD> </TR>"
        
                
          
   
    strEmailBody +=" </table><br><br><br>"
    strEmailBody +="<P align=" + chrDblquote + "center" + chrDblquote + "><FONT face=" + chrDblquote + "Arial" + chrDblquote + " size=" + chrDblquote + "4" + chrDblquote + ">"
    strEmailBody +="<STRONG>" +  strFooter +"</STRONG></FONT></P>"
    strEmailBody +="</body></html>"

    
    
    # Now send email to lockshop group
    strWhere  = " persongroup='FAWRCLOCKSHOP' " 
    persongroupremote= MXServer.getMXServer().getMboSet("persongroupteam", runAsUserInfo1)         
    persongroupremote.setUserWhere(strWhere)
    if (not persongroupremote.isEmpty()):
        intCount=persongroupremote.count()                                          
        for i in xrange(intCount):                                                    
            if (persongroupremote.getMbo(i) is not None ):
                strPersonid=persongroupremote.getMbo(i).getString("resppartygroup")
                strToEmail=getEmailaddress(strPersonid)
                strWhereWO=" rownum=1"
                woset2Remote=MXServer.getMXServer().getMboSet("WORKORDER", runAsUserInfo1)         
                woset2Remote.setUserWhere(strWhereWO)
                wombo=woset2Remote.getMbo(0)
                wombo.LblSendMail("smtp.lbl.gov", "iss-fac@lbl.gov", strToEmail, "", strSubject,  "HTML", strEmailBody)
                wombo.LblSendMail("smtp.lbl.gov", "iss-fac@lbl.gov", 'PBhide@lbl.gov', "", strSubject,  "HTML", strEmailBody)
                
   
   
    wosetRemote=None
    lbl_facworkrequestRemote=None
    lbl_maxvarsRemote.setUserWhere("varname='" + "DT_LOCKSHOPWOEMAIL" +"'")
    lbl_maxvarsRemote.reset()
    if lbl_maxvarsRemote is not None:
        strCurrentDateTime= SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(Date())
        lbl_maxvarsRemote.getMbo(0).setValue("varvalue",strCurrentDateTime)
        lbl_maxvarsRemote.save()