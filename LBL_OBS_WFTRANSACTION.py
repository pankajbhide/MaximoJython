##################################################################
# Purpose: Script for checking whether memo contents are recorded
#          before the FAM decides canceling work order
#
# Author : Pankaj Bhide
#
# Date    : Feb 13, 2017
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

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams",errparm)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
    
boolError=False
if (mbo.getString("actionperformed")=='FAAGWOCAN' or mbo.getString("actionperformed")=='FAAGINFO'):
        
    if (isBlank(mbo.getString("memo")) == True):
        setError("lbl_memoblank","wftransaction","")
        boolError=True  
     
if (boolError==False and mbo.getString("actionperformed")=='FAAGWPLANSUP' and mbo.getString("nodetype")=='WFINPUT' and mbo.getString("processname") != 'FAEXPEDITE'):
        
    if (isBlank(mbo.getString("memo")) == True):
        setError("lbl_memoblank","wftransaction","")
         
if (boolError==False and mbo.getString("actionperformed")=='FAAGPLAN' and mbo.getString("nodetype")=='WFINPUT' and mbo.getString("processname") == 'FASCHEDULE'):
        
    if (isBlank(mbo.getString("memo")) == True):
        setError("lbl_memoblank","wftransaction","")
        
    