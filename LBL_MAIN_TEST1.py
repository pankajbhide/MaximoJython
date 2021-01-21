##########################################################################
# Purpose: Script for changing WPLabor data JIRA EF-7872
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
workorderSet = mxServer.getMboSet('SR', runAsUserInfo1 )

   
        
##################################
# Add parent work order in WPlabor
################################### 
#strWhere  =" orgid='LBNL' and siteid='FAC' and reportedby='813149' "
strWhere  =" orgid='LBNL' and siteid='FAC' and affectedperson='813149' "

workorderSet.setWhere (strWhere)
#workorderSet.setWhere (" orgid='LBNL' and siteid='FAC' and wonum='W0123832' ") 
workorderSet.reset()
if workorderSet is not None:
    intCount1=workorderSet.count()
    # Loop through each row from the collection
    for i in xrange(intCount1):
        
        print "Processing Work order: "  + workorderSet.getMbo(i).getString("description")
        
workorderSet.close() 
