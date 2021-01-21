############################################################
# Purpose: Script for checking whether comments are recorded
#          before the work order status can be changed
#
# Author : Pankaj Bhide
#
# Date    : Feb 8, 2017
#
# Revision
# History : 
#
######################################################


from psdi.server import MXServer
from psdi.util import MXApplicationException
from psdi.mbo import Mbo
from psdi.mbo import MboSet
from psdi.mbo import MboConstants

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

if (jIOStatus=="CAN" or jIOStatus=="INFO" or jIOStatus=="HOLD"):
    jIOMemo_required = True   
    
