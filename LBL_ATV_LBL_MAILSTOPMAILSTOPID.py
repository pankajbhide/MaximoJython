############################################################
# Purpose: Script for attribute level launch of
#          lbl_mailstop.mailstopid
#
# Author : Pankaj Bhide
#
# Date    : August 26, 2015
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

if (onadd==True):
    
    if (isBlank(mbo.getString("mailstopid")) == True):
        setError("lbl_mailstopidnull","lbl_mailstop"," ")
        boolError=True
        
    if (boolError==False):
        
                 
           # Check whether mail stop already exists
           mailstopSet = MXServer.getMXServer().getMboSet("lbl_mailstop", mbo.getUserInfo())       
           strWhere = "mailstopid='" + mbo.getString("mailstopid") + "'"
                    
           mailstopSet.setUserWhere(strWhere)
           if (not mailstopSet.isEmpty()):
               setError("lbl_mailstopnonunique","lbl_mailstop"," ")
           
           mailstopSet=None    
           