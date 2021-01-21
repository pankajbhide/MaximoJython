##########################################################################
# Purpose: Script to init level launch on WPLabor

# Author : Pankaj Bhide
#
# Date    : Jul 3, 2018
#
# Revision
# History : 
#
######################################################
from java.util import Calendar
from java.util import Date
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

if (onadd==True):
    
    mbo.setValue("quantity", 0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)     