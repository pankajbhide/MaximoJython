################################################################
# Purpose: Script for object level launch for setting values
#          for changeby and change date
#          (save) 
# Author : Pankaj Bhide
#
# Date    : August  21, 2015
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

# 
if (jIOrgid=="LBNL" and jISiteid=="FAC" and  ondelete == False):

    
        maximo = MXServer.getMXServer()
        jOChangedate= maximo.getDate()
        jOChangeby = user  # variable provided by scripting framework
        if (mbo.getOwner() is not None):
            mbo.setValue("conditionnum", mbo.getOwner().getInt("conditionnum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("wcd_level", mbo.getOwner().getInt("wcd_level"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        