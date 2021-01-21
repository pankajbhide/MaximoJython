####################################################
# Purpose: Attribute action launch on asset.location
#
# Author : Pankaj Bhide
#
# Date    : Jul 30 2019
#
# Revision
# History : 
######################################################

from psdi.server import MXServer
from psdi.mbo  import   MboConstants

from java.util import HashMap



def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True



logger = mbo.getMboLogger()
ctx = HashMap()
ctx.put("mbo",mbo)

if ( mbo.getString("orgid") == 'LBNL' and mbo.getString("siteid") == 'FAC'):
    
    if (isBlank(mbo.getString("location") == False)):
        locationsSet = MXServer.getMXServer().getMboSet("LOCATIONS", mbo.getUserInfo())
        strWhere = "location='" + mbo.getString("location") + "'"
        locationsSet.setUserWhere(strWhere)
        if (not  locationsSet.isEmpty()):
                mbo.setValue("lbl_building", locationsSet.getMbo(0).getString("lo1"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        locationsSet = None
        strWhere = None