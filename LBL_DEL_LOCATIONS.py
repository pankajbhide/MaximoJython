##########################################################################
# Purpose: Script for deleting rows from locatons

# Author : Pankaj Bhide
#
# Date    : Sept 29 2018
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

#query_string=request.getQueryParam("location_type")

#strLocationtype=""
#for item in query_string:
#    strLocationtype +=item

                            

####################################################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently comment#################

# Get Response body 
resp = JSONObject()
resp.put("locations","deleted")  

# Convert to JSON Array
reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(resp))

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
locationsSetRemote= MXServer.getMXServer().getMboSet("LOCATIONS", runAsUserInfo1)
print "PRB request: " + str(reqData)

# Navigate elements from array (first pass disable them)  
for i in range(len(reqData)):
    print "PRB location: " + reqData.get(i).get("location")
      
    locationsSetRemote.setWhere("location='" + reqData.get(i).get("location") +"'")
    locationsSetRemote.reset()
    location = locationsSetRemote.moveFirst()
    location.setValue("disabled",True, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    location.save()
    
# Navigate elements from array  (second pass delete them)
for i in range(len(reqData)):
    print "PRB location: " + reqData.get(i).get("location")
    
  
    locationsSetRemote.setWhere("location='" + reqData.get(i).get("location") +"'")
    locationsSetRemote.reset()
    location = locationsSetRemote.moveFirst()
    
    try:
        
        location.delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        location.save()    
   

################################################################
    finally:
        pass
        
        


responseBody = resp.serialize(True)