################################################################
# Purpose: Script for object level (save) launch for routes
#          
# Author : Pankaj Bhide
#
# Date    : Aug 14 2019
#
# Revision
# History : 
#
#################################################################

from psdi.mbo import MboRemote
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

boolError=False

logger = mbo.getMboLogger()

# Validations before saving the contents of the record 
if (ondelete == False and mbo.getString("lbl_routetype")=="FEG"):
    
 
    if (
        isBlank(mbo.getString("route"))  == True      or 
        isBlank(mbo.getString("description")) == True      or
        isBlank(mbo.getString("lbl_feg_system"))== True or 
        isBlank(mbo.getString("lbl_feg_status"))== True or 
        isBlank(mbo.getString("lbl_feg_type"))== True   
        ):
          
        
        setError("lbl_fegrequed","route","")

