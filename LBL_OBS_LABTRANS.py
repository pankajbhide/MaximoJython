###############################################################
# Purpose: Script for object  level (save) launch 
#          on LABTRANS
#
# Author : Pankaj Bhide
#
# Date    : August 31, 2015
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


if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
 
    owner=mbo.getOwner()
    
    if (owner is not None and owner.getName() =="WORKORDER"):   
        mbo.setValue("lt1", "Y", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        mbo.setValue("genapprservreceipt", 1, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION) 
       