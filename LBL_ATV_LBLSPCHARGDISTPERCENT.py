############################################################
# Purpose: Script for attribute level launch of
#          lbl_sp_charge_dist.charged_to_percent
#
# Author : Pankaj Bhide
#
# Date    : Sept 25, 2015
#
# Revision
# History : 
#
######################################################


from psdi.server import MXServer
from psdi.util import MXApplicationException
from java.util import Date
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

if (ondelete==False):
    if (jICharged_to_percent <=0):
          setError("lbl_invalidchargedtopercent","lbl_sp_charge_dist", " ")
    
        
   