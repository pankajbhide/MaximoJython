####################################################################
# Purpose: Script for synchronizing CATS transactions 
#          into MAXIMO 7.6
#
# Author : Pankaj Bhide
#
# Date    : Dec 15, 2015 
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

def getPhone(strPersonid):
    strPhone=None
    phoneSet = MXServer.getMXServer().getMboSet("PHONE", runAsUserInfo1)
    phoneSet.setUserWhere("isprimary=1 and personid='" + strPersonid +"'")
    if (not phoneSet.isEmpty()):
                strPhone=phoneSet.getMbo(0).getString("phonenum")
    phoneSet=None      
    return strPhone


def getLocationDesc(strLocation):
    strLocationDesc=None
    locationsSet = MXServer.getMXServer().getMboSet("LOCATIONS", runAsUserInfo1)
    locationsSet.setUserWhere("location='" + strLocation+"' and orgid='LBNL' and siteid='FAC' ")
    if (not locationsSet.isEmpty()):
                strLocationDesc=locationsSet.getMbo(0).getString("description")
    locationsSet=None      
    return strLocationDesc

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

def getDivision(strDivision):
    strDivisiondesc=None
    craftSet= MXServer.getMXServer().getMboSet("CRAFT", runAsUserInfo1)
    craftSet.setUserWhere("lbl_org_level_1='" + strDivision +"' and lbl_org_level_2 is null and lbl_org_level_3 is null and lbl_org_level_4 is null")
    if (not craftSet.isEmpty()):
                strDivisiondesc=craftSet.getMbo(0).getString("description")
    craftSet=None      
    return strDivisiondesc



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
strAllowedCATSstatus="" # String for storing allowing cats status values
strExternrefs=[] # array for holding needed external ref ids 

conKey = mxServer.getSystemUserInfo().getConnectionKey()
wosetRemote= MXServer.getMXServer().getMboSet("WORKORDER", runAsUserInfo1)
woset2Remote= MXServer.getMXServer().getMboSet("WORKORDER", runAsUserInfo1)

# Assumes a database link titled lock2max that connects to lockadm@shrxxx 
# Get JDBC connection from mxserver
 
con = mxServer.getDBManager().getConnection(conKey)
strLineSep=System.getProperty("line.separator")
strLineSep=strLineSep + System.getProperty("line.separator")

#*************************************************************
# Firstly, refresh the status of the work orders found in
# lbl_maximo_cats_stat table from MAXIMO work order table
#*************************************************************
strUpdateStat1  = " UPDATE LBL_MAXIMO_CATS_STATUS   "
strUpdateStat1 += " SET WO_STATUS=?, SUPERVISOR=?, STATUSDATE=?, "
strUpdateStat1 += " MEMO=?, PARENT=?, PARENTID=?,  DATEUPDATED=SYSDATE, "
strUpdateStat1 += " GLACCOUNT=? "
strUpdateStat1 += " WHERE WONUM=? AND ORGID=? AND SITEID=? "
stmtUpdateStat1=con.prepareStatement(strUpdateStat1)

strSelectStat1  = " SELECT A.ORGID, A.SITEID, A.WONUM, B.GLACCOUNT,  "
strSelectStat1 += " B.SUPERVISOR, B.STATUS, B.STATUSDATE, B.PARENT, C.MEMO, "
strSelectStat1 +="  DECODE(INSTR(LTRIM(B.WO4,'CATS-'),'.'),0, LTRIM(B.WO4,'CATS-'), LTRIM(SUBSTR(B.WO4,1,INSTR(B.WO4,'.')-1),'CATS-')) PARENTID "
strSelectStat1 += " FROM LBL_MAXIMO_CATS_STATUS A," 
strSelectStat1 += " MAXIMO.WORKORDER B, MAXIMO.WOSTATUS C " 
strSelectStat1 += " WHERE A.ORGID=B.ORGID AND A.SITEID=B.SITEID  " 
strSelectStat1 += " AND A.WONUM=B.WONUM AND B.ORGID=C.ORGID "
strSelectStat1 += " AND B.SITEID=C.SITEID AND B.WONUM=C.WONUM "
strSelectStat1 += " AND B.STATUS=C.STATUS AND B.STATUSDATE=C.CHANGEDATE"    
strSelectStat1 +="  AND A.WO_STATUS NOT IN ('CAN','CLOSE') "
strSelectStat1 +="  AND A.STATUSDATE != B.STATUSDATE ";         
strSelectStat1 +="  AND A.ORGID="  +"'" + "LBNL"+"'";
strSelectStat1 +="  AND A.SITEID=" +"'" + "FAC"+"'";

myStatement1 = con.prepareStatement(strSelectStat1)             
Rs1=myStatement1.executeQuery();

#Browse through the record set
while Rs1.next():

    stmtUpdateStat1.setString(1,Rs1.getString("STATUS"))
    stmtUpdateStat1.setString(2,Rs1.getString("SUPERVISOR"))
    stmtUpdateStat1.setDate(3,Rs1.getDate("STATUSDATE"))
    stmtUpdateStat1.setString(4,Rs1.getString("MEMO"))
    stmtUpdateStat1.setString(5,Rs1.getString("PARENT"))
    stmtUpdateStat1.setString(6,Rs1.getString("PARENTID"))
    stmtUpdateStat1.setString(7,Rs1.getString("GLACCOUNT"))
    stmtUpdateStat1.setString(8,Rs1.getString("WONUM"))
    stmtUpdateStat1.setString(9,Rs1.getString("ORGID"))
    stmtUpdateStat1.setString(10,Rs1.getString("SITEID"))
    stmtUpdateStat1.executeUpdate()

Rs1.close()
stmtUpdateStat1.close()
con.commit()



Rs1=myStatement1.executeQuery();

#***************************************************************
# Find out list of allowable CATS status and store them
# into list
#****************************************************************
strSelectStat1  = " select varvalue from maximo.lbl_maxvars "
strSelectStat1 += " where varname='ALLOWABLE_CATS_STATUS' "
myStatement1 = con.prepareStatement(strSelectStat1)              
Rs1=myStatement1.executeQuery()
   
# Browse through the record set
while Rs1.next():
      if (isBlank(strAllowedCATSstatus) == True):
          strAllowedCATSstatus=Rs1.getString("varvalue")
      else:
          strAllowedCATSstatus="," + Rs1.getString("varvalue")
     
      
Rs1.close()
myStatement1.close()
         



#********************************************************    
# Updating interface table to set dateexported to sysdate
# so that, the records already processed are not considered
# for the future processing.
#********************************************************    

strUpdateStat1  = "  UPDATE LBL_MAXIMO_CATS_INTFC "
strUpdateStat1  +="  SET   dateimported=SYSDATE, "
strUpdateStat1  +="  IMPORTSTATUS=?, IMPORTMESSAGE=?   "
strUpdateStat1  +="  WHERE DATEIMPORTED IS NULL  "
strUpdateStat1  +="  AND ROWID=? "
strUpdateStat1  +="  AND ORGID="  +"'" + "LBNL"+"'"
strUpdateStat1  +="  AND SITEID=" +"'" + "FAC" +"'"

stmtUpdateStat1=con.prepareStatement(strUpdateStat1)

##########################################################################
# Start reading the un-processed records from MAXIMO-CATS interface table
# and if present, get the latest status of the work order associated with
# the cats record.
##########################################################################
     
strSelectStat1  =" SELECT B.EXTERNALREFID EXTERNALREFID, B.DESCRIPTION, B.REPORTEDBY, "
strSelectStat1 +=" B.REPORTDATE, B.LOCATION, B.UNPARSEDLOCATION,     "
strSelectStat1 +=" NVL(B.GLACCOUNT,'Institutional') GLACCOUNT, NVL(B.INSTITUTIONAL_FLAG,'N')INSTITUTIONAL_FLAG, B.PROGRAM_PROJECT, " 
strSelectStat1 +=" B.APPROVER_EMPLOYEE_ID, B.FINDER_EMPLOYEE_ID, " 
strSelectStat1 +=" NVL(MAXIMO.LBL_MAXIMO_PKG.GET_EMPLOYEE_NAME(B.APPROVER_EMPLOYEE_ID),' ') APPROVER_NAME, "
strSelectStat1 +=" NVL(MAXIMO.LBL_MAXIMO_PKG.GET_EMPLOYEE_NAME(B.INITIATOR_EMPLOYEE_ID),' ')  INITIATOR_NAME, "
strSelectStat1 +=" B.TARGSTARTDATE, B.DUE_DATE TARGCOMPDATE, "
strSelectStat1 +=" B.WO2, B.RISK_LEVEL, B.FINDING_STATEMENT, B.NOTES, "
strSelectStat1 +=" B.ASSESSMENT_TYPE," 
strSelectStat1 +=" B.TITLE, B.REVIEW_REPORT_TITLE, "
strSelectStat1 +=" B.STATUS, B.DATECOPIED, NVL(A.WONUM,'NULL') WONUM, NVL(A.ORGID,'LBNL') ORGID, NVL(A.SITEID,'FAC') SITEID, "
strSelectStat1 +=" NVL(A.WO_STATUS,'NULL') WO_STATUS, B.ROWID, "
strSelectStat1 +=" B.corrective_action, " 
strSelectStat1 +=" B.ISSUE_DESC, B.INITIATOR_EMPLOYEE_ID, "
strSelectStat1 +=" LTRIM(RTRIM(TO_CHAR(B.DATECOPIED, 'YYYYMMDD HH24:MI:SS'))) DATETIMECOPIED "
strSelectStat1 +=" FROM LBL_MAXIMO_CATS_INTFC B, LBL_MAXIMO_CATS_STATUS A"
strSelectStat1 +=" WHERE B.EXTERNALREFID=A.EXTERNALREFID(+) " 
#strSelectStat1 +=" AND  B.DATEIMPORTED IS NULL ";
strSelectStat1 +=" AND  B.ORGID="  +"'" + "LBNL"+"'";
strSelectStat1 +=" AND  B.SITEID=" +"'" + "FAC"+"'";
strSelectStat1 +=" and B.externalrefid in ('13331.8381','13333.8382') "      
strSelectStat1 +=" ORDER BY B.DATECOPIED, B.EXTERNALREFID";

myStatement1 = con.prepareStatement(strSelectStat1)              
Rs1 =myStatement1.executeQuery()
                 
#Browse through the record set
while Rs1.next():
       
         
    strRowid=Rs1.getString("ROWID")                                       
    strExternalRefId = Rs1.getString("EXTERNALREFID")
    strWoStatus=Rs1.getString("WO_STATUS")
    strStatus=Rs1.getString("STATUS")
    strWonum=Rs1.getString("WONUM")
    strOrgId=Rs1.getString("ORGID")
    strSiteId=Rs1.getString("SITEID")
    strDescription=Rs1.getString("DESCRIPTION")
    strDatetimecopied=Rs1.getString("DATETIMECOPIED")
   
     
    # Check same external ref id already exists in list. If it exists, then remove the older record from the list 
    strLogslength=len(strExternrefs)
    if (strLogslength >=0):
        for i in range(0,strLogslength):            
            if (strLogs[i]== strExternalRefId ):
                strExternrefs.remove(strExternalRefId) 
     
    if (isBlank(strStatus) == False):
       
        # Fill the information into array for email
        strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
        strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
        strTemp +=Rs1.getString("REPORTEDBY") +"|" + "ERROR" +"|" + "Invalid CATS STATUS. Can not insert/update work order."
        strLogs.append(strTemp)
        continue
       
    strFound="FALSE"          
    arrayStatus = strAllowedCATSstatus.split(",")
    for indStatus in arrayStatus:
        if (indStatus.upper()==strStatus.upper()):
            strFound="TRUE"
            break
            
    if (strFound=="FALSE"):
        # Fill the information into array for email
        strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
        strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
        strTemp +=Rs1.getString("REPORTEDBY") +"|" + "ERROR" +"|" + "Invalid CATS STATUS. Can not insert/update work order."
        strLogs.append(strTemp)
        continue
   
    # Check if LOCATION is valid
    if (isBlank(Rs1.getString("LOCATION")) == False):
        
        if (isBlank(getLocationDesc(Rs1.getString("LOCATION"))) == True):
            
            # Fill the information into array for email
            strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
            strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
            strTemp +=Rs1.getString("REPORTEDBY") +"|" + "ERROR" +"|" + "Invalid LOCATION. Can not insert/update work order."
            strLogs.append(strTemp)
            continue
        
    print "PRB glaccount: " +  Rs1.getString("glaccount")     
    # Check if GLACCOUNT is valid
    if (isBlank(Rs1.getString("GLACCOUNT")) == False):
                
        if (Rs1.getString("glaccount").upper() != "INSTITUTIONAL" ):
                                
            if (isBlank(getGLDesc(Rs1.getString("GLACCOUNT"))) == True):
                
                # Fill the information into array for email
                strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
                strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
                strTemp +=Rs1.getString("REPORTEDBY") +"|" + "ERROR" +"|" + "Invalid Project/activity id. Can not insert/update work order."
                strLogs.append(strTemp)
                continue
                    
    # Check division
    if (isBlank(Rs1.getString("WO2")) == False):
        
        if (isBlank(getDivision(Rs1.getString("WO2"))) == True):
            
            # Fill the information into array for email
            strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
            strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
            strTemp +=Rs1.getString("REPORTEDBY") +"|" + "ERROR" +"|" + "Invalid DIVISION. Can not insert/update work order."
            strLogs.append(strTemp)
            continue     
    
    # Check reportedby
    if (isBlank(Rs1.getString("REPORTEDBY")) == False):
        
        if (isBlank(getPersonname(Rs1.getString("REPORTEDBY"))) == True):
            
            # Fill the information into array for email
            strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
            strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
            strTemp +=Rs1.getString("REPORTEDBY") +"|" + "ERROR" +"|" + "Invalid REPORTEDBY. Can not insert/update work order."
            strLogs.append(strTemp)
            continue             
    
    # If the work order is approved, then location, description, glaccount
    #  must have valid value
    if ( isBlank(Rs1.getString("WO_STATUS")) == False):
        
        if (Rs1.getString("WO_STATUS").upper() !="WAPPR" and Rs1.getString("WO_STATUS").upper() !="RFI"):
                      
            if ((isBlank(Rs1.getString("LOCATION"))   == True) or
                (isBlank(Rs1.getString("GLACCOUNT"))  == True) or
                (isBlank(Rs1.getString("DESCRIPTION"))  == True) ):
                      
                    # Fill the information into array for email
                    strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
                    strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
                    strTemp +=Rs1.getString("REPORTEDBY") +"|" + "ERROR" +"|" + "Location/GLAccount/Description should not be null for the approved work order"
                    strLogs.append(strTemp)
                    continue
                             
        # If the CATS status is DELETED and if the work order status is NULL, thenskip the transaction           
         
        if ((strStatus.upper() == "DELETED") and (strWoStatus.upper() == "NULL")):
            
            # Fill the information into array for email
            strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
            strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
            strTemp +=Rs1.getString("REPORTEDBY") +"|" + "WARNING" +"|" + "CATS recorded deleted. Work order does not exist. Skipping.."
            strLogs.append(strTemp)
            continue
         
        # If CATS status is Open and wo_status is CAN,WCLOSE,CLOSE,COMP
        # then send an e-mail              
        if ((strStatus.upper() == "OPEN" or  strStatus.upper() == "OVERDUE")):
            if ((strWoStatus == "CAN ") or  (strWoStatus == "COMP") or (strWoStatus == "WCLOSE") or (strWoStatus=="CLOSE" )):
                 
                    # Fill the information into array for email
                    strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
                    strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
                    strTemp +=Rs1.getString("REPORTEDBY") +"|" + "ERROR" +"|" + "CATS record is Opened. Can not update canceled/completed/closed work order "                    
                    strLogs.append(strTemp)
                    continue
                
       
        
        strNewWorkorder="FALSE"        
                 
        #Start processing the transaction for insert/update into MAXIMO
        if (strWonum=="NULL"):
            # New work order     
            mboWorkorder=wosetRemote.add()    
            strWonum=mboWorkorder.getString("wonum")
            strNewWorkorder="TRUE"
            mboWorkorder.setValue("orgid", Rs1.getString("orgid")  ,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboWorkorder.setValue("siteid", Rs1.getString("siteid"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboWorkorder.setValue("assetnum", "",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
        else:
            # Existing work order
            wosetRemote = MXServer.getMXServer().getMboSet("WORKORDER", runAsUserInfo1)
            wosetRemote.setUserWhere("orgid='LBNL' and siteid='FAC' and wonum='" +strWonum +"'")
            mboWorkorder=wosetRemote.getMbo(0)
            
        # Cancel work order if cats status is deleted     
        if (Rs1.getString("STATUS").upper() == "DELETED" and strWoStatus !="CAN"):
            mboWorkorder.changeStatus("CAN", MXSession.getSession().getDate(),"CATS: " + strExternalRefId + " Deleted")
            # Fill the information into array for email
            strTemp  =strExternalRefId +"|" + strWonum  +"|" +  strDescription + "|" + strRowid + "|" 
            strTemp +=strDatetimecopied +"|" + strSiteId +"|" +  strOrgId +"|" 
            strTemp +=Rs1.getString("REPORTEDBY") +"|" + "SUCCESS" +"|" + "CATS record is deleted. Work order is canceled"
            strLogs.append(strTemp)
            continue
            
        #Set the remaining attribute of the WORKORDER related MBO
        mboWorkorder.setValue("description", Rs1.getString("description"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
        
        if ((Rs1.getString("WO_STATUS")  == "NULL") or (Rs1.getString("WO_STATUS")  =="WAPPR") or (Rs1.getString("WO_STATUS")  =="RFI")):
            mboWorkorder.setValue("worktype", "CM",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            if (Rs1.getString("glaccount").upper() != "INSTITUTIONAL" ):
                mboWorkorder.setValue("glaccount", Rs1.getString("glaccount"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            else:
                mboWorkorder.setValue("glaccount", "", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboWorkorder.setValue("location", Rs1.getString("location"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboWorkorder.setValue("reportedby",  Rs1.getString("REPORTEDBY"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboWorkorder.setValue("reportdate",  Rs1.getDate("REPORTDATE"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboWorkorder.setValue("wo2", Rs1.getString("WO2"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)    
            mboWorkorder.setValue("wo4", "CATS-" + strExternalRefId, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
       
        # Prepare long description
        strLdtext=""
        strLdtext = mboWorkorder.getString("description_longdescription")
        if (isBlank(strLdtext) == True):
      
           strLdtext += System.getProperty("line.separator")
           strLdtext +="---------------------------------------------------------------------------------"
           strLdtext += System.getProperty("line.separator")
             
        # Issue desc replaces finding statement
        if (isBlank(Rs1.getString("FINDING_STATEMENT")) == False):
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Issue Description :" + Rs1.getString("FINDING_STATEMENT")+ System.getProperty("line.separator")
            else:
                strLdtext +="Issue Description: "  + Rs1.getString("FINDING_STATEMENT") + System.getProperty("line.separator")                
     
        #Initiator replaces Finder
        if (isBlank(Rs1.getString("finder_employee_id")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Initiator :" + Rs1.getString("finder_employee_id")+ "-" + Rs1.getString("INITIATOR_NAME") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Initiator :" + Rs1.getString("finder_employee_id")+ "-" + Rs1.getString("INITIATOR_NAME") +  System.getProperty("line.separator")                
        
        #Approver
        if (isBlank(Rs1.getString("approver_employee_id")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Approver :" + Rs1.getString("approver_employee_id")+ "-" + Rs1.getString("APPROVER_NAME") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Approver :" + Rs1.getString("approver_employee_id")+ "-" + Rs1.getString("APPROVER_NAME") +  System.getProperty("line.separator")                        
    
        #Notes
        if (isBlank(Rs1.getString("notes")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Notes :" + Rs1.getString("notes") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Notes :" + Rs1.getString("notes") +  System.getProperty("line.separator")
                
        #Review report title
        if (isBlank(Rs1.getString("review_report_title")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Review report title :" + Rs1.getString("review_report_title") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Review report title:" + Rs1.getString("review_report_title") +  System.getProperty("line.separator")                           
        
        #ASSESSMENT_TYPE
        if (isBlank(Rs1.getString("ASSESSMENT_TYPE")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Assessment type:" + Rs1.getString("ASSESSMENT_TYPE") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Assessment type:" + Rs1.getString("ASSESSMENT_TYPE") +  System.getProperty("line.separator")                                   
                           
            
        #RISK_LEVEL
        if (isBlank(Rs1.getString("RISK_LEVEL")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Risk level:" + Rs1.getString("RISK_LEVEL") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Risk level:" + Rs1.getString("RISK_LEVEL") +  System.getProperty("line.separator")                                   
        
        # Title
        if (isBlank(Rs1.getString("title")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Title:" + Rs1.getString("title") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Title :" + Rs1.getString("title") +  System.getProperty("line.separator")                                   
                
        #Unparsed location
        if (isBlank(Rs1.getString("UNPARSEDLOCATION")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Unparsed location:" + Rs1.getString("UNPARSEDLOCATION") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Unparsed Location :" + Rs1.getString("UNPARSEDLOCATION") +  System.getProperty("line.separator")                                    
        
                 
        #Corrective_action
        if (isBlank(Rs1.getString("corrective_action")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Corrective Action:" + Rs1.getString("corrective_action") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Corrective Action :" + Rs1.getString("corrective_action") +  System.getProperty("line.separator")                                    
        
                 
        #Institutional
        if (isBlank(Rs1.getString("INSTITUTIONAL_FLAG")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Institutional: " + Rs1.getString("INSTITUTIONAL_FLAG") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Institutional: " + Rs1.getString("INSTITUTIONAL_FLAG") +  System.getProperty("line.separator")                                    
            
   
        #PROGRAM_PROJECT
        if (isBlank(Rs1.getString("PROGRAM_PROJECT")) == False): 
            if (isBlank(strLdtext) == True):                
                strLdtext  ="Program project: " + Rs1.getString("PROGRAM_PROJECT") +  System.getProperty("line.separator")              
            else:
                strLdtext +="Program project: " + Rs1.getString("PROGRAM_PROJECT") +  System.getProperty("line.separator")                                    
            
  
        if (isBlank(strLdtext)==False):
            mboWorkorder.setValue("description_longdescription", strLdtext, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION);
             
   
    
wosetRemote.save()
stmtUpdateStat1.close()
con.commit()

wosetRemote=None
srsetRemote=None  
woset2Remote=None
Rs1=None

 # At the end of the program release the db connection to the pool
mxServer.getDBManager().freeConnection(conKey) 
conn=None        