##########################################################################
# Purpose: Script for attribute level launch lbl_auth_release.personid
#
# Author : Pankaj Bhide
#
# Date    : April 23, 2015
#
# Revision
# History : 
#
############################################################################


from psdi.server import MXServer
from psdi.util import MXApplicationException
from psdi.mbo import Mbo
from psdi.mbo import MboSet
from java.util import HashMap


def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams",errparm)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)

   
if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
    if ( ondelete == False):
        
         
        boolError=False
               
        thisSet=mbo.getThisMboSet()
        intCount=thisSet.count()
       
           
        # Check for the uniqueness of personid    
        if (onadd==True):
           intCount=intCount-1
                         
        for i in xrange(intCount):
            
            thisRow = thisSet.getMbo(i)
          
            if (thisRow.getString("personid") == mbo.getString("personid")): 
                setError("lbl_duplicateperson_id","lbl_auth_release"," ")
                boolError=True
                
       # The status of the person id should be active
        if (boolError==False):
            strWhere1  = "personid='" + mbo.getString("personid") + "' and lbl_status='A'"
           
            personSet= MXServer.getMXServer().getMboSet("PERSON", mbo.getUserInfo())
            personSet.setUserWhere(strWhere1)

          
            if (personSet.isEmpty()):  # Don't use count method
                setError("lbl_invalidpersonid","lbl_auth_release"," ")

            personSet=None
        
                
        
       
                