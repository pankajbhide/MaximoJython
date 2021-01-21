###################################################################################################
# Purpose: Script for inserting/modifying rows in lbl_facworkrequest and WORKORDER MBO based upon 
#          the JSON payload received
#
# Author : Pankaj Bhide
#
# Date    : December/January 2019,20
#
# Revision
# History :
#
###################################################################################################
from psdi.server import MXServer
from com.ibm.json.java import JSONObject
from org.python.core.util import StringUtil
from com.ibm.tivoli.maximo.oslc import OslcUtils
from psdi.util.logging import MXLoggerFactory
from java.sql import *
from psdi.mbo import MboConstants
from java.util import Date
from java.text import SimpleDateFormat

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def isBoolBlank(myObject):
    if (myObject is None):
        return True
    else:
        if (isBlank(str(myObject))==True):
            return True
        else:
            return False
    
def getPersondivision(strPersonid):
    strPersondivision=None
    personSet = MXServer.getMXServer().getMboSet("PERSON", runAsUserInfo1)
    personSet.setUserWhere("personid='" + strPersonid +"'")
    if (not personSet.isEmpty()):
                strPersondivision=personSet.getMbo(0).getString("lbl_org_level_1")
    personSet=None      
    return strPersondivision

def getClassification(strDescription):
    strClassification=None    
    strWhere="  1=1  "
    strWhere +=" and description='" + strDescription +"'"
    strWhere +=" and orgid='LBNL' "
    strWhere +=" and siteid='FAC'"
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    clsSet = MXServer.getMXServer().getMboSet("classstructure",runAsUserInfo1)
    clsSet.setUserWhere(strWhere)
    if (not clsSet.isEmpty()):
                strClassification=clsSet.getMbo(0).getString("classstructureid")
    clsSet=None      
    return strClassification
    
def getLblmaxvarvalue(strVarname):
    strLblvarvalue=None
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    lblmaxvarSet = MXServer.getMXServer().getMboSet("LBL_MAXVARS", runAsUserInfo1)
    lblmaxvarSet.setUserWhere("varname='" + strVarname +"' and orgid='LBNL' and siteid='FAC' ")
    if (not lblmaxvarSet.isEmpty()):
                strLblvarvalue=lblmaxvarSet.getMbo(0).getString("varvalue")
    lblmaxvarSet=None      
    return strLblvarvalue


def getAlnDomainDesc(strDomainid, strValue):
    strDomainDesc=None
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    domainSet = MXServer.getMXServer().getMboSet("ALNDOMAIN", runAsUserInfo1)
    domainSet.setUserWhere("domainid='" + strDomainid +"' and value='" + strValue +"'")
    if (not domainSet.isEmpty()):
                strDomainDesc=domainSet.getMbo(0).getString("description")
    domainSet=None      
    return strDomainDesc


def getPersonname(strPersonid):
    strPersonname=None
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    personSet = MXServer.getMXServer().getMboSet("PERSON", runAsUserInfo1)
    personSet.setUserWhere("personid='" + strPersonid +"'")
    if (not personSet.isEmpty()):
                strPersonname=personSet.getMbo(0).getString("displayname")
    personSet=None      
    return strPersonname

def getPersonlocation(strPersonid):
    strLocation=None
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    personSet = MXServer.getMXServer().getMboSet("PERSON", runAsUserInfo1)
    personSet.setUserWhere("personid='" + strPersonid +"'")
    if (not personSet.isEmpty()):
                strLocation=personSet.getMbo(0).getString("location")
    personSet=None      
    return strLocation

def getCommodityDesc(strCommodity):
    strCommodityDesc=None
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    commoditySet = MXServer.getMXServer().getMboSet("commodities", runAsUserInfo1)
    commoditySet.setUserWhere("commodity='" + strCommodity +"'")
    if (not commoditySet.isEmpty()):
                strCommodityDesc=commoditySet.getMbo(0).getString("description")
    commoditySet=None      
    return strCommodityDesc

def getPhone(strPersonid):
    strPhone=None
    if (isBlank(strPersonid)==True):
        return strPhone
   
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    phoneSet = MXServer.getMXServer().getMboSet("PHONE", runAsUserInfo1)
    phoneSet.setUserWhere("isprimary=1 and personid='" + strPersonid +"'")
    if (not phoneSet.isEmpty()):
                strPhone=phoneSet.getMbo(0).getString("phonenum")
    phoneSet=None      
    return strPhone

def getEmailaddress(strPersonid):
    strEmail=None
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    emailSet = MXServer.getMXServer().getMboSet("email", runAsUserInfo1)
    emailSet.setUserWhere("personid='" + strPersonid +"' and isprimary=1 ")
    if (not emailSet.isEmpty()):
                strEmail=emailSet.getMbo(0).getString("emailaddress")
    emailSet=None      
    return strEmail

def getLocationDesc(strLocation):
    strLocationDesc=None
    if (isBlank(strLocation)==True):
        return strLocationDesc
   
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    locationsSet = MXServer.getMXServer().getMboSet("LOCATIONS", runAsUserInfo1)
    locationsSet.setUserWhere("orgid='LBNL' and siteid='FAC' and location='" + strLocation +"' and disabled=0")
    if (not locationsSet.isEmpty()):
                strLocationDesc=locationsSet.getMbo(0).getString("description")
    locationsSet=None      
    return strLocationDesc

def getCOADesc(strGLAccount):
    strAccountname=None
    if (isBlank(strGLAccount)==True):
        return strAccountname
   
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    coaSet = MXServer.getMXServer().getMboSet("CHARTOFACCOUNTS", runAsUserInfo1)
    coaSet.setUserWhere("orgid='LBNL' and glaccount='" + strGLAccount +"' and active=1")
    if (not coaSet.isEmpty()):
                strAccountname=coaSet.getMbo(0).getString("accountname")
    coaSet=None      
    return strAccountname

def getDivisionDesc(strDivision):
    strDivisionDesc=None
    if (isBlank(strDivision)==True):
        return strDivisionDesc
   
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    craftSet = MXServer.getMXServer().getMboSet("CRAFT", runAsUserInfo1)
    craftSet.setUserWhere("orgid='LBNL' and lbl_org_level_1='" + strDivision +"' and lbl_org_level_2 is null and lbl_org_level_3 is null and lbl_org_level_4 is null ")
    if (not craftSet.isEmpty()):
                strDivisionDesc=craftSet.getMbo(0).getString("description")
    craftSet=None      
    return strDivisionDesc
strWonum=""
strSrnum=""


myLogger = MXLoggerFactory.getLogger("maximo.script.autoscript")

myLogger.debug("PRB starting")
####################################################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently commented
###################################################################





reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(requestBody))
row_count=0

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
lbl_facworkrequestRemote=MXServer.getMXServer().getMboSet("LBL_FACWORKREQUEST", runAsUserInfo1)
wosetRemote= MXServer.getMXServer().getMboSet("WORKORDER", runAsUserInfo1)
srsetRemote= MXServer.getMXServer().getMboSet("SR", runAsUserInfo1)

strClassificationid_NewKey=getClassification("New Key Request")
strClassificationid_TransferKey=getClassification("Transfer Key Request")
strClassificationid_LostKey=getClassification("Lost Key Request")


for i in range(len(reqData)):

    obj=reqData[i]
    row_count =row_count + 1
    ldtext1=" "
    ldtext_prepared=" "
    ldtext=" "
    ldtextdelimiter="\r\n\r\n"
    strLeadcraft=""
    strSupervisor=""
    strGlaccount=""
    strDescription=""
    strEscortReqd=""    
    strCondRel=""
    strCommentsCondRel=""
    strWorktype=""
    strLocation=""
    strWo5="3"
    strLbl_destgroup=""
    strCommgroup=""
    strCommodity=""
    strPickupfrom=""
    strDeliverto=""
    strLead=""
    strDocumenttype=""
    strDocumentnumber=""
    strNewStatus=""
    strNewStatusMemo=""
    
    obj["activity_id"]="" if ( not "activity_id" in obj)  else obj["activity_id"]
    obj["anotherwonum"]="" if ( not "anotherwonum" in obj)  else obj["anotherwonum"]
    obj["building"]="" if ( not "building" in obj)  else obj["building"]
    obj["changeby"]="" if ( not "changeby" in obj)  else obj["changeby"]
    obj["changedate"]="" if ( not "changedate" in obj)  else obj["changedate"]
    obj["datetafsent"]="" if ( not "datetafsent" in obj)  else obj["datetafsent"]
    obj["deliverybuilding"]="" if ( not "deliverybuilding" in obj)  else obj["deliverybuilding"]
    obj["deliveryroom"]="" if ( not "deliveryroom" in obj)  else obj["deliveryroom"]
    obj["description"]="" if ( not "description" in obj)  else obj["description"]
    obj["documentnumber"]="" if ( not "documentnumber" in obj)  else obj["documentnumber"]
    obj["documenttype"]="" if ( not "documenttype" in obj)  else obj["documenttype"]
    obj["equipid"]="" if ( not "equipid" in obj)  else obj["equipid"]
    obj["esthrs"]="" if ( not "esthrs" in obj)  else obj["esthrs"]
    obj["followupexplain"]="" if ( not "followupexplain" in obj)  else obj["followupexplain"]
    obj["follupstpwkwonum"]="" if ( not "follupstpwkwonum" in obj)  else obj["follupstpwkwonum"]
    obj["fromworkcompdate"]="" if ( not "fromworkcompdate" in obj)  else obj["fromworkcompdate"]
    obj["hasld"]="" if ( not "hasld" in obj)  else obj["hasld"]
    obj["hazardsdetails"]="" if ( not "hazardsdetails" in obj)  else obj["hazardsdetails"]
    obj["isanotherwo"]="" if ( not "isanotherwo" in obj)  else obj["isanotherwo"]
    obj["isbldgrepair"]="" if ( not "isbldgrepair" in obj)  else obj["isbldgrepair"]
    obj["iscustodialwork"]="" if ( not "iscustodialwork" in obj)  else obj["iscustodialwork"]
    obj["isescortrequired"]="" if ( not "isescortrequired" in obj)  else obj["isescortrequired"]
    obj["isestreq"]="" if ( not "isestreq" in obj)  else obj["isestreq"]
    obj["isfacpersonnel"]="" if ( not "isfacpersonnel" in obj)  else obj["isfacpersonnel"]
    obj["isfacpersonnelwo"]="" if ( not "isfacpersonnelwo" in obj)  else obj["isfacpersonnelwo"]
    obj["isfirstavaildate"]="" if ( not "isfirstavaildate" in obj)  else obj["isfirstavaildate"]
    obj["isfollupstpwk"]="" if ( not "isfollupstpwk" in obj)  else obj["isfollupstpwk"]
    obj["ishazards"]="" if ( not "ishazards" in obj)  else obj["ishazards"]
    obj["ismulticraft"]="" if ( not "ismulticraft" in obj)  else obj["ismulticraft"]
    obj["isparentwo"]="" if ( not "isparentwo" in obj)  else obj["isparentwo"]
    obj["receiver"]="" if ( not "receiver" in obj)  else obj["receiver"]
    obj["isreceivermatrix"]="" if ( not "isreceivermatrix" in obj)  else obj["isreceivermatrix"]
    obj["isrecycle"]="" if ( not "isrecycle" in obj)  else obj["isrecycle"]
    obj["isrush"]="" if ( not "isrush" in obj)  else obj["isrush"]
    obj["issafetyissue"]="" if ( not "issafetyissue" in obj)  else obj["issafetyissue"]
    obj["issalvage"]="" if ( not "issalvage" in obj)  else obj["issalvage"]
    obj["isschedconstraints"]="" if ( not "isschedconstraints" in obj)  else obj["isschedconstraints"]
    obj["istranshazards"]="" if ( not "istranshazards" in obj)  else obj["istranshazards"]
    obj["iswarrantyissue"]="" if ( not "iswarrantyissue" in obj)  else obj["iswarrantyissue"]
    obj["itemweight"]="" if ( not "itemweight" in obj)  else obj["itemweight"]
    obj["keyauthorizer"]="" if ( not "keyauthorizer" in obj)  else obj["keyauthorizer"]
    obj["keydateneeded"]="" if ( not "keydateneeded" in obj)  else obj["keydateneeded"]
    obj["keyreceiver"]="" if ( not "keyreceiver" in obj)  else obj["keyreceiver"]
    obj["keysequence"]="" if ( not "keysequence" in obj)  else obj["keysequence"]
    obj["knumber"]="" if ( not "knumber" in obj)  else obj["knumber"]
    obj["lbl_facworkrequstid"]="" if ( not "lbl_facworkrequstid" in obj)  else obj["lbl_facworkrequstid"]
    obj["location"]="" if ( not "location" in obj)  else obj["location"]
    obj["locationnotes"]="" if ( not "locationnotes" in obj)  else obj["locationnotes"]
    obj["mailstop"]="" if ( not "mailstop" in obj)  else obj["mailstop"]
    obj["matrixedtodivision"]="" if ( not "matrixedtodivision" in obj)  else obj["matrixedtodivision"]
    obj["needestimatedate"]="" if ( not "needestimatedate" in obj)  else obj["needestimatedate"]
    obj["noofitems"]="" if ( not "noofitems" in obj)  else obj["noofitems"]
    obj["orgid"]="" if ( not "orgid" in obj)  else obj["orgid"]
    obj["othstakeholder"]="" if ( not "othstakeholder" in obj)  else obj["othstakeholder"]
    obj["othstakemobile"]="" if ( not "othstakemobile" in obj)  else obj["othstakemobile"]
    obj["othstakephone"]="" if ( not "othstakephone" in obj)  else obj["othstakephone"]
    obj["parentwonum"]="" if ( not "parentwonum" in obj)  else obj["parentwonum"]
    obj["pickupbuilding"]="" if ( not "pickupbuilding" in obj)  else obj["pickupbuilding"]
    obj["pickuproom"]="" if ( not "pickuproom" in obj)  else obj["pickuproom"]
    obj["pocmobile"]="" if ( not "pocmobile" in obj)  else obj["pocmobile"]
    obj["pocphone"]="" if ( not "pocphone" in obj)  else obj["pocphone"]
    obj["pointofcontact"]="" if ( not "pointofcontact" in obj)  else obj["pointofcontact"]
    obj["prevkeyowner"]="" if ( not "prevkeyowner" in obj)  else obj["prevkeyowner"]
    obj["project_id"]="" if ( not "project_id" in obj)  else obj["project_id"]
    obj["reportdate"]="" if ( not "reportdate" in obj)  else obj["reportdate"]
    obj["requestnumber"]="" if ( not "requestnumber" in obj)  else obj["requestnumber"]
    obj["requestor"]="" if ( not "requestor" in obj)  else obj["requestor"]
    obj["requestormobile"]="" if ( not "requestormobile" in obj)  else obj["requestormobile"]
    obj["requestorphone"]="" if ( not "requestorphone" in obj)  else obj["requestorphone"]
    obj["requesttype"]="" if ( not "requesttype" in obj)  else obj["requesttype"]
    obj["room"]="" if ( not "room" in obj)  else obj["room"]
    obj["schedconstraints"]="" if ( not "schedconstraints" in obj)  else obj["schedconstraints"]
    obj["siteid"]="" if ( not "siteid" in obj)  else obj["siteid"]
    obj["toworkcompdate"]="" if ( not "toworkcompdate" in obj)  else obj["toworkcompdate"]
    obj["typeofitems"]="" if ( not "typeofitems" in obj)  else obj["typeofitems"]
    obj["warrantydetails"]="" if ( not "warrantydetails" in obj)  else obj["warrantydetails"]
    obj["workpurpose"]="" if ( not "workpurpose" in obj)  else obj["workpurpose"]
    
    obj["acccntrlarea"]="" if ( not "acccntrlarea" in obj)  else obj["acccntrlarea"]
    obj["acccntrlareacont"]="" if ( not "acccntrlareacont" in obj)  else obj["acccntrlareacont"]
    obj["sf_issue_comments"]="" if ( not "sf_issue_comments" in obj)  else obj["sf_issue_comments"]
    
    obj["iscmpm"]="" if ( not "iscmpm" in obj)  else obj["iscmpm"]
    obj["requiresoutage"]="" if ( not "requiresoutage" in obj)  else obj["requiresoutage"]
    
    obj["newstatus"]="" if (not "newstatus" in obj)  else obj["newstatus"]
    obj["newstatusmemo"]="" if (not "newstatusmemo" in obj)  else obj["newstatusmemo"]
    obj["description_longdescription"]="" if (not "description_longdescription" in obj)  else obj["description_longdescription"]

 
                            
    if  (obj is not None):
        
                   
        if (isBlank(obj["project_id"])==False and isBlank(obj["activity_id"])==False):
            strGlaccount=obj["project_id"] + "." + obj["activity_id"]
            
            
        if (isBlank(obj["documenttype"])==False and isBlank(obj["documentnumber"])==False):
            
            strDocumenttype=obj["documenttype"]
            strDocumentnumber=obj["documentnumber"]
            
            lbl_facworkrequestRemote.setUserWhere("documenttype='" + strDocumenttype + "' and documentnumber='" + strDocumentnumber +"'")
    
            if (not lbl_facworkrequestRemote.isEmpty()):
                facworkrequestSet=lbl_facworkrequestRemote.getMbo(0)
        else:
            facworkrequestSet=lbl_facworkrequestRemote.add()
            
        strNewStatus=obj["newstatus"]
        strNewStatusMemo=obj["newstatusmemo"]
        
        # Status change
        if (isBlank(strNewStatus) == False and isBlank(strDocumenttype)==False and  isBlank(strDocumentnumber)==False):
            if (strDocumenttype=="WORKORDER"):
                wosetRemote.setUserWhere("wonum='" +  strDocumentnumber +"'")
        
                if (not wosetRemote.isEmpty()):
                    mboWorkorder=wosetRemote.getMbo(0)
                    strWonum=mboWorkorder.getString("wonum")
                    mboWorkorder.changeStatus(strNewStatus,MXServer.getMXServer().getDate(), strNewStatusMemo, MboConstants.NOACCESSCHECK)
                    wosetRemote.save()
                    
            if (strDocumenttype=="SR"):
                srsetRemote.setUserWhere("ticketid='" +  strDocumentnumber +"'")
        
                if (not srsetRemote.isEmpty()):
                    mboSR=srsetRemote.getMbo(0)
                    mboSR.changeStatus(strNewStatus,MXServer.getMXServer().getDate(), strNewStatusMemo, MboConstants.NOACCESSCHECK)
                    srsetRemote.save()             
        
        else:  # No status change
              
                 
                #facworkrequestSet.setValue("lbl_facworkrequstid" ,obj["lbl_facworkrequstid"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            #facworkrequestSet.setValue("hasld" ,obj["hasld"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            if (isBlank(obj["orgid"])== False):
                facworkrequestSet.setValue("orgid" ,obj["orgid"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        
            if (isBlank(obj["siteid"])== False):
                facworkrequestSet.setValue("siteid" ,obj["siteid"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            if (isBlank(obj["requesttype"])== False):
                facworkrequestSet.setValue("requesttype" ,obj["requesttype"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            if (isBlank(obj["requestnumber"])== False):
                facworkrequestSet.setValue("requestnumber" ,obj["requestnumber"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            if (isBlank(obj["requestor"])== False):
                facworkrequestSet.setValue("requestor" ,obj["requestor"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strWo1=obj["requestor"]
                
            strPhone=""
            if (isBlank(obj["requestorphone"])== False):
                facworkrequestSet.setValue("requestorphone" ,obj["requestorphone"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strPhone=obj["requestorphone"]
                
            if (isBlank(obj["requestormobile"])== False):
                facworkrequestSet.setValue("requestormobile" ,obj["requestormobile"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("requestormobile" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            
            if (isBlank(obj["pointofcontact"])== False):
                facworkrequestSet.setValue("pointofcontact" ,obj["pointofcontact"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strWo1=obj["pointofcontact"]
            else:
                facworkrequestSet.setValueNull("pointofcontact" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            if (isBlank(obj["pocphone"])== False):
                facworkrequestSet.setValue("pocphone" ,obj["pocphone"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("pocphone" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                   
            if (isBlank(obj["othstakeholder"])== False):
                facworkrequestSet.setValue("othstakeholder" ,obj["othstakeholder"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("othstakeholder" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
            if (isBlank(obj["othstakephone"])== False):
                facworkrequestSet.setValue("othstakephone" ,obj["othstakephone"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("othstakephone" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             
            if (isBlank(obj["othstakemobile"])== False):
                facworkrequestSet.setValue("othstakemobile" ,obj["othstakemobile"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("othstakemobile" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                  
                
            if (isBlank(obj["schedconstraints"])== False):
                facworkrequestSet.setValue("schedconstraints" ,obj["schedconstraints"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("schedconstraints" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
                
            if (isBlank(obj["building"])== False):
                facworkrequestSet.setValue("building" ,obj["building"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("building" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            if (isBlank(obj["room"])== False):
                facworkrequestSet.setValue("room" ,obj["room"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("room" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
           
            if (isBlank(obj["locationnotes"])== False):
                facworkrequestSet.setValue("locationnotes" ,obj["locationnotes"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("locationnotes" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
          
            if (isBlank(obj["needestimatedate"])== False):
                facworkrequestSet.setValue("needestimatedate" ,obj["needestimatedate"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("needestimatedate" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            strTargStart=""    
            if (isBlank(obj["fromworkcompdate"])== False):
                facworkrequestSet.setValue("fromworkcompdate" ,obj["fromworkcompdate"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strTargStart=obj["fromworkcompdate"]
            else:
                facworkrequestSet.setValueNull("fromworkcompdate" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
            strTargComp=""    
            if (isBlank(obj["toworkcompdate"])== False):
                facworkrequestSet.setValue("toworkcompdate" ,obj["toworkcompdate"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strTargComp=obj["toworkcompdate"]
            else:
                facworkrequestSet.setValueNull("toworkcompdate" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
            if (isBlank(obj["project_id"])== False):
                facworkrequestSet.setValue("project_id" ,obj["project_id"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("project_id" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        
            if (isBlank(obj["activity_id"])== False):
                facworkrequestSet.setValue("activity_id" ,obj["activity_id"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("activity_id" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            #if (isBlank(obj["changedate"])== False):
            facworkrequestSet.setValue("changedate" ,MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
            facworkrequestSet.setValue("changeby" ,"IT-BS-MXINTADM", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            if (isBlank(obj["keyreceiver"])== False):
                facworkrequestSet.setValue("keyreceiver" ,obj["keyreceiver"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            if (isBlank(str(obj["isreceivermatrix"]))== False):
                facworkrequestSet.setValue("isreceivermatrix" ,obj["isreceivermatrix"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            if (isBlank(obj["keysequence"])== False):
                facworkrequestSet.setValue("keysequence" ,obj["keysequence"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            if (isBlank(obj["knumber"])== False):
                facworkrequestSet.setValue("knumber" ,obj["knumber"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("knumber",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                          
            if (isBlank(obj["matrixedtodivision"])== False):
                facworkrequestSet.setValue("matrixedtodivision" ,obj["matrixedtodivision"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                   
            if (isBlank(obj["keydateneeded"])== False):
                facworkrequestSet.setValue("keydateneeded" ,obj["keydateneeded"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            if (isBlank(obj["keyauthorizer"])== False):
                facworkrequestSet.setValue("keyauthorizer" ,obj["keyauthorizer"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            if (isBlank(str(obj["isrush"]))== False):
                facworkrequestSet.setValue("isrush" ,obj["isrush"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            if (isBlank(obj["prevkeyowner"])== False):
                facworkrequestSet.setValue("prevkeyowner" ,obj["prevkeyowner"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            if (isBlank(obj["mailstop"])== False):
                facworkrequestSet.setValue("mailstop" ,obj["mailstop"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("mailstop" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            if (isBoolBlank(obj["isfirstavaildate"])== False):
                facworkrequestSet.setValue("isfirstavaildate" ,obj["isfirstavaildate"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isfirstavaildate" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                    
            if (isBoolBlank(obj["isschedconstraints"])== False):
                facworkrequestSet.setValue("isschedconstraints" ,obj["isschedconstraints"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isschedconstraints" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            if (isBoolBlank(obj["iscustodialwork"])== False):
                facworkrequestSet.setValue("iscustodialwork" ,obj["iscustodialwork"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("iscustodialwork" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
            if (isBoolBlank(obj["isbldgrepair"])== False):
                facworkrequestSet.setValue("isbldgrepair" ,obj["isbldgrepair"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isbldgrepair" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            if (isBoolBlank(obj["isanotherwo"])== False):
                facworkrequestSet.setValue("isanotherwo" ,obj["isanotherwo"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isanotherwo" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
 
                
            if (isBlank(obj["anotherwonum"])== False):
                facworkrequestSet.setValue("anotherwonum" ,obj["anotherwonum"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("anotherwonum" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            if (isBlank(obj["equipid"])== False):
                facworkrequestSet.setValue("equipid" ,obj["equipid"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("equipid" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)                
               
                
            if (isBoolBlank(obj["iswarrantyissue"])== False):
                facworkrequestSet.setValue("iswarrantyissue" ,obj["iswarrantyissue"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("iswarrantyissue" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)                
 
            if (isBlank(obj["warrantydetails"])== False):
                facworkrequestSet.setValue("warrantydetails" ,obj["warrantydetails"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("warrantydetails" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)                

            if (isBoolBlank(obj["isestreq"])== False):
                facworkrequestSet.setValue("isestreq" ,obj["isestreq"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isestreq" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            if (isBoolBlank(obj["issafetyissue"])== False):
                facworkrequestSet.setValue("issafetyissue" ,obj["issafetyissue"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("issafetyissue" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                          
            if (isBoolBlank(obj["ishazards"])== False):
                facworkrequestSet.setValue("ishazards" ,obj["ishazards"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("ishazards" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            if (isBlank(obj["hazardsdetails"])== False):
                facworkrequestSet.setValue("hazardsdetails" ,obj["hazardsdetails"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("hazardsdetails" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            if (isBoolBlank(obj["isfacpersonnel"])== False):
                facworkrequestSet.setValue("isfacpersonnel" ,obj["isfacpersonnel"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isfacpersonnel" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    
            if (isBoolBlank(obj["isfollupstpwk"])== False):
                facworkrequestSet.setValue("isfollupstpwk" ,obj["isfollupstpwk"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isfollupstpwk" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    
            if (isBlank(obj["follupstpwkwonum"])== False):
                facworkrequestSet.setValue("follupstpwkwonum" ,obj["follupstpwkwonum"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("follupstpwkwonum" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                   
                
            if (isBlank(obj["followupexplain"])== False):
                facworkrequestSet.setValue("followupexplain" ,obj["followupexplain"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("followupexplain" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                   
                
            if (isBoolBlank(obj["isfacpersonnelwo"])== False):
                facworkrequestSet.setValue("isfacpersonnelwo" ,obj["isfacpersonnelwo"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isfacpersonnelwo" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
                 
            if (isBoolBlank(obj["iscmpm"])== False):
                facworkrequestSet.setValue("iscmpm" ,obj["iscmpm"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("iscmpm" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            if (isBoolBlank(obj["requiresoutage"])== False):
                facworkrequestSet.setValue("requiresoutage" ,obj["requiresoutage"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("requiresoutage" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
        
          
            if (isBoolBlank(obj["esthrs"])== False):
                facworkrequestSet.setValue("esthrs" ,obj["esthrs"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("esthrs" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
              
                           
            if (isBoolBlank(obj["isparentwo"])== False):
                facworkrequestSet.setValue("isparentwo" ,obj["isparentwo"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isparentwo" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            if (isBlank(obj["parentwonum"])== False):
                facworkrequestSet.setValue("parentwonum" ,obj["parentwonum"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("parentwonum" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
   
            if (isBoolBlank(obj["ismulticraft"])== False):
                facworkrequestSet.setValue("ismulticraft" ,obj["ismulticraft"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("ismulticraft" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                    
            if (isBoolBlank(obj["isescortrequired"])== False):
                facworkrequestSet.setValue("isescortrequired" ,obj["isescortrequired"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isescortrequired" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    
            
            if (isBoolBlank(obj["acccntrlarea"])== False):
                facworkrequestSet.setValue("acccntrlarea" ,obj["acccntrlarea"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("acccntrlarea" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            
                
            if (isBlank(obj["noofitems"])== False):
                facworkrequestSet.setValue("noofitems" ,obj["noofitems"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("noofitems" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
            if (isBlank(obj["acccntrlareacont"])== False):
                facworkrequestSet.setValue("acccntrlareacont" ,obj["acccntrlareacont"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("acccntrlareacont" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            if (isBlank(obj["sf_issue_comments"])== False):
                facworkrequestSet.setValue("sf_issue_comments" ,obj["sf_issue_comments"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("sf_issue_comments" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            ################################################################################################################################## 
               
            if (isBlank(obj["noofitems"])== False):
                facworkrequestSet.setValue("noofitems" ,obj["noofitems"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("noofitems" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            if (isBlank(obj["typeofitems"])== False):
                facworkrequestSet.setValue("typeofitems" ,obj["typeofitems"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("typeofitems" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    
                
            if (isBlank(obj["itemweight"])== False):
                facworkrequestSet.setValue("itemweight" ,obj["itemweight"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("itemweight" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
      
                
            if (isBlank(obj["pickupbuilding"])== False and obj["pickupbuilding"] !="--Select--"):
                facworkrequestSet.setValue("pickupbuilding" ,obj["pickupbuilding"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strPickupfrom=obj["pickupbuilding"] 
            else:
                facworkrequestSet.setValueNull("pickupbuilding" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
                
            
                
            if (isBlank(obj["pickuproom"])== False and obj["pickuproom"] != "--Select--"):
                facworkrequestSet.setValue("pickuproom" ,obj["pickuproom"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strPickupfrom=obj["pickupbuilding"] +"-" + obj["pickuproom"]
            else:
                facworkrequestSet.setValueNull("pickuproom" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
                           
            if (isBlank(obj["deliverybuilding"])== False and obj["deliverybuilding"] !="--Select--"):
                facworkrequestSet.setValue("deliverybuilding" ,obj["deliverybuilding"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strDeliverto=obj["deliverybuilding"]
            else:
                facworkrequestSet.setValueNull("deliverybuilding" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
            if (isBlank(obj["deliveryroom"])== False and obj["deliveryroom"] !="--Select--"):
                facworkrequestSet.setValue("deliveryroom" ,obj["deliveryroom"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strDeliverto=obj["deliverybuilding"] +"-" + obj["deliveryroom"]
            else:
                facworkrequestSet.setValueNull("deliveryroom" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                
            if (isBoolBlank(obj["isrecycle"])== False):
                facworkrequestSet.setValue("isrecycle" ,obj["isrecycle"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("isrecycle" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    
                
            if (isBoolBlank(str(obj["issalvage"]))== False):
                facworkrequestSet.setValue("issalvage" ,obj["issalvage"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("issalvage" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    
                        
            if (isBoolBlank(obj["istranshazards"])== False):
                facworkrequestSet.setValue("istranshazards" ,obj["istranshazards"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValue("istranshazards" ,0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    
                 
            #acworkrequestSet.setValue("documenttype" ,obj["documenttype"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
           
            #facworkrequestSet.setValue("documentnumber" ,obj["documentnumber"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            if (isBlank(obj["pocmobile"])== False):
                facworkrequestSet.setValue("pocmobile" ,obj["pocmobile"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("pocmobile" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            if (isBlank(obj["workpurpose"])== False):
                facworkrequestSet.setValue("workpurpose" ,obj["workpurpose"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                strCommodity=obj["workpurpose"]
                
                
            if (isBlank(obj["description_longdescription"])== False):
                facworkrequestSet.setValue("description_longdescription" ,obj["description_longdescription"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                facworkrequestSet.setValueNull("description_longdescription" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    
                
            strDescription=obj["description"]
            
            if (isBlank(obj["reportdate"])== False):
                facworkrequestSet.setValue("reportdate" ,obj["reportdate"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            #else:
            #    facworkrequestSet.setValue("reportdate",  MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                
            ########################################    
            # Start creating work order or SR
            ########################################
            
            if (obj["requesttype"]=="GENERAL"):
                
                
                if (isBlank(obj["building"])==False and isBlank(obj["room"])==False):
                    strLocation=obj["building"] +"-" + obj["room"]
                if (isBlank(obj["building"])==False and isBlank(obj["room"])==True):
                    strLocation=obj["building"]
                                                  
                if (isBlank(obj["workpurpose"])== False):
                    if (obj["workpurpose"]=="19"): # Pest control
                        strSupervisor=getLblmaxvarvalue("WOPESTREQ_SUPERVISOR")
                        strWorktype=getLblmaxvarvalue("WOPESTREQ_WORKTYPE")
                    if (obj["workpurpose"]=="03"): # Radio shop
                        strSupervisor=getLblmaxvarvalue("RADIOSHOP_SUPERVISOR")
                    if (obj["workpurpose"]=="09"): # Lock shop
                        strSupervisor=getLblmaxvarvalue("LOCKSHOP_SUPERVISOR")
                            
                strCommgroup="FAOPS"
                myLogger.debug("PRB setting the value to FAOPS")
                
                # Prepare long description
                if (isBlank(obj["description_longdescription"])==False):    
                    ldtext_prepared +="Detailed description: " + obj["description_longdescription"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Detailed description: Not Specified" +ldtextdelimiter
                    
                if (isBlank(obj["requestormobile"])== False):
                    ldtext_prepared +="Requestor Mobile: " + obj["requestormobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Requestor Mobile: Not specified." +ldtextdelimiter
                
                if (isBlank(obj["pointofcontact"])== False):
                    ldtext_prepared +="Point of contact: " + obj["pointofcontact"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact: Not specified." +ldtextdelimiter
               
                if (isBlank(obj["pocphone"])== False):
                    ldtext_prepared +="Point of contact phone: " + obj["pocphone"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact phone: Not specified." +ldtextdelimiter
                    
                if (isBlank(obj["pocmobile"])== False):
                    ldtext_prepared +="Point of contact mobile: " + obj["pocmobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact mobile: Not specified." +ldtextdelimiter
                
                if (isBlank(obj["locationnotes"])==False):    
                    ldtext_prepared +="Location Notes: " + obj["locationnotes"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Location Notes: Not specified." +ldtextdelimiter
                    
                if (str(obj["isfirstavaildate"])=="1" or str(obj["isfirstavaildate"])=="True" ):
                    ldtext_prepared +="First Available date: " + "Yes "+ldtextdelimiter
                else:
                    ldtext_prepared +="First Available date: " + "No" +ldtextdelimiter
                           
                if (isBlank(obj["fromworkcompdate"])== False):
                    ldtext_prepared +="Target Start Date: " + obj["fromworkcompdate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Target Start Date: Not specified"  +ldtextdelimiter
                    
                if (isBlank(obj["toworkcompdate"])== False):    
                    ldtext_prepared +="Target Completion Date: " + obj["toworkcompdate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Target Completion Date: Not specified"  +ldtextdelimiter
                    
                if (isBlank(obj["schedconstraints"])== False):    
                    ldtext_prepared +="Scheduling details: " + obj["schedconstraints"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Scheduling details: Not specified"  +ldtextdelimiter
                    
                if (str(obj["isbldgrepair"])=="1" or str(obj["isbldgrepair"])=="True" ):
                    ldtext_prepared +="Building repair: " + "Yes "+ldtextdelimiter
                else:  
                    ldtext_prepared +="Building repair:  " + "No " +ldtextdelimiter
                
                if (isBlank(obj["anotherwonum"])== False):        
                    ldtext_prepared +="Another work order number:  " + obj["anotherwonum"] +ldtextdelimiter
                else:             
                    ldtext_prepared +="Another work order number: Not specified"  +ldtextdelimiter
                
                if (isBlank(obj["equipid"])== False):        
                    ldtext_prepared +="Equipment Id:  " + obj["equipid"] +ldtextdelimiter
                else:             
                    ldtext_prepared +="Equipment Id: Not specified"  +ldtextdelimiter
                    
                if (isBlank(obj["warrantydetails"])== False):        
                    ldtext_prepared +="Warranty issue details:  " + obj["warrantydetails"] +ldtextdelimiter
                else:             
                    ldtext_prepared +="Warranty issue details: Not specified"  +ldtextdelimiter
                
                if (isBlank(obj["follupstpwkwonum"])== False):        
                    ldtext_prepared +="Follow up work order or response to STOP work order:  " + obj["follupstpwkwonum"] +ldtextdelimiter
                else:             
                    ldtext_prepared +="Follow up work order or response to STOP work order: Not specified"  +ldtextdelimiter
                
                if (isBlank(obj["followupexplain"])== False):        
                    ldtext_prepared +="Explanation of follow up work order or response to STOP work order:  " + obj["followupexplain"] +ldtextdelimiter
                else:             
                    ldtext_prepared +="Explanation of follow up work order or response to STOP work order: Not specified"  +ldtextdelimiter
                    
                if (str(obj["issafetyissue"])=="1" or str(obj["issafetyissue"])=="True" ):
                    ldtext_prepared +="Safety Issue: " + "Yes "+ldtextdelimiter
                else:  
                    ldtext_prepared +="Safety Issue:  " + "No " +ldtextdelimiter
                    
                if (str(obj["isescortrequired"])=="1" or str(obj["isescortrequired"])=="True" ):
                    ldtext_prepared +="Escort required: " + "Yes "+ldtextdelimiter
                else:  
                    ldtext_prepared +="Escort required:  " + "No " +ldtextdelimiter    
        
                    
                if (str(obj["ishazards"])=="1" or str(obj["ishazards"])=="True" ): 
                    ldtext_prepared +="Hazards to the Facilities staff: Yes" +ldtextdelimiter
                else:
                    ldtext_prepared +="Hazards to Facilities staff: No" +ldtextdelimiter
                     
                if (isBlank(obj["hazardsdetails"])== False):        
                    ldtext_prepared +="Hazards details:  " + obj["hazardsdetails"] +ldtextdelimiter
                else:             
                    ldtext_prepared +="Hazards details : Not specified"  +ldtextdelimiter
    
                if (isBlank(obj["esthrs"])== False):        
                    ldtext_prepared +="Estimated hours:  " + obj["esthrs"] +ldtextdelimiter
                else:             
                    ldtext_prepared +="Estimated hours : Not specified"  +ldtextdelimiter
                  
                if (isBlank(obj["parentwonum"])== False):
                    ldtext_prepared +="Parent work order:  " + obj["parentwonum"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Parent work order: Not specified" +ldtextdelimiter
                    
                
                
                if (str(obj["acccntrlarea"])=="1" or str(obj["acccntrlarea"])=="True" ): 
                    ldtext_prepared +="Access to the controlled area: Yes" +ldtextdelimiter
                else:
                    ldtext_prepared +="Access to the controlled area: No" +ldtextdelimiter
                     
                if (isBlank(obj["acccntrlareacont"])== False):
                    ldtext_prepared +="Contact for access to the controller area:  " + obj["acccntrlareacont"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Contact for access to the controller area: Not specified" +ldtextdelimiter
                
                if (isBlank(obj["sf_issue_comments"])== False):
                    ldtext_prepared +="Safety issue comments:  " + obj["sf_issue_comments"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Safety issue comments: Not specified" +ldtextdelimiter
                
         
                if (str(obj["iscmpm"])=="1" or str(obj["iscmpm"])=="True" ): 
                    ldtext_prepared +="Are you Construction/Project Manager:  " + "Yes" +ldtextdelimiter
                else:
                    ldtext_prepared +="Are you Construction/Project Manager:  " + "No" +ldtextdelimiter
                
                if (str(obj["requiresoutage"])=="1" or str(obj["requiresoutage"])=="True" ): 
                    ldtext_prepared +="Requires Outage:  " + "Yes" +ldtextdelimiter
                else:
                    ldtext_prepared +="Requires Outage:  " + "No" +ldtextdelimiter
                
                if (str(obj["iscmpm"])=="1" or str(obj["iscmpm"])=="True" ):
                    strWorktype="PROJ"
              
                         
            ###################
            #   TRANSPORTATION
            ###################        
                    
            if (obj["requesttype"]=="TRANSPORTATION"):     
                
                if (isBlank(obj["description_longdescription"])==False):    
                    ldtext_prepared +="Detailed description: " + obj["description_longdescription"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Detailed description: Not Specified" +ldtextdelimiter
                    
                    
                if (isBlank(obj["requestormobile"])== False):
                    ldtext_prepared +="Requestor Mobile: " + obj["requestormobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Requestor Mobile: Not specified." +ldtextdelimiter
                
                if (isBlank(obj["pointofcontact"])== False):
                    ldtext_prepared +="Point of contact: " + obj["pointofcontact"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact: Not specified." +ldtextdelimiter
               
                if (isBlank(obj["pocphone"])== False):
                    ldtext_prepared +="Point of contact phone: " + obj["pocphone"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact phone: Not specified." +ldtextdelimiter    
                
                if (isBlank(obj["pocmobile"])== False):
                    ldtext_prepared +="Point of contact mobile: " + obj["pocmobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact mobile: Not specified." +ldtextdelimiter    
                    
                if (isBlank(obj["itemweight"])==False):
                    
                    if (obj["itemweight"]=="> 250 LBS"):
                        strLeadcraft=getLblmaxvarvalue("WOREQ_TRANSP_>250_LEADCRAFT")
                        strSupervisor=getLblmaxvarvalue("WOREQ_TRANSP_>250_SUPERVISOR")
                    else:
                        strLeadcraft=getLblmaxvarvalue("WOREQ_TRANSP_<250_LEADCRAFT")
                        strSupervisor=getLblmaxvarvalue("WOREQ_TRANSP_<250_SUPERVISOR")
                        
                if (isBlank(obj["noofitems"])== False and isBlank(strPickupfrom)==False and  isBlank(strDeliverto)==False):
                    strDescription="Move " + obj["noofitems"].strip() +" " +  obj["typeofitems"] +"  from " + strPickupfrom + " To " + strDeliverto
                else:
                    strDescription = "Transporation work request created by " + obj["requestor"] 
                    
                strWorktype="TM"
                strLbl_destgroup="OTH"
                strCommgroup="FARES"
                
                if (isBlank(obj["needestimatedate"])== False):
                    strTargStart=obj["needestimatedate"]
                    strTargComp=obj["needestimatedate"]
                
                # Prepare long description
                if (isBlank(obj["noofitems"])==False):    
                    ldtext_prepared +="Number of items being moved: " + obj["noofitems"] + ldtextdelimiter
                else:
                    ldtext_prepared +="Number of items being moved: Not specified" + ldtextdelimiter
                    
                if (isBlank(obj["typeofitems"])==False):    
                    ldtext_prepared +="Type of items being moved: " + obj["typeofitems"] + ldtextdelimiter
                else:
                    ldtext_prepared +="Type of items being moved: Not specified" + ldtextdelimiter
                    
                if (isBlank(obj["itemweight"])==False):    
                    ldtext_prepared +="Item Weight: " + getAlnDomainDesc("WRC-WEIGHT",obj["itemweight"]) + ldtextdelimiter 
                else:
                    ldtext_prepared +="Item Weight: Not specified" + ldtextdelimiter 
                
                    
                if (isBlank(strPickupfrom)==False):    
                    ldtext_prepared +="Pick up from:  " + strPickupfrom + ldtextdelimiter
                    strLocation=strPickupfrom
                else:
                    ldtext_prepared +="Pick up from: Not specified" + ldtextdelimiter
                    strLocation=""  
                    
                if (isBlank(strDeliverto)==False):    
                    ldtext_prepared +="Deliver to: " + strDeliverto + ldtextdelimiter 
                else:
                    ldtext_prepared +="Deliver to: Not specified" + ldtextdelimiter
                
                if (str(obj["issalvage"])=="1" or str(obj["issalvage"])=="True" ):
                    ldtext_prepared +="Is Salvage:" + "Yes "+ldtextdelimiter
                else:
                    ldtext_prepared +="Is Salvage :" + "No "+ldtextdelimiter
              
                
                if (str(obj["isrecycle"])=="1" or str(obj["isrecycle"])=="True" ):
                    ldtext_prepared +="Recycle Pickup :" + "Yes "+ldtextdelimiter
                else:
                    ldtext_prepared +="Recycle Pickup :" + "No "+ldtextdelimiter
    
                if (str(obj["istranshazards"])=="1" or str(obj["istranshazards"])=="True" ):
                    ldtext_prepared +="Hazards exist: " + "Yes "+ldtextdelimiter
                else:
                    ldtext_prepared +="Hazards exist: " + "No "+ldtextdelimiter    
                
                if (isBlank(obj["locationnotes"])==False):    
                    ldtext_prepared +="Location Notes: " + obj["locationnotes"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Location Notes: Not specified." +ldtextdelimiter     
           
                if (isBlank(obj["needestimatedate"])== False):    
                    ldtext_prepared +="Date needed: " + obj["needestimatedate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Date needed: Not specified"  +ldtextdelimiter       
                                    
                    
            ###################
            #   CUSTODIAL
            ###################    
            if (obj["requesttype"]=="CUSTODIAL"): 
                strTodayDate=SimpleDateFormat("MM/dd/yyyy").format(Date()) 
                strDescription="Custodial request created by "  +    obj["requestor"] + " on " +   strTodayDate
                               
                
                if (isBlank(obj["building"])==False and isBlank(obj["room"])==False):
                    strLocation=obj["building"] +"-" + obj["room"]
                if (isBlank(obj["building"])==False and isBlank(obj["room"])==True):
                    strLocation=obj["building"] 
                
                if (isBlank(obj["needestimatedate"])== False):
                    strTargStart=obj["needestimatedate"]
                    strTargComp=obj["needestimatedate"]
                    
                strLbl_destgroup="OTH"
                strCommgroup="FAOPS"
                
                # Prepare long description
                if (isBlank(obj["description_longdescription"])==False):    
                    ldtext_prepared +="Detailed description: " + obj["description_longdescription"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Detailed description: Not Specified" +ldtextdelimiter
                    
                if (isBlank(obj["requestormobile"])== False):
                    ldtext_prepared +="Requestor Mobile: " + obj["requestormobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Requestor Mobile: Not specified." +ldtextdelimiter
                
                if (isBlank(obj["pointofcontact"])== False):
                    ldtext_prepared +="Point of contact: " + obj["pointofcontact"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact: Not specified." +ldtextdelimiter
               
                if (isBlank(obj["pocphone"])== False):
                    ldtext_prepared +="Point of contact phone: " + obj["pocphone"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact phone: Not specified." +ldtextdelimiter    
                
                if (isBlank(obj["pocmobile"])== False):
                    ldtext_prepared +="Point of contact mobile: " + obj["pocmobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact mobile: Not specified." +ldtextdelimiter    
                    
                if (str(obj["iscustodialwork"])=="1" or str(obj["iscustodialwork"])=="True" ):
                    ldtext_prepared +="Routine Custodial work :" + "Yes "+ldtextdelimiter
                else:
                    ldtext_prepared +="Routine Custodial work :" + "No "+ldtextdelimiter
                if (isBlank(obj["locationnotes"])==False):    
                    ldtext_prepared +="Location Notes: " + obj["locationnotes"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Location Notes: Not specified." +ldtextdelimiter 
                
                if (isBlank(obj["needestimatedate"])== False):    
                    ldtext_prepared +="Date needed: " + obj["needestimatedate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Date needed: Not specified"  +ldtextdelimiter       
                      
                                    
                strLeadcraft=getLblmaxvarvalue("WOREQ_CUSTODIAL_LEADCRAFT")
                strSupervisor=getLblmaxvarvalue("WOREQ_CUSTODIAL_SUPERVISOR")
                       
    
            ###################
            #   ESTIMATE
            ###################    
            if (obj["requesttype"]=="ESTIMATE"): 
                
                if (isBlank(obj["description_longdescription"])==False):    
                    ldtext_prepared +="Detailed description: " + obj["description_longdescription"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Detailed description: Not Specified" +ldtextdelimiter
                
                if (isBlank(obj["description"])== False):
                    ldtext_prepared +="Scope of work: " + obj["description"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Scope of work : Not specified." +ldtextdelimiter
                
                if (isBlank(obj["requestormobile"])== False):
                    ldtext_prepared +="Requestor Mobile: " + obj["requestormobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Requestor Mobile: Not specified." +ldtextdelimiter
                
                if (isBlank(obj["pointofcontact"])== False):
                    ldtext_prepared +="Point of contact: " + obj["pointofcontact"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact: Not specified." +ldtextdelimiter
               
                if (isBlank(obj["pocphone"])== False):
                    ldtext_prepared +="Point of contact phone: " + obj["pocphone"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact phone: Not specified." +ldtextdelimiter    
                
                if (isBlank(obj["pocmobile"])== False):
                    ldtext_prepared +="Point of contact mobile: " + obj["pocmobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact mobile: Not specified." +ldtextdelimiter        
                if (isBlank(obj["locationnotes"])==False):    
                    ldtext_prepared +="Location Notes: " + obj["locationnotes"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Location Notes: Not specified." +ldtextdelimiter  
                
                if (isBlank(obj["othstakeholder"])==False):    
                    ldtext_prepared +="Other stakeholder id: " + obj["othstakeholder"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Other stakeholder id : Not specified." +ldtextdelimiter   
                    
    
                if (isBlank(obj["othstakephone"])==False):    
                    ldtext_prepared +="Other stakeholder phone: " + obj["othstakephone"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Other stakeholder phone : Not specified." +ldtextdelimiter       
                
                if (isBlank(obj["othstakemobile"])==False):    
                    ldtext_prepared +="Other stakeholder mobile: " + obj["othstakemobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Other stakeholder mobile : Not specified." +ldtextdelimiter
                 
                if (isBlank(obj["fromworkcompdate"])== False):
                    ldtext_prepared +="Target Start Date: " + obj["fromworkcompdate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Target Start Date: Not specified"  +ldtextdelimiter
                    
                if (isBlank(obj["toworkcompdate"])== False):    
                    ldtext_prepared +="Target Completion Date: " + obj["toworkcompdate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Target Completion Date: Not specified"  +ldtextdelimiter           
                    
                if (isBlank(obj["workpurpose"])==False):    
                    ldtext_prepared +="Purpose of estimated work : " + getCommodityDesc(obj["workpurpose"]) +ldtextdelimiter
                    
                    strCommodity=obj["workpurpose"]
                    strCommgroup="FAESTIMATE"
                   
                else:
                    ldtext_prepared +="Purpose of estimated work : Not specified." +ldtextdelimiter
                    
                if (isBlank(obj["schedconstraints"])== False):    
                    ldtext_prepared +="Scheduling details: " + obj["schedconstraints"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Scheduling details: Not specified"  +ldtextdelimiter                
                    
                if (isBlank(obj["needestimatedate"])== False):    
                    ldtext_prepared +="Need estimate by : " + obj["needestimatedate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Need estimate by : Not specified"  +ldtextdelimiter
                           
                strDescription=obj["description"]
                
                if (isBlank(obj["building"])==False and isBlank(obj["room"])==False):
                    strLocation=obj["building"] +"-" + obj["room"]
                if (isBlank(obj["building"])==False and isBlank(obj["room"])==True):
                    strLocation=obj["building"]     
                    
                strWorktype="ET"    
                strLead=getLblmaxvarvalue("WOESTREQ_LEAD")
                strSupervisor=getLblmaxvarvalue("WOESTREQ_SUPERVISOR")
                
            ###############################
            #   PESTCONTROL / CARDCARDKEYCOMM
            ################################   
            if (obj["requesttype"]=="PESTCONTROL" or obj["requesttype"]=="CARDKEYCOMM" or obj["requesttype"]=="FURNKEYLOCKREP"):
                
                if (isBlank(obj["building"])==False and isBlank(obj["room"])==False):
                    strLocation=obj["building"] +"-" + obj["room"]
                if (isBlank(obj["building"])==False and isBlank(obj["room"])==True):
                    strLocation=obj["building"]     
                    
                if (isBlank(obj["description_longdescription"])==False):    
                    ldtext_prepared +="Detailed description: " + obj["description_longdescription"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Detailed description: Not Specified" +ldtextdelimiter
                    
                if (isBlank(obj["requestormobile"])== False):
                    ldtext_prepared +="Requestor Mobile: " + obj["requestormobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Requestor Mobile: Not specified." +ldtextdelimiter
                
                if (isBlank(obj["pointofcontact"])== False):
                    ldtext_prepared +="Point of contact: " + obj["pointofcontact"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact: Not specified." +ldtextdelimiter
               
                if (isBlank(obj["pocphone"])== False):
                    ldtext_prepared +="Point of contact phone: " + obj["pocphone"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact phone: Not specified." +ldtextdelimiter    
                
                if (isBlank(obj["pocmobile"])== False):
                    ldtext_prepared +="Point of contact mobile: " + obj["pocmobile"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Point of contact mobile: Not specified." +ldtextdelimiter    
                        
                if (str(obj["isfirstavaildate"])=="1" or str(obj["isfirstavaildate"])=="True" ):
                    ldtext_prepared +="First Available date: " + "Yes "+ldtextdelimiter
                else:
                    ldtext_prepared +="First Available date: " + "No " +ldtextdelimiter
                           
                if (isBlank(obj["fromworkcompdate"])== False):
                    ldtext_prepared +="Target Start Date: " + obj["fromworkcompdate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Target Start Date: Not specified"  +ldtextdelimiter
                    
                if (isBlank(obj["toworkcompdate"])== False):    
                    ldtext_prepared +="Target Completion Date: " + obj["toworkcompdate"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Target Completion Date: Not specified"  +ldtextdelimiter
                if (str(obj["issafetyissue"])=="1" or str(obj["issafetyissue"])=="True" ):
                    ldtext_prepared +="Safety Issue: " + "Yes "+ldtextdelimiter
                else:  
                    ldtext_prepared +="Safety Issue:  " + "No " +ldtextdelimiter
                    
                if (str(obj["ishazards"])=="1" or str(obj["ishazards"])=="True" ): 
                    ldtext_prepared +="Hazards to the Facilities staff: Yes" +ldtextdelimiter
                else:
                    ldtext_prepared +="Hazards to Facilities staff: No" +ldtextdelimiter
                     
                if (isBlank(obj["hazardsdetails"])== False):        
                    ldtext_prepared +="Hazards details:  " + obj["hazardsdetails"] +ldtextdelimiter
                else:             
                    ldtext_prepared +="Hazards details : Not specified"  +ldtextdelimiter
                    
                if (isBlank(obj["locationnotes"])==False):    
                    ldtext_prepared +="Location Notes: " + obj["locationnotes"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Location Notes: Not specified." +ldtextdelimiter     
                                    
                if (str(obj["isbldgrepair"])=="1" or str(obj["isbldgrepair"])=="True" ):
                    ldtext_prepared +="Lab overhead (building repair): " + "Yes "+ldtextdelimiter
                else:  
                    ldtext_prepared +="Lab overhead (building repair):  " + "No " +ldtextdelimiter
                                
                if (isBlank(obj["schedconstraints"])== False):    
                    ldtext_prepared +="Scheduling details: " + obj["schedconstraints"] +ldtextdelimiter
                else:
                    ldtext_prepared +="Scheduling details: Not specified"  +ldtextdelimiter
                
                if (obj["requesttype"]=="PESTCONTROL"):                 
                    strWorktype=getLblmaxvarvalue("WOPESTREQ_WORKTYPE")                               
                    strSupervisor=getLblmaxvarvalue("WOPESTREQ_SUPERVISOR")
                    
                
                if (obj["requesttype"]=="CARDKEYCOMM"):                 
                    strLeadcraft=getLblmaxvarvalue("WOREQ_CARDKEY_LEADCRAFT")            
                    strSupervisor=getLblmaxvarvalue("WOREQ_CARDKEY_SUPERVISOR")    
        
            ################################
            #   NEWKEY and TRANSFERKEY 
            ################################   
            if (obj["requesttype"]=="NEWKEY" or obj["requesttype"]=="TRANSFERKEY" ):
                
                if (isBlank(obj["requestor"])== False): 
                    ldtext_prepared +="Requestor: " + obj["requestor"] + ldtextdelimiter
                    ldtext_prepared +="Division: " + getPersondivision(obj["requestor"]) + ldtextdelimiter
                
                if (isBlank(obj["receiver"])== False):
                    ldtext_prepared +="Receiver: " + obj["receiver"] +"-" + getPersonname(obj["receiver"])+  ldtextdelimiter    
                if (isBlank(obj["prevkeyowner"])== False):
                    ldtext_prepared +="Previous Owner: " + obj["prevkeyowner"] +"-" + getPersonname(obj["prevkeyowner"])+  ldtextdelimiter
                                   
                if (str(obj["isreceivermatrix"])=="1" or str(obj["isreceivermatrix"])=="True" ): 
                    ldtext_prepared +="Matrixed to other division: Yes" + ldtextdelimiter
                else:
                    ldtext_prepared +="Matrixed to other division: No" + ldtextdelimiter
                    
                if (isBlank(obj["matrixedtodivision"]) ==False):
                    ldtext_prepared  +="Matrixed to Division: " + getDivisionDesc(obj["matrixedtodivision"]) +    ldtextdelimiter      
                               
                if (isBlank(obj["building"]) ==False):
                    ldtext_prepared  +="Building: " + obj["building"] +    ldtextdelimiter  
                    
                if (isBlank(obj["room"]) ==False):
                    ldtext_prepared  +="Room: " + obj["room"] +    ldtextdelimiter  
                
                if (isBlank(obj["keysequence"]) ==False):
                    ldtext_prepared  +="Key Sequence: " + obj["keysequence"] +    ldtextdelimiter
                    
                if (isBlank(obj["knumber"]) == False):
                    ldtext_prepared  +="K Number: " + obj["knumber"] +    ldtextdelimiter
                    
                if (isBlank(obj["project_id"]) ==False):
                    ldtext_prepared  +="Project Id: " + obj["project_id"] +    ldtextdelimiter
                    
                if (isBlank(obj["activity_id"]) ==False):
                    ldtext_prepared  +="Activity Id: " + obj["activity_id"] +    ldtextdelimiter
                
                if (isBlank(obj["keydateneeded"]) ==False):
                    ldtext_prepared  +="Key Date needed: " + obj["keydateneeded"] +    ldtextdelimiter
                    
                if (isBlank(obj["keyauthorizer"]) ==False):
                    ldtext_prepared  +="Key Authorizer: " + obj["keyauthorizer"] + "-" + getPersonname(obj["keyauthorizer"]) +   ldtextdelimiter   
                    
                if (isBlank(str(obj["isrush"]))== False):
                    if (str(obj["isrush"])=="1" or str(obj["isrush"])=="True" ): 
                        ldtext_prepared  +="Rush: Yes "   + ldtextdelimiter   
                    else:
                        ldtext_prepared  +="Rush: No "  + ldtextdelimiter 
               
                    
                if (isBlank(obj["description_longdescription"]) ==False):
                    ldtext_prepared  +="Comments: " + obj["description_longdescription"] +    ldtextdelimiter
                
                     
                if (isBlank(obj["mailstop"]) ==False):
                    ldtext_prepared  +="Mailstop: " + obj["mailstop"] +    ldtextdelimiter
                       
                if (str(obj["isrush"])=="1" or str(obj["isrush"])=="True" ):                   
                    strDescription="[RUSH] New key from " +obj["requestor"]
                else:
                    strDescription="New key from " +obj["requestor"]
                    
                strLocation="076-0233A"
                strSupervisor=getLblmaxvarvalue("LOCKSHOP_SUPERVISOR")
                strWorktype="LS"
              
                        
            ################################
            #   TRANSFER KEY - SR
            ################################   
            if (obj["requesttype"]=="TRANSFERKEY" ):
                strDescription="Request for transfer of a key from " + obj["requestor"]
                
                if (isBlank(obj["documenttype"])==False and isBlank(obj["documentnumber"])==False):
                    strDocumenttype=obj["documenttype"]
                    strDocumentnumber=obj["documentnumber"]
                    srsetRemote.setUserWhere("tickeid='" +  strDocumentnumber +"'")
        
                    if (not srsetRemote.isEmpty()):
                        mboSr=srsetRemote.getMbo(0)
                else:
                        
                        mboSr=srsetRemote.add()
                        strSrnum=mboSr.getString("ticketid")
                
                mboSr.setValue("description", strDescription,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboSr.setValue("description_longdescription", ldtext_prepared.strip(),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboSr.setValue("orgid", "LBNL",  MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboSr.setValue("siteid", "FAC" ,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
        
                mboSr.setValue("reportedby", obj["requestor"],MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                
                if (isBlank(obj["reportdate"])== False):
                    mboSr.setValue("reportdate" ,obj["reportdate"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                #else:
                #    mboSr.setValue("reportdate",  MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                #'''
                
            
                #mboSr.setValue("owner", obj["requestor"],MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboSr.setValue("REPORTEDPHONE", getPhone( obj["requestor"]),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboSr.setValue("REPORTEDEMAIL", getEmailaddress( obj["requestor"]),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)            
                mboSr.setValue("AFFECTEDPERSON", obj["keyreceiver"],MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                if (isBlank(obj["keyreceiver"])==False):
                    mboSr.setValue("AFFECTEDPHONE", getPhone(obj["keyreceiver"]),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                    mboSr.setValue("AFFECTEDEMAIL", getEmailaddress(obj["keyreceiver"]),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboSr.setValue("classstructureid", strClassificationid_TransferKey, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboSr.setValue("status", "NEW", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                   
                facworkrequestSet.setValue("DOCUMENTTYPE" ,"SR",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                facworkrequestSet.setValue("DOCUMENTNUMBER" ,strSrnum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                          
                                    
            if (obj["requesttype"] != "TRANSFERKEY" ): 
            ################################ Common for all work order related requests######################
            
                if (isBlank(obj["documenttype"])==False and isBlank(obj["documentnumber"])==False):
                    strDocumenttype=obj["documenttype"]
                    strDocumentnumber=obj["documentnumber"]
                    wosetRemote.setUserWhere("orgid='LBNL' and siteid='FAC' and wonum='" +  strDocumentnumber +"'")
        
                    if (not wosetRemote.isEmpty()):
                        mboWorkorder=wosetRemote.getMbo(0)
                        strWonum=mboWorkorder.getString("wonum")
                else:                   
                    mboWorkorder=wosetRemote.add()    
                    strWonum=mboWorkorder.getString("wonum")
                    
            
                #if (isBlank(strLocation)==True):
                #        strLocation=getPersonlocation(obj["requestor"])
                  
               
                if (isBlank(strLocation)==False):
                        locationSetRemote= MXServer.getMXServer().getMboSet("LOCATIONS", runAsUserInfo1)
                        locationSetRemote.setUserWhere("orgid='LBNL' and siteid='FAC' and location='" + strLocation +"'")
                        if (not locationSetRemote.isEmpty()):
                            strEscortReqd=locationSetRemote.getMbo(0).getString("LBL_ESCORT_REQD")
                            strCommentsCondRel=locationSetRemote.getMbo(0).getString("LBL_COMMENTS_CONDR")
                            strCondRel=locationSetRemote.getMbo(0).getString("LBL_COND_RELEASE")
                        
                        locationSetRemote=None  
                   
                facworkrequestSet.setValue("DOCUMENTTYPE" ,"WORKORDER",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                facworkrequestSet.setValue("DOCUMENTNUMBER" ,strWonum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                facworkrequestSet.setValue("description",strDescription,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            
                 
                mboWorkorder.setValue("orgid", "LBNL", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("siteid", "FAC", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                
                strLocationDesc=getLocationDesc(strLocation)
                if (isBlank(strLocationDesc)==False):
                    mboWorkorder.setValue("location", strLocation,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                    
                if (isBlank(strLocation)==True):
                    mboWorkorder.setValueNull("location", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)

                                   
                mboWorkorder.setValue("reportedby", obj["requestor"],MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                
                   
                if (isBlank(obj["reportdate"])== False):
                    mboWorkorder.setValue("reportdate" ,obj["reportdate"],MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                #else:
                #    mboWorkorder.setValue("reportdate",  MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                            
                mboWorkorder.setValue("description", strDescription[0:50],MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("description_longdescription", ldtext_prepared.strip(),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("wo1", strWo1,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                
                if (obj["requesttype"] == "NEWKEY" ):
                    mboWorkorder.setValue("onbehalfof", obj["keyreceiver"],MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                    mboWorkorder.setValue("LBL_WORKCNTRHAZARD", "1",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                    mboWorkorder.setValue("classstructureid", strClassificationid_NewKey, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                    
                else:
                    mboWorkorder.setValue("onbehalfof", strWo1,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    
                mboWorkorder.setValue("wo5", strWo5,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("phone", strPhone,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                
                strCOADesc=getCOADesc(strGlaccount)
                if (isBlank(strCOADesc)==False):
                    mboWorkorder.setValue("glaccount", strGlaccount,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
               
                if (isBlank(strGlaccount)== True):
                    mboWorkorder.setValueNull("glaccount", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                    
                       
                mboWorkorder.setValue("TARGSTARTDATE", strTargStart,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("TARGCOMPDATE", strTargComp,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("changedate" ,MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
                mboWorkorder.setValue("changeby" ,"IT-BS-MXINTADM", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                mboWorkorder.setValue("LBL_DESTGROUP", strLbl_destgroup,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION) 
                mboWorkorder.setValue("LBL_ESCORT_REQD", strEscortReqd,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("LBL_CONDITION_REL", strCondRel,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("LBL_CONDITION_REL_LONGDESCRIPTION", strCommentsCondRel,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                myLogger.debug("PRB  before setting comm group----> " +strCommgroup )
                mboWorkorder.setValue("commoditygroup", strCommgroup,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("commodity", strCommodity,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("leadcraft", strLeadcraft,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("lead", strLead,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("supervisor", strSupervisor,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                mboWorkorder.setValue("worktype", strWorktype,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                
                
                if (obj["requesttype"] == "GENERAL"):
                    if (str(obj["isescortrequired"])=="1" or str(obj["isescortrequired"])=="True" ):
                        mboWorkorder.setValue("LBL_ESCORT_REQD", "Y",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                    else:
                        mboWorkorder.setValue("LBL_ESCORT_REQD", "N",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                        
                    
             
        
        
            lbl_facworkrequestRemote.save()
            wosetRemote.save()
            srsetRemote.save()
            
        lbl_facworkrequestRemote=None
        wosetRemote=None    
        srsetRemove=None
    
        
resp = JSONObject()

resp.put("result","Successful")    

if (isBlank(strWonum)==False):
    resp.put("documenttype","WORKORDER")       
    resp.put("documentnumber",strWonum)
else:
    resp.put("documenttype","SR")
    resp.put("documentnumber",strSrnum)

responseBody = resp.serialize(True)