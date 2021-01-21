########################################################################
# Purpose: Script for object level (init) launch LBL_AUTH_RELEASE
#
# Author : Pankaj Bhide
#
# Date    : Aug 19, 2015
#
# Revision
# History : 
#
######################################################

from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer

 # Set the value of various columns from the owner (locations)        
if (mbo.getOwner() is not None and mbo.getOwner().getName()=="LOCATIONS"):
    
    mbo.setValue("building_number", mbo.getOwner().getString("lo1"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("floor_number",    mbo.getOwner().getString("lo2"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("room_number",     mbo.getOwner().getString("lo3"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("Lbl_roof_level",  mbo.getOwner().getString("lbl_roof_level"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("location",        mbo.getOwner().getString("location"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("orgid",           mbo.getOwner().getString("orgid"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("siteid",          mbo.getOwner().getString("siteid"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)



    
    