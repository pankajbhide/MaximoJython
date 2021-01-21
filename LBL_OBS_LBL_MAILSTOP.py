################################################################
# Purpose: Script for object level (save) launch for lbl_mailstop
#          
# Author : Pankaj Bhide
#
# Date    : August 26, 2015
#
# Revision
# History : 
#
#################################################################

from psdi.mbo import MboRemote
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

boolError=False

logger = mbo.getMboLogger()

# Validations before saving the contents of the record 
if (ondelete == False):
    
    
    
   
    #global emailSubject, emailFrom, emailTo, emailCc, emailBcc, emailBody, emailSmtp
    #ctx2=HashMap()
    #ctx2.put("emailSubject","TESTING MAIL THROUGH jython")
    #ctx2.put("emailFrom","PBhide@lbl.gov")
    #ctx2.put("emailTo","PBhide@lbl.gov")
    #ctx2.put("emailBody","<HTML><BODY><BR>This is test email</BODY></HTML>")
    #ctx2.put("emailSmtp","smtp.lbl.gov")
    #service.invokeScript("LBL_LIB_SENDEMAIL", ctx2)
        
    
    if (isBlank(mbo.getString("mailstopid"))== True):
        setError("lbl_mailstopidnull","lbl_mailstop","")
        boolError=True
        
        
    if (onadd == True):
        
        # Check whether mail stop already exists
        mailstopSet = MXServer.getMXServer().getMboSet("lbl_mailstop", mbo.getUserInfo())       
        strWhere = "mailstopid='" + mbo.getString("mailstopid") + "'"
                    
        mailstopSet.setUserWhere(strWhere)
        if (not mailstopSet.isEmpty()):
            setError("lbl_mailstopnonunique","lbl_mailstop"," ")
            boolError=True
           
        mailstopSet=None 
        
    if (boolError==False):
            
        if (isBlank(mbo.getString("building_number"))== True):
            setError("lbl_bldgnull","lbl_mailstop","")
            boolError=True
            
    if (boolError==False):
        bldgSet= MXServer.getMXServer().getMboSet("locations", mbo.getUserInfo())
        bldgSet.setUserWhere("location='" + mbo.getString("building_number") + "' and gisparam1='B'")
        if ( bldgSet.isEmpty()):
              setError("lbl_bldgnull","lbl_mailstop","")
              boolError=True
        bldgSet=None
            
    if (boolError==False):
        if (isBlank(mbo.getString("floor_number")) == True):
            setError("lbl_floornull","lbl_mailstop","")
            boolError=True
            
    if (boolError==False):
        floorSet= MXServer.getMXServer().getMboSet("locations", mbo.getUserInfo())
        floorSet.setUserWhere("lo1='" + mbo.getString("building_number") + "' and lo2='" + mbo.getString("floor_number")  +  "' and gisparam1='F'")
        if ( floorSet.isEmpty()):
              setError("lbl_floornull","lbl_mailstop","")
              boolError=True
        floorSet=None
            
    if (boolError==False):
        if (isBlank(mbo.getString("description")) == True):
            setError("lbl_descriptionnull","lbl_mailstop","")
            boolError=True
            
    if (boolError==False):    
        if (isBlank(mbo.getString("zip"))== True):
            setError("lbl_zipnull","lbl_mailstop","")
            boolError=True
            
    if (boolError==False):    
        if (len(mbo.getString("zip")) != 5):
            setError("lbl_invalidzip","lbl_mailstop","")
            boolError=True
            
    if (boolError==False):    
        if (mbo.getString("zip").isdigit() == False):
            setError("lbl_invalidzip","lbl_mailstop","")
            boolError=True
                      
        
    maximo = MXServer.getMXServer()
    jOChangedate= maximo.getDate()
    jOChangeby = user  # variable provided by scripting framework
    jOOrgid="LBNL"
    jOSiteid="FAC"

    #print "PRB name of MXSever: " + maximo.getName()
    
    
    
    
   