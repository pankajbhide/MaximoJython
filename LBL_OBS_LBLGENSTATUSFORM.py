###########################################################################
# Purpose: Object level (save) on 
#
# Author : Pankaj Bhide
#
# Date    : 
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
assetSetRemote= MXServer.getMXServer().getMboSet("ASSET",  mbo.getUserInfo())

if (onadd == True):
    
    # FOR PSPS change asset status from new record
    strAssetStatus=mbo.getMboValue("status").getCurrentValue().asString()
        
    if (isBlank(strAssetStatus)== False and isBlank(mbo.getString("assetnum")== False)):
        
           
                    assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + mbo.getString("assetnum") + "'")
                    assetSetRemote.reset()             
                    if (not assetSetRemote.isEmpty()):
                        assetSet=assetSetRemote.getMbo(0)
                        if (assetSet.getString("status") != strAssetStatus):
                            assetSet.changeStatus(strAssetStatus, False, False, False, False) # rollToAllChildren, removeFromActiveRoutes, removeFromActiveSP,changePMStatus
                            assetSetRemote.save()
                        assetSetRemote=None
    