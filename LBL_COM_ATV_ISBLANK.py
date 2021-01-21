############################################################
# Purpose: Script for checking whether input field is blank.
#  
#
# Author : Pankaj Bhide
#
# Date    : July 20, 2015
#
# Revision
# History : 
#
######################################################


from psdi.server import MXServer
from psdi.util import MXApplicationException
from psdi.mbo import Mbo
from psdi.mbo import MboSet
from java.util import HashMap
from array import array

logger = mbo.getMboLogger()

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def setError():
    ctx = HashMap()
    ctx.put("paramErrorkey","lbl_fieldnotblank")
    ctx.put("paramErrorgroup","workorder")
         
    ctx.put("paramParams",jIInputfieldname)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
    
def setError3():
    ctx = HashMap()
    ctx.put("paramErrorkey","lbl_field<=0")
    ctx.put("paramErrorgroup","workorder")
         
    ctx.put("paramParams",jIInputfieldname)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
    
def setError2(errkey,errgroup, errparm):
    global errorkey,errorgroup,params
    errorkey=errkey
    errorgroup=errgroup
    params=[errparm]
 

boolError=False

if ( jIInputfieldvalue is None):
    boolError=True
    setError()
    
if (jIInputfieldtype=="STRING"):
        
    if ( isBlank(jIInputfieldvalue) == True):
        boolError=True
        setError()
        
if (jIInputfieldtype=="NUMBER"):
    while True:
           try:
               num = int(jIInputfieldvalue or '')
               if (num <= 0):
                   boolError=True
                   setError3()                   
               break
           except ValueError:
             boolError=True
             setError()

if (boolError == False):
    
    #logger = mbo.getMboLogger()   
    #logger.info("PRB  launchpoint: " + launchPoint)
    
                  
    if (mbo.getName()=="WORKORDER"):
        
        if (launchPoint=="LBL_ATV_WOREPORTEDBY"):
             # Check whether the value entered is valid
             # Get reference to person collection
             personSet = MXServer.getMXServer().getMboSet("PERSON", mbo.getUserInfo())       
             strWhere = "personid='" + mbo.getString("reportedby") + "'"
             
             personSet.setUserWhere(strWhere)
             if (personSet.isEmpty()):
                 boolError=True                                  
                 setError2("lbl_InvalidPerson","workorder","for work order: " +mbo.getString("wonum"))
             personSet = None
               
        
            
      