###########################################################
# Purpose: Script for object level  launch for ROUTE_STOP
#
# Author : Pankaj Bhide
#
# Date    : Aug 1, 2019
#
# Revision
# History : 
#
##########################################################
from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap

def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams",errparm)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
    
def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

  
if (onadd == True or onupdate == True):
    
    if (mbo.getOwner() is not None):
    
        strRoutetype=mbo.getOwner().getString("lbl_routetype")
        if (strRoutetype=="FEG"):
            # Validate that only 1 primary is indicated.
            thisSet=mbo.getThisMboSet()
            intTotalPrimary=0 
            intCount=thisSet.count()
            
            for i in xrange(intCount):
                    
                    if (thisSet.getMbo(i).toBeDeleted() == False):
                    
                        if (isBlank(mbo.getString("assetnum"))== True):   
                            setError("lbl_assetnumreqd","route"," ") 
                
                        if (thisSet.getMbo(i).getBoolean("LBL_ISPRIMARY") == True):
                            intTotalPrimary=intTotalPrimary + 1
                            
                        if (intTotalPrimary > 1):
                            setError("lbl_onlyoneprimaryallowed","route"," ")              
                                                  
                        
                
                
                
                