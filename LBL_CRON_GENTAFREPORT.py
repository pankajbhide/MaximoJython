####################################################################
# Purpose: Script for generating and email the TAF report 
#
# Author : Pankaj Bhide
#
# Date    : Feb 28, 2020
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
from java.lang import System
from com.ibm.tivoli.maximo.report.birt.runtime import ReportParameterData
from java.io import File,FileOutputStream


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def getPersonname(strPersonid):
    strPersonname=None
    personSet = MXServer.getMXServer().getMboSet("PERSON", runAsUserInfo1)
    personSet.setUserWhere("personid='" + strPersonid +"'")
    if (not personSet.isEmpty()):
                strPersonname=personSet.getMbo(0).getString("displayname")
    personSet=None      
    return strPersonname



def getLocationDesc(strLocation):
    strLocationDesc=None
    locationsSet = MXServer.getMXServer().getMboSet("LOCATIONS", runAsUserInfo1)
    locationsSet.setUserWhere("location='" + strLocation+"' and orgid='LBNL' and siteid='FAC' ")
    if (not locationsSet.isEmpty()):
                strLocationDesc=locationsSet.getMbo(0).getString("description")
    locationsSet=None      
    return strLocationDesc


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


strLineSep=System.getProperty("line.separator")
strLineSep=strLineSep + System.getProperty("line.separator")
sdf = SimpleDateFormat("yyyyMMddhhmmss")

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
reportService = mxServer.lookup("BIRTREPORT")

reportParams = ReportParameterData()
strEnvironment=getLblmaxvarvalue("APPLICATION_ENV")

# Get access to lbl_facworkrequest MBO
lbl_facworkrequestRemote= MXServer.getMXServer().getMboSet("lbl_facworkrequest", runAsUserInfo1)
workorderRemote= MXServer.getMXServer().getMboSet("workorder", runAsUserInfo1)

lbl_facworkrequestRemote.setUserWhere("requesttype='TRANSPORTATION' and (datetafsent is null or datetafsent < changedate)")
#lbl_facworkrequestRemote.setUserWhere("documentnumber='W0198993'")
lbl_facworkrequestRemote.reset()

# Read all the rows from lbl_facworkrequest collection 
if (not lbl_facworkrequestRemote.isEmpty()):
    
    intCount=lbl_facworkrequestRemote.count()
    # Loop through each row from the collection
    for i in xrange(intCount):
        lbl_facworkrequestRemote.getMbo(i).setValue("datetafsent", MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        workorderRemote.setUserWhere("orgid='LBNL' and siteid='FAC' and wonum='" +lbl_facworkrequestRemote.getMbo(i).getString("documentnumber") +"'" )
        workorderRemote.reset()
        
        reportParams = ReportParameterData()
        reportParams.addParameter("paramOrg",  lbl_facworkrequestRemote.getMbo(i).getString("orgid"))
        reportParams.addParameter("paramSite", lbl_facworkrequestRemote.getMbo(i).getString("siteid"))
        reportParams.addParameter("paramWO",  lbl_facworkrequestRemote.getMbo(i).getString("documentnumber"))
        strRequestor=lbl_facworkrequestRemote.getMbo(i).getString("requestor")
       

        
        # Prepare file name
        strFileName="LBNL_TAF_" + strRequestor + "_"+ sdf.format(mxServer.getDate()) + ".pdf"
        # 
        tafReport = File("lbnl_reports",  strFileName)
        reportOutput = reportService.runReport(runAsUserInfo1, "lbl_wrc_mov_matl_form_birt.rptdesign", "USER", reportParams, tafReport.getName(), "pdf")
        fileOutput = FileOutputStream(tafReport.getAbsolutePath())
        fileOutput.write(reportOutput)
        fileOutput.flush()
        fileOutput.close()
        strFileAbsolutepath=tafReport.getAbsolutePath()
        #Attachments=strFileAbsolutepath.split(',')
       
        
        reportParams=None
      
        strSubject=""
        strSubject2=""
        strBody=""
        
        if (strEnvironment =="PRODUCTION"):
            strToEmail=getEmailaddress(strRequestor)
        else:
            strWhere  = " persongroup='FASUPERTEST'" 
            mbosetremote = MXServer.getMXServer().getMboSet("persongroupteam", runAsUserInfo1)
            mbosetremote.setUserWhere(strWhere)
            strToEmail=""
            if (not mbosetremote.isEmpty()):
                
                intCount=mbosetremote.count()                                         
                for j in xrange(intCount):                             
                    if (mbosetremote.getMbo(j) is not None ):                                           
                        thismbo=mbosetremote.getMbo(j)                                                     
                        if (isBlank(strToEmail)== True):
                            strToEmail=getEmailaddress(thismbo.getString("resppartygroup")) 
                        else:
                            strToEmail = strToEmail +"," + getEmailaddress(thismbo.getString("resppartygroup"))
            mbosetremote=None   
            strSubject="[TEST] "
            strSubject2="[TEST] "
        
        strSubject +="Transportation authorization form(TAF) for Facilities work order " + workorderRemote.getMbo(0).getString("wonum") + "."
   
        strBody +="<HTML><HEAD></HEAD><BODY>"
        strBody +="<TABLE BORDER=0><TR><TD>"
        strBody +="Hello " + getPersonname(workorderRemote.getMbo(0).getString("reportedby")) + ",<BR><BR>"
        strBody +="Thank you for submitting Facilities Work Order "   + workorderRemote.getMbo(0).getString("wonum") +".<BR><BR>"
        strBody +="Transportation will NOT move anything that does not have&nbsp;"
        strBody +="Transportation Authorization Form(TAF) attached.<BR><BR>"
        strBody +="Per PUB3000 Section 5.8 Transportation can NOT move anything "
        strBody +="that does not have a Transportation Authorization From (TAF) attached.<BR><BR>" 
        
         
        strBody2 ="<TABLE BORDER='1' ALIGN=LEFT>"
        strBody2 +="<TR><TD>Work Order Number</TD><TD>"  + workorderRemote.getMbo(0).getString("wonum") +"</TD></TR>"
        strBody2 +="<TR><TD>Date Requested</TD><TD>" + SimpleDateFormat("MM/dd/yyyy").format(workorderRemote.getMbo(0).getDate("reportdate"))+"</TD></TR>"
        strBody2 +="<TR><TD>Name</TD><TD>" + getPersonname(workorderRemote.getMbo(0).getString("reportedby")) +"</TD></TR>"
        strBody2 +="<TR><TD>Alternate&nbsp;Contact/Responsible&nbsp;Individual</TD><TD>"+getPersonname(workorderRemote.getMbo(0).getString("wo1"))+"</TD></TR>"
        strBody2 +="<TR><TD>Requested work</TD><TD>" + workorderRemote.getMbo(0).getString("description") +"</TD></TR>"
      
        if  isBlank( workorderRemote.getMbo(0).getString("description_longdescription") == False):
            strBody2 +="<TR><TD> Description</TD><TD>" + workorderRemote.getMbo(0).getString("description_longdescription") +"</TD></TR>"
     
        strBody2 +="<TR><TD>Location</TD><TD>" + workorderRemote.getMbo(0).getString("location")+"</TD></TR>"
        strTargCompdate="Not Specified"
        
        if (not workorderRemote.getMbo(0).isNull("TARGCOMPDATE")):
            strTargCompdate=SimpleDateFormat("MM/dd/yyyy").format(workorderRemote.getMbo(0).getDate("targcompdate"))
        
        
        strBody2 +="<TR><TD>Date Needed</TD><TD>" + strTargCompdate + "</TD></TR>"  
        strBody2 +="<TR><TD>Project ID and Activity ID</TD><TD>"  + workorderRemote.getMbo(0).getString("glaccount")+"</TD></TR>"
      
        strBody2 +="</TABLE>"
        
        strBody +=strBody2;
        
        if (( isBlank(lbl_facworkrequestRemote.getMbo(i).getString("deliverybuilding")== False)) and (lbl_facworkrequestRemote.getMbo(i).getString("deliverybuilding")=="STORAGE")):
            # page break
            #strBody +="<h2 style="+ "\"" +"page-break-before: always;" +"\"" +">Storage Request Instructions for Employees</h2>"
            strBody +="<TR><TD>&nbsp;</TD></TR>"
            strBody +="<TR><TD><BIG><B><U>Storage Request Instructions for Employees</U></B></BIG></TD></TR>"
            strBody +="<TR><TD>&nbsp;</TD></TR>"
            strBody +="<TR><TD>All items going to the off-site warehouse must be inspected "
            strBody +="for hazards by EH&amp;S. Please call x6825 to arrange for inspection."
            strBody +="</TD></TR>"
          
            strBody +="<TR><TD>&nbsp;</TD></TR>"
          
            strBody +="<TR><TD>Crated material must be inspected prior to crating. If "
            strBody +="material is already crated, requester may need to remove "
            strBody +="material for inspection at the discretion of the inspector. "
            strBody +="Requester is responsible for sealing crate immediately after "
            strBody +="inspection."
            strBody +="</TD></TR>"
          
            strBody +="<TR><TD>&nbsp;</TD></TR>"
            strBody +="<TR><TD>Uncrated material must be inspected by EH&amp;S in "
            strBody +="conjunction with Transportation pickup."
            strBody +="</TD></TR>"
          
            strBody +="<TR><TD>&nbsp;</TD></TR>"
          
            strBody +="<TR><TD>The Transportation Authorization Form (TAF) must "
            strBody +="be attached to the material being transported."
            strBody +="</TD></TR>"
          
            strBody +="<TR><TD>&nbsp;</TD></TR>"
            strBody +="<TR><TD><I><U>Official Storage</U></I></TD></TR>"
          
            strBody +="<TR><TD>&nbsp;</TD></TR>"
          
            strBody +="<TR><TD>The following can not be placed in Official Storage:"
            strBody +="</TD></TR>"
          
            strBody +="<TR><TD>"
            strBody +="<UL>"
            strBody +="<LI>Property that does not belong to DOE or LBNL</LI>"
            strBody +="<LI>Hazardous materials</LI>"
            strBody +="<LI>Furniture</LI>"
            strBody +="<LI>Computers, monitors, printers</LI>"
            strBody +="<LI>Books, papers, documents</LI>"
            strBody +="<LI>Work benches</LI>"
            strBody +="<LI>Empty crates</LI>"
            strBody +="<LI>Packing material</LI>"
            strBody +="</UL>"
            strBody +="</TD></TR>"
          
            strBody +="<TR><TD>To place items in Official Storage:</TD></TR>"
            strBody +="&nbsp;&nbsp;&nbsp;"
            strBody +="<OL start=1>"
            strBody +="<LI>Complete Storage Request Document and attach to material with TAF </LI>"
            strBody +="<LI>If crating is necessary, enter separate work request for "
            strBody +="crating. Do not seal crate until inspected by EH&amp;S. "
            strBody +="If material has DOE #, write on outside of crate</LI>"
            strBody +="<LI>Arrange inspection with EH&amp;S x6825</LI>"
            strBody +="<LI>Transportation will coordinate delivery to Warehouse.</LI>"
            strBody +="</OL>"
                    
            strBody3 ="<HTML><HEAD></HEAD><BODY>"
            strBody3 +="<TABLE BORDER=0><TR><TD>"
            strBody3 +="Hello, </TD></TR><BR>"
            strBody3 +="<TR><TD> For your information, the following Warehouse "
            strBody3 +="Storage Request work order has been submitted."
            strBody3 +="</TD></TR><BR>"
            strBody3 +=strBody2
            strBody3 +="</TABLE></BODY></HTML>"
          
            strSubject2 +="Warehouse Storage Request against work order " + workorderRemote.getMbo(0).getString("wonum") + "."
        
           
        strBody +="</TABLE></BODY></HTML>"
        lbl_facworkrequestRemote.getMbo(i).setValue("datetafsent", MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        
                                   
                       
                              
        if (isBlank(strToEmail) == False):
            emailList = strToEmail.split(",")
            
        print "PRB: " + str(emailList)
            
            # Loop the list.
        for strTo in emailList:
            print "PRB- in loop: " + strTo
            workorderRemote.getMbo(0).LblSendMailAttachment("smtp.lbl.gov","transportation@lbl.gov",strTo,"", strSubject,"HTML",strBody,strFileAbsolutepath)
                                                           
    
lbl_facworkrequestRemote.save()
lbl_facworkrequestRemote=None

