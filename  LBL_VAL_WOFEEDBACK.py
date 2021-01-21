###################################################################################################
# Purpose: Script for validating whether work order is eligible to receive the feedback or not
#
# Author : Pankaj Bhide
#
# Date    : April 14, 2020
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
from java.text import SimpleDateFormat
from psdi.mbo import MboConstants



def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def isNull(myObject):
    if (myObject is None):
        return True
    else:
        return False

strWonum=""
strSrnum=""

myLogger = MXLoggerFactory.getLogger("maximo.script.autoscript")


####################################################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently commented
###################################################################



myLogger.debug("PRB just converted reqdata")
resp = str(requestBody)  
# Convert to JSON Array
reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(resp))

# Navigate elements from array 
mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")

lblwofeedbackSet= MXServer.getMXServer().getMboSet("lbl_wofeedback", runAsUserInfo1)
workordersSet= MXServer.getMXServer().getMboSet("workorder", runAsUserInfo1)

for i in range(len(reqData)):
    obj=reqData[i]
    
    obj["documentnumber"]="" if ( not "documentnumber" in obj)  else obj["documentnumber"]
    obj["requestor"]="" if ( not "requestor" in obj)  else obj["requestor"]
    
    strWonum=obj["documentnumber"]   
    strCustomer=obj["requestor"]
    
strMessage=""
resp = JSONObject()
  

if (isBlank(strWonum)==True):
    strMessage="ERROR: Work order number can not be blank."
    
if (isBlank(strMessage)== True and isBlank(strCustomer)==True):
    strMessage="ERROR: Requestor can not be blank."
    
if (isBlank(strMessage)== True):
    strWhere="orgid='LBNL' and siteid='FAC' and wonum='" + strWonum +"'"
    strWhere += " and ( reportedby='" + strCustomer +"' or wo1='" + strCustomer +"' or onbehalfof='" + strCustomer +"') "
    strWhere += "  and lbl_feedbackreq_dt is not null"     
    workordersSet.setUserWhere(strWhere)
    if (workordersSet.isEmpty()):
        strMessage="ERROR: This work order is not eligible to receive feedback."
    workordersSet=None

if (isBlank(strMessage)== True):
    strWhere="orgid='LBNL' and siteid='FAC' and wonum='" + strWonum +"' and customerid='"+  strCustomer +  "'"
    lblwofeedbackSet.setUserWhere(strWhere)
    if (not lblwofeedbackSet.isEmpty()):
        strMessage="ERROR: Feedback is already recorded for this work order."
    lblwofeedbackSet=None
 
if (isBlank(strMessage)== True):
    resp.put("result","Success")  
else:
    resp.put("result",strMessage)  
    
resp.put("documenttype","WORKORDER")       
resp.put("documentnumber",strWonum)
 
responseBody = resp.serialize(True)
     

