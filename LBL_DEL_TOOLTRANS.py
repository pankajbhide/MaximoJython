##########################################################################
# Purpose: Script for deleting rows in tooltrans table

# Author : Pankaj Bhide
#
# Date    : May 4, 2018
#
# Revision
# History :
#
######################################################
from psdi.server import MXServer
from com.ibm.json.java import JSONObject

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


# Get Site id and work order number from the MBO
#strWonum=mbo.getString("wonum")
#strSite=mbo.getString("siteid")
resp = JSONObject()
resp.put("tooltrans","deleted")
mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
conKey = mxServer.getSystemUserInfo().getConnectionKey()

################################################################################
# If siteid and work order are not null then, get reference of tooltrans records
################################################################################

con = mxServer.getDBManager().getConnection(conKey)
strDelete  =" delete from maximo.tooltrans "
strDelete +=" where orgid='LBNL' and siteid='FAC' "
strDelete +=" and TT1='W' "
strDelete +=" and MEMO LIKE 'PRELIMINARY%' "

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
responseBody = resp.serialize(True)