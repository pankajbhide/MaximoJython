################################################################
# Purpose: Script for object level launch for lbl_wrhsfeeddef
#
# Author : Pankaj Bhide
#
# Date    : July 22, 2015
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
from psdi.util import MXApplicationException
from java.util import HashMap

def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams","")
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
    
def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

boolError=False


if (isBlank(jIDef_proj_act_id) == True):
    setError("lbl_glaccountnull","workorder"," ")
    boolError=True
    
if (boolError==False):
        
    if (isBlank(jIDrop_proj_act_id) == True):
        setError("lbl_glaccountnull","workorder"," ")
        boolError=True    

if (boolError==False):
        
    if (jIRate_per_sqft <=0):
        setError("lbl_invalidrtsqft","lbl_wrhsfeed"," ")
        boolError=True
        
        
if (boolError==False):
        
    if (jIRate_per_vault <=0):
        setError("lbl_invalidrtpervault","lbl_wrhsfeed"," ")
        boolError=True
        
if (boolError==False):
        
    if (jIEffdt is None):
        setError("lbl_invalideffdt","lbl_wrhsfeed"," ")
        boolError=True
        
if (boolError==False):
        
    if (jIMin_days_recharge <=0):
        setError("lbl_invalidmindaysrecharge","lbl_wrhsfeed"," ")
        boolError=True
      
    
if (boolError == False):
    jOOrgid="LBNL"
    jOSiteid="FAC"
    jOFeeder_id="STR"  
    maximo = MXServer.getMXServer()
    jOChangedate= maximo.getDate()
    jOChangeby = user  
      
         