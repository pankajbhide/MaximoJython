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

workorderSet = mxServer.getMboSet('WORKORDER', runAsUserInfo1 )
wpLaborSet1 = mxServer.getMboSet('WPLABOR', runAsUserInfo1 )
wpLaborSet2 = mxServer.getMboSet('WPLABOR', runAsUserInfo1 )
   
        
##################################
# Add parent work order in WPlabor
################################### 
strWhere  =" wonum in "
strWhere +=" (select b.parent from wplabor, workorder b " 
strWhere +=" where b.wonum=wplabor.wonum and "
strWhere +=" wpl1='X') and status not in ('COMP','CAN','CLOSE','WCLOSE','WCOMP') "

workorderSet.setWhere (strWhere)
#workorderSet.setWhere (" orgid='LBNL' and siteid='FAC' and wonum='W0123832' ") 
workorderSet.reset()
if workorderSet is not None:
    intCount1=workorderSet.count()
    # Loop through each row from the collection
    for i in xrange(intCount1):
        
        print "Processing Work order: "  + workorderSet.getMbo(i).getString("wonum")
        
        WPLaborSetRemote   =workorderSet.getMbo(i).getMboSet("SHOWALLPLANLABOR")
        WPLaborSetNewRemote=workorderSet.getMbo(i).getMboSet("WPLABOR")
        
        intCount2=0
        if WPLaborSetRemote is not None:
            intCount2=WPLaborSetRemote.count()
            
        strCraft=""
        dblQty=0
            
        # Loop through each row from the collection
        for j in xrange(intCount2):
            strCraft=WPLaborSetRemote.getMbo(j).getString("craft")
            dblQty=WPLaborSetRemote.getMbo(j).getDouble("quantity")
        
        if (intCount2 > 0):
            newWPLaborSetRemote = WPLaborSetNewRemote.add()
            newWPLaborSetRemote.setValue("wonum",workorderSet.getMbo(i).getString("wonum"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWPLaborSetRemote.setValue("craft",strCraft,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWPLaborSetRemote.setValue("wpl1","A",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newWPLaborSetRemote.setValue("quantity",dblQty,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            print "Work order " + workorderSet.getMbo(i).getString("wonum") + " added."
            WPLaborSetNewRemote.save()
            WPLaborSetNewRemote.close()
                    
        WPLaborSetRemote.close()
        
workorderSet.close() 
