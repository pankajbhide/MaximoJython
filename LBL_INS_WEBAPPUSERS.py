##########################################################################
# Purpose: Script for inserting the web application user 
#          TAD application
#
# Author : Pankaj Bhide
#
# Date    : June 6 2019
#
# Revision
# History :
#
###########################################################################
from psdi.server import MXServer
from com.ibm.json.java import JSONObject
from org.python.core.util import StringUtil
from com.ibm.tivoli.maximo.oslc import OslcUtils
from com.ibm.tivoli.maximo.oslc.provider.OslcRequest import *
from psdi.mbo  import   MboConstants

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True







#################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently comment#################

# Get Response body 
resp = str(requestBody)  
# Convert to JSON Array
reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(resp))

# Navigate elements from array 
strUserid =""
strWebapp=""
strOrglevel1=""
strOrgid=""
strSiteid=""

for i in range(len(reqData)):
    
    strUserid=reqData.get(i).get("userid")
    strWebapp=reqData.get(i).get("webapp")
    strOrglevel1=reqData.get(i).get("org_level_1")
    strOrgid=reqData.get(i).get("orgid")
    strSiteid=reqData.get(i).get("siteid")
    

 

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
webAppSet= MXServer.getMXServer().getMboSet("lbl_webapp_users", runAsUserInfo1)


newWebapp=webAppSet.add()
newWebapp.setValue("userid",strUserid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
newWebapp.setValue("webapp",strWebapp, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
newWebapp.setValue("org_level_1",strOrglevel1, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
newWebapp.setValue("orgid",strOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
newWebapp.setValue("siteid",strOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)         
newWebapp.setValue("changeby", runAsUserInfo1.getUserName(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
newWebapp.setValue("changedate",mxServer.getDate(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
  
    
webAppSet.save()


#
resp = JSONObject()
resp.put("lbl_webapp_users","success")
responseBody = resp.serialize(True)