####################################################
# Purpose: ACTION LAUNCH POINT ON WORKORDER
#
# Author : Pankaj Bhide
#
# Date    : March 2, 2017
#
# Revision
# History : Change the status of the work order to WPLAN
#
##########################################################

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

logger = mbo.getMboLogger()


if (jIOrgid=="LBNL" and jISiteid=="FAC"):
   
    
    if (mbo.getString("status") !="WPLAN"):
        
        
        #strWhere1  = "orgid='" + jIOrgid +"' and siteid='" + jISiteid +"' and wonum='"+ mbo.getString("wonum") + "'"
        #workordersSet= MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())
        #workordersSet.setUserWhere(strWhere1)
        
        
        mbo.getThisMboSet().getApp().getResultsBean().getSelection()
        workordersSet=mbo.getThisMboSet()
        if (not workordersSet.isEmpty()):
            workordersSet.getMbo(0).changeStatus("WPLAN",  MXServer.getMXServer().getDate(),
                                                "Changed by action",
                                                MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            workordersSet.save()
                          
               
        
        
                
            
            
            
        
        
        
