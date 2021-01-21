#######################################################
# Purpose: Script for object level before save launch
#          for lasers 
#
# Author : Pankaj Bhide
#
# Date    : May 13 2016
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

if (ondelete == False):
        
    boolError=False
    
    ########################        
    if (mbo.getName()== "LBL_LASERWAVE"):
        
        floatvar=mbo.getFloat("wavelength")
        while True:
           try:
               wavelength = float(floatvar or '' or 0)
               break
           except ValueError:
                wavelength=0
                
        floatvar=mbo.getFloat("wavelength_min")
        while True:
           try:
               wavelengthmin = float(floatvar or '' or 0)
               break
           except ValueError:
                wavelengthmin=0    
                
        floatvar=mbo.getFloat("wavelength_max")
        while True:
           try:
               wavelengthmax = float(floatvar or '' or 0)
               break
           except ValueError:
                wavelengthmax=0    
        
        if (wavelength==0 and wavelengthmin==0 and wavelengthmax==0):
                
            setError("lbl_wavelengthreqd","lbl_laser","")            
            boolError=True
       
        
           
        if (wavelengthmin > wavelengthmax):
            setError("lbl_wavelengminmaxerror","lbl_laser","")            
            boolError=True
        
        floatvar=mbo.getFloat("max_power")
        while True:
           try:
               maxpower = float(floatvar or '' or 0)
               break
           except ValueError:
                maxpower=0    
        
        if (maxpower<=0):
            setError("lbl_maxpowerreqd","lbl_laser","")            
            boolError=True
        
        #if (isBlank(mbo.getString("max_power_uom")) == True):
        #    setError("lbl_maxpoweruomreqd","lbl_laser","")            
        #    boolError=True
        
            
        if (isBlank(mbo.getString("wavetype")) == True):
            setError("lbl_wavetypeblank","lbl_laser","")            
            boolError=True
                
                
            
                    
    if (boolError == False):
        #owner=mbo.getOwner()
        #if (mbo.getName()== "LBL_LASERHIST"):
        #    mbo.setValue("assetnum", owner.getString("assetnum"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)        
        # Common for all mbos    
        maximo = MXServer.getMXServer()
        mbo.setValue("changedate", maximo.getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        mbo.setValue("changeby",   user,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        
        
                  