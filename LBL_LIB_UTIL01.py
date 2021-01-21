#############################################
# Purpose: Library of methods used in scripts 
#
# Author : Pankaj Bhide
#
# Date    : July 10, 2015
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


def setError(errkey,errgroup, errparm):
    global errorkey,errorgroup,params
    errorkey=errkey
    errorgroup=errgroup
    params=[errparm]
    
def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return '0'
    #myString is None OR myString is empty or blank
    return '1'