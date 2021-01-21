##########################################################################
# Purpose: Script for changing WPLabor data JIRA EF-8268
#
# Author : Pankaj Bhide
#
# Date    : June 25, 2018 
#
# Revision
# History : 
#
######################################################
import time
from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from com.ibm.json.java import JSONObject

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


    
#########################################################
       
# Open MXServer session
mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")

#workorderSet = mxServer.getMboSet('WORKORDER', runAsUserInfo1 )
WPSet = mxServer.getMboSet('WPLABOR', runAsUserInfo1 )

   
        
##################################
# Add parent work order in WPlabor
################################### 
#strWhere  =" orgid='LBNL' and siteid='FAC' and reportedby='813149' "


strWhere  =" orgid='LBNL' and siteid='FAC' and craft ='FATSE' and "
strWhere  +=" wonum in (select w.wonum from workorder w where " 
strWhere  +=" w.reportdate >= to_date('01-01-2017','DD-MM-YYYY') and w.status not in ('COMP','WCOMP','CAN','CLOSE'))"
strWhere  +=" order by wonum,craft"

WPSet.setWhere (strWhere)
#workorderSet.setWhere (" orgid='LBNL' and siteid='FAC' and wonum='W0123832' ") 
WPSet.reset()

if WPSet is not None:
    intCount1=WPSet.count()
    print "total count: " + str(intCount1)
    # Loop through each row from the collection
    for i in xrange(intCount1):
        
        print "processing row: " +str(i)
        print "About to processing Work order: "  + WPSet.getMbo(i).getString("wonum")
        
        if (isBlank(WPSet.getMbo(i).getString("craft"))==False):
            WPSet.getMbo(i).setValue("craft","FATSE2",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            

WPSet.save()        
WPSet.close() 
resp = JSONObject()
resp.put("WPLabor","updated")
responseBody = resp.serialize(True)