#######################################################
# Purpose: Script for intercepting the inbound traffic
#          for performing extra business processing
#
# Author : Pankaj Bhide
#
# Date    : April 5, 2018    
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


def afterMboData(ctx):
    
    
    if (ctx.getMbo().getString("lbl_npdisabled")=="true"):
        ctx.getMbo().setValue("disabled",True)
    else:
        ctx.getMbo().setValue("disabled",False)
         
    if (ctx.getMbo().getString("gisparam1")=="B"):
         ctx.getMbo().setValue("hasparent",True)
         ctx.getMbo().setValue("haschildren",True)
         
    if (ctx.getMbo().getString("gisparam1")=="F"):
         ctx.getMbo().setValue("hasparent",True)
         ctx.getMbo().setValue("haschildren",True)
             
    if (ctx.getMbo().getString("gisparam1")=="R"):
         ctx.getMbo().setValue("hasparent",True)
         ctx.getMbo().setValue("haschildren",False)