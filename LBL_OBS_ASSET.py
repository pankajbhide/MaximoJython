################################################################
# Purpose: Script for object level (save) launch for asset
#          
# Author : Pankaj Bhide
#
# Date    : July 19, 2019
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
if (ondelete == False and app=="LBLMEL"):
    
 
    if (
        isBlank(mbo.getString("assettag"))  == True      or 
        isBlank(mbo.getString("ASSETTYPE")) == True      or
        isBlank(mbo.getString("LBL_ASSETSYSTEM"))== True or 
        isBlank(mbo.getString("LBL_UNITNUM"))== True     or
        isBlank(mbo.getString("LBL_BUILDING"))== True    or 
        isBlank(mbo.getString("assetnum"))== True
        ):
        
        
        
        setError("lbl_melcolsrequired","asset","")
        
    # Asset tag should be unique
    strPrevAssettag=mbo.getMboValue("ASSETTAG").getPreviousValue().asString()
    if (isBlank(strPrevAssettag) == True):
        strPrevAssettag="_"
        
    if (strPrevAssettag != mbo.getString("ASSETTAG")):               
        assetSet= MXServer.getMXServer().getMboSet("ASSET", mbo.getUserInfo())
        strWhere = "ASSETTAG='" + mbo.getString("ASSETTAG") + "'"
        assetSet.setUserWhere(strWhere)
        if (not  assetSet.isEmpty()):
            setError("lbl_assettagnotunique","asset","")
        
        
                
        assetSet = None
        strWhere = None        
        
        
        
    
    