#######################################################
# Purpose: Script for object level before save launch
#          for lbl_fam table and its children MBOs 
#
# Author : Pankaj Bhide
#
# Date    : July 20  2016
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
logger = mbo.getMboLogger() 

if (ondelete==True and mbo.getName()== "LBL_FAM"):
    
    remoteSet= mbo.getMboSet("LBL_FAM2FAMLOC")
    if (not remoteSet.isEmpty()):
        remoteSet.deleteAll()
    
    mbo.delete()

if (ondelete == False):
        
    boolError=False
    
    ########################        
    if (mbo.getName()== "LBL_FAM"):
                
            
        if (isBlank(mbo.getString("famid")) == True):
            setError("lbl_famidblank","lbl_fam","")            
            boolError=True
        
        if (isBlank(mbo.getString("description")) == True):
            setError("lbl_famdescblank","lbl_fam","")            
            boolError=True
               
                       
             
    if (mbo.getName()== "LBL_FAMLOCATION"):
         if (isBlank(mbo.getString("location")) == True):
             setError("lbl_famlocationisnull","lbl_fam","")            
             boolError=True
                                                        
                    
    if (boolError == False):
        owner=mbo.getOwner()
        if (mbo.getName() != "LBL_FAM"):
        
            mbo.setValue("famid", owner.getString("famid"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    
        #Common for all mbos    
        maximo = MXServer.getMXServer()
        mbo.setValue("orgid",  "LBNL",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        mbo.setValue("siteid", "FAC",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        mbo.setValue("changedate", maximo.getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        mbo.setValue("changeby",   user,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        
        
                  