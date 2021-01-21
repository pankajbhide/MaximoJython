###############################################################
# Purpose: Script for object  level (save) launch 
#          on PM
#
# Author : Pankaj Bhide
#
# Date    : Nov 17, 2015
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
    
 
    if (onadd == True):
        jIOWostatus="WAPPR"
        