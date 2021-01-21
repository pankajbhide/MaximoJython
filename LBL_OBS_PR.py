# Purpose: Object level (save) on PR 
#
# Author : Pankaj Bhide
#
# Date    : Sept 8 , 2015
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
from java.util import HashMap


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams","")
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
    

logger = mbo.getMboLogger()



if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
    if (isBlank(mbo.getString("lbl_requestedby")) == False):
        mbo.setValue("requestedby", mbo.getString("lbl_requestedby"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    else:        
        mbo.setValue("requestedby", user.upper() ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
   
    
    if (jIStatus_internal == "APPR"):
        
       
        if (isBlank(mbo.getString("lbl_requestedby")) == True):
            setError("lbl_requestedbynull","PR"," ")
                   
    
            
            
        
        
        
