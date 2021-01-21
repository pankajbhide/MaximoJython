##########################################################################
# Purpose: Script for updating asset meters for fleet vehicles, executed
#          via datastage job
#
# Author : Pankaj Bhide
#
# Date    : November 2019
#
# Revision
# History :
#
######################################################
from psdi.server import MXServer
from com.ibm.json.java import JSONObject
from org.python.core.util import StringUtil
from com.ibm.tivoli.maximo.oslc import OslcUtils
from psdi.util.logging import MXLoggerFactory
from java.sql import *
from java.text import SimpleDateFormat
from psdi.mbo  import   MboConstants


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


# Get Site id and work order number from the MBO
#strWonum=mbo.getString("wonum")
#strSite=mbo.getString("siteid")


myLogger = MXLoggerFactory.getLogger("maximo.script.customscript")

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
AssetMeterRemote= MXServer.getMXServer().getMboSet("ASSETMETER", runAsUserInfo1)


for i in range(len(reqData)):

    obj=reqData[i]
    row_count =row_count + 1
                             
    assetnum=obj["_data"]["assetnum"]
    odometer=0
    odometer=obj["_data"]["odometer"]
    strodometer=""
    strodometer= str(odometer)
    
    
       
    strWhere1 =" orgid='LBNL' and siteid='FAC' and assetnum='" + assetnum + "' and metername='FLEET' "
    AssetMeterRemote.setUserWhere(strWhere1)
    if (not AssetMeterRemote.isEmpty()):
        AssetMeterRemote.getMbo(0).setValue("lastreading",strodometer,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        AssetMeterRemote.getMbo(0).setValue("lastreadingdate", MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        AssetMeterRemote.getMbo(0).setValue("inspector", "IT-BS-MXINTADM",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        AssetMeterRemote.save()
        
        
        
        
     

