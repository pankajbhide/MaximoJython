##########################################################################
# Purpose: Script for generating work orders for testing the scaleability 
#          for workflow
#
# Author : Pankaj Bhide
#
# Date    : Apr 21 2017
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

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

# Open connection from db connection pool 
mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
conKey = mxServer.getSystemUserInfo().getConnectionKey()
con = mxServer.getDBManager().getConnection(conKey)
print "PRB in the script"
# Create wosetRemote collection for work orders
wosetRemote= MXServer.getMXServer().getMboSet("WORKORDER", runAsUserInfo1)

# Loop to create 150 work order
for intNumberworkorders in xrange(150):
    print "PRB processing records"
    # Dummy select for db connection
    strSelect="select to_char(sysdate,'YYYY-MM-DD HH24:MI:SS') as now1  from dual"
    results=con.createStatement().executeQuery(strSelect)
    
    while results.next():
        strNow=results.getString("now1")
        
    results.close()
         
    # Add new work order from the collection 
    mboWorkorder=wosetRemote.add()    
    strWonum=mboWorkorder.getString("wonum")
    print "PRB work order: " + strWonum
    
    # Prepare work order description
    strDescription ="Test: Work order created for load testing-" + str(intNumberworkorders) + " : " +  strNow
    
    mboWorkorder.setValue("description", strDescription, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION);
    mboWorkorder.setValue("orgid", "LBNL", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("siteid", "FAC", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("reportedby", "813149",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("reportdate",mxServer.getDate(),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("location","069-0102D",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
           
wosetRemote.save()
results.close()
con.commit()

wosetRemote=None
srsetRemote=None  
woset2Remote=None
Rs1=None

 # At the end of the program release the db connection to the pool
mxServer.getDBManager().freeConnection(conKey) 
conn=None            
