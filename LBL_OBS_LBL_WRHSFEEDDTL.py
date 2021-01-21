################################################################
# Purpose: Script for object level (save) launch for LBL_WRHSFEEDDTL
#          
# Author : Pankaj Bhide
#
# Date    : July 23, 2015
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
from java.util import Date
from java.util import Calendar



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

if (ondelete == False):
  
    if (isBlank(jIProj_act_id)):
        setError("lbl_glaccountnull","workorder"," ")
        boolError=True
    
    if (boolError==False):
        
        if (isBlank(mbo.getString("vault_number"))==True):
        
            while True:
               try:
                   num = float(jISq_ft_used or '' or 0)
                   break
               except ValueError:
                    setError("lbl_invalidsqftused","lbl_wrhsfeed"," ")
                    boolError=True
                
            if (jISq_ft_used <=0):
                setError("lbl_invalidsqftused","lbl_wrhsfeed"," ")
                boolError=True
        
    if (boolError==False):
        
        
        while True:
           try:
               num = float(jIQuantity or '' or 0)
               break
           except ValueError:
                setError("lbl_invalidqty","lbl_wrhsfeed"," ")
                boolError=True 
                   
        if (jIQuantity <=0):
            setError("lbl_invalidqty","lbl_wrhsfeed"," ")
            boolError=True
        
    
    if (boolError==False):
                           
        if (jIDate_received is not None):
                          
               cal=Calendar.getInstance()                      
               todayDate=MXServer.getMXServer().getDate() # Current date
                          
               if (jIDate_received > todayDate):
                   setError("lbl_invaliddaterecd","lbl_wrhsfeed", " ")
                   boolError=True
                   
               
    
    if (boolError==False):
        if (jIDate_returned is not None and jIDate_received is not None):
                 
                   if (jIDate_returned < jIDate_received):
                        setError("lbl_invalid_dtreturn","lbl_wrhsfeed", " ")
                        boolError=True
                        
                   if (boolError==False):
                                         
                         strWhere   = " FINANCIALPERIOD=(SELECT MIN(C.FINANCIALPERIOD) FROM FINANCIALPERIODS C"
                         strWhere  +="  WHERE  (NVL(C.CLOSEDBY,' ') NOT LIKE '%STR%') AND C.ORGID='" + jIOOrgid +  "') "
                         financialperiodsSet= MXServer.getMXServer().getMboSet("FINANCIALPERIODS", mbo.getUserInfo())
                         financialperiodsSet.setUserWhere(strWhere)
                         if (financialperiodsSet.isEmpty()):
                              setError("lbl_invalid_dtreturn","lbl_wrhsfeed"," ")
                              boolError=True
                         if (boolError == False):
                             if (financialperiodsSet.getMbo(0).getDate("periodstart") > jIDate_returned):
                                 setError("lbl_invalid_dtreturn","lbl_wrhsfeed", " ")
                        
                         financialperiodsSet=None     
            
                        
            
    if (boolError == False):
        jIOOrgid="LBNL"
        jIOSiteid="FAC"
        jOFeeder_id="STR"  
        maximo = MXServer.getMXServer()
        jOChangedate= maximo.getDate()
        jOChangeby = user  
          

    
    
    
    