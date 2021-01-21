# Purpose: Object level (save) on LBL_LABTRANS
#
# Author : Pankaj Bhide
#
# Date    : Aug 31, 2015
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

logger = mbo.getMboLogger()



if (jIOrgid=="LBNL" and jISiteid=="FAC"):
   
    
    if (mbo.getString("lbl_status")=="COMPLETE"):
        
        lngLblLabtransid=mbo.getLong("lbl_labtransid")
        
        strWhere   =" siteid='" + jISiteid + "'" 
        strWhere= strWhere + " and refwo='"+ mbo.getString("refwo") +"'" 
        strWhere= strWhere + " and orgid='"+ jIOrgid + "'" 
        strWhere= strWhere + " and lbl_status !='COMPLETE'  "
        strWhere= strWhere + " and lbl_transtype='PLAN' "
        strWhere= strWhere + " and lbl_labtransid !=" + str(lngLblLabtransid) 
        LblLabtransSet= MXServer.getMXServer().getMboSet("LBL_LABTRANS", mbo.getUserInfo())
        LblLabtransSet.setUserWhere(strWhere)
        
        
     
        boolUpdateWoStatus=1
        if (not LblLabtransSet.isEmpty()):
            boolUpdateWoStatus=0
        
       
         
        if (boolUpdateWoStatus == 1):
            strWhere="siteid='" + jISiteid + "'" 
            strWhere= strWhere + " and wonum='"+ mbo.getString("refwo") +"'" 
            WorkordersSet= MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())
            WorkordersSet.setUserWhere(strWhere)
            
            
            if (not WorkordersSet.isEmpty()):
                
                       
                WorkordersSet.getMbo(0).changeStatus("WCOMP",
                                    MXServer.getMXServer().getDate(),
                                    "All assignments are marked as completed dataSplice",
                                    MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
              
                WorkordersSet.save()                                         
             
                
            
            
            
        
        
        
