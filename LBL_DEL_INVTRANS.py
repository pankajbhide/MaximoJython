##########################################################################
# Purpose: Script for deleting rows from invtrans table via jdbc

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

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

query_string=request.getQueryParam("financialperiod")

strFinancialperiod=""
for item in query_string:
    strFinancialperiod +=item

                            

####################################################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently comment#################

# Get Response body 
resp = str(requestBody)  
# Convert to JSON Array
reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(resp))

# Navigate elements from array 
#for i in range(len(reqData)):
#    print "PRB location: " + reqData.get(i).get("location")
'''    
################################################################

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
conKey = mxServer.getSystemUserInfo().getConnectionKey()

################################################################################
# If siteid and work order are not null then, get reference of tooltrans records
################################################################################

con = mxServer.getDBManager().getConnection(conKey)
strDelete  =" delete from maximo.invtrans"
strDelete +=" where orgid='LBNL' and siteid='FAC' "
strDelete +=" and financialperiod='" + strFinancialperiod + "'"
strDelete +=" and transtype='ROUNDADJ'" 

stmtDelete=con.prepareStatement(strDelete)
stmtDelete.executeUpdate()
try:
    stmtDelete.close()
    con.commit()

except:
    con.rollback()


# At the end of the program release the db connection to the pool
mxServer.getDBManager().freeConnection(conKey)
stmtDelete=None
conn=None
resp = JSONObject()
resp.put("invtrans","deleted")
responseBody = resp.serialize(True)