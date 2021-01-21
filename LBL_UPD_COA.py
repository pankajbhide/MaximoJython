##########################################################################
# Purpose: Script for updating the rows in chartoaccounts table

# Author : Pankaj Bhide
#
# Date    : June 2018
#
# Revision
# History :
#
######################################################
from psdi.server import MXServer
from com.ibm.json.java import JSONObject
from org.python.core.util import StringUtil
from com.ibm.tivoli.maximo.oslc import OslcUtils

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


# Get Site id and work order number from the MBO
#strWonum=mbo.getString("wonum")
#strSite=mbo.getString("siteid")

####################################################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently commented
###################################################################
'''
# Get Response body 
resp = str(requestBody)  
# Convert to JSON Array
reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(resp))

# Navigate elements from array 
for i in range(len(reqData)):
    print "PRB location: " + reqData.get(i).get("location")
'''    
################################################################

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
conKey = mxServer.getSystemUserInfo().getConnectionKey()

################################################################################
# If siteid and work order are not null then, get reference of tooltrans records
################################################################################

con = mxServer.getDBManager().getConnection(conKey)

strUpdate  ="update maximo.chartofaccounts a "
strUpdate +=" set (a.active, a.accountname,a.lbl_project_id,a.lbl_activity_id, "
strUpdate +=" a.lbl_proj_desc, a.lbl_act_desc,a.lbl_changedate "
strUpdate +=") ="
strUpdate +="(select b.active,b.comptext, b.lbl_project_id,b.lbl_activity_id, "
strUpdate +="b.lbl_proj_desc, b.lbl_act_desc,sysdate "
strUpdate +="from maximo.glcomponents b "
strUpdate +="where b.compvalue=a.glaccount ) "



stmtUpdate=con.prepareStatement(strUpdate)
stmtUpdate.executeUpdate()
try:
    stmtUpdate.close()
    con.commit()

except:
    con.rollback()


# At the end of the program release the db connection to the pool
mxServer.getDBManager().freeConnection(conKey)
stmtUpdate=None
conn=None

resp = JSONObject()
resp.put("coa","updated")
responseBody = resp.serialize(True)
