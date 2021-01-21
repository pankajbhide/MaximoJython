###################################################################################################
# Purpose: Script for inserting/rows in lbl_wofeedback and lbl_wofeedbackcomments MBOs based upon 
#          the JSON payload received
#
# Author : Pankaj Bhide
#
# Date    : February 13, 2020
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
lblwofeedbackCommentsSet= MXServer.getMXServer().getMboSet("lbl_wofeedbackcomments", runAsUserInfo1)

for i in range(len(reqData)):
    obj=reqData[i]
    
    obj["documentnumber"]="" if ( not "documentnumber" in obj)  else obj["documentnumber"]
    obj["comments_provided"]="" if ( not "comments_provided" in obj)  else obj["comments_provided"]
    obj["feedback_provided"]="" if ( not "feedback_provided" in obj)  else obj["feedback_provided"]
    obj["requestor"]="" if ( not "requestor" in obj)  else obj["requestor"]
    
    strWonum=obj["documentnumber"] 
    strComments=obj["comments_provided"]    
    strFeedback=obj["feedback_provided"]    
    strCustomer=obj["requestor"]
    
if (isBlank(strWonum) == False and isBlank(strFeedback)== False):
        #split string based upon comma 
        listFeedback=strFeedback.split(",")
        
        for strTemp in listFeedback:
            
            strTemp2=strTemp.split("-")
            strId=strTemp2[0]
            strValue=strTemp2[1]
            
            newWoFeedback=lblwofeedbackSet.add()
            newWoFeedback.setValue("orgid","LBNL",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWoFeedback.setValue("siteid","FAC",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWoFeedback.setValue("wonum", strWonum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWoFeedback.setValue("customerid",strCustomer,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION) 
            newWoFeedback.setValue("id",strId,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWoFeedback.setValue("value",strValue,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWoFeedback.setValue("changeby", runAsUserInfo1.getUserName(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWoFeedback.setValue("changedate",mxServer.getDate(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        
        lblwofeedbackSet.save()
 
if (isBlank(strWonum) == False and isBlank(strComments)== False):      
    newWoFeedbackcomments=lblwofeedbackCommentsSet.add()
    newWoFeedbackcomments.setValue("orgid","LBNL",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    newWoFeedbackcomments.setValue("siteid","FAC",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    newWoFeedbackcomments.setValue("wonum", strWonum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    newWoFeedbackcomments.setValue("customerid",strCustomer,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION) 
    newWoFeedbackcomments.setValue("comments",strComments,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    
    lblwofeedbackCommentsSet.save()
    
    
lblwofeedbackSet=None
lblwofeedbackCommentsSet=None

resp = JSONObject()
resp.put("result","Successful")    

if (isBlank(strWonum)==False):
    resp.put("documenttype","WORKORDER")       
    resp.put("documentnumber",strWonum)
else:
    resp.put("documenttype","SR")
    resp.put("documentnumber",strSrnum)

responseBody = resp.serialize(True)
     

