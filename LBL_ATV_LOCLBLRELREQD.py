###################################################################################
# Purpose: Script for attribute level launch LOCATION.LBL_REL_REQD
#
# Author : Pankaj Bhide
#
# Date    : April 10, 2015
#
# Revision
# History : July 29 PMuramalla
#               Updated setError Function to invoke common Error Function - LBL_LIB_SHOWERRORMSG
#
####################################################################################

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

if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
    boolError=False
    
    
    if (jILbl_rel_reqd_modified == True):
        
        # Received non-value
        if (isBlank(jILbl_rel_reqd) == False): 
            if (jILbl_rel_reqd != "Y" and jILbl_rel_reqd !="N"):
                boolError=True
                setError("lbl_invalidrelreqd","lbl_auth_release","")
                
        if (boolError != True):
            
           
            # Make sure that no work order exists against that
            # location whose status="WREL"      
            if (jILbl_rel_reqd == "N"):
                  strWhere1  = "orgid='LBNL' and siteid='FAC' and status='WREL'  and location='" + mbo.getString("location") + "'"
                  strWhere1 +=" and worktype not in (select a.worktype from worktype a where a.lbl_rel_reqd is not null and a.lbl_rel_reqd='N') "
                  workordersSet= MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())
                  workordersSet.setUserWhere(strWhere1)
                  if (not workordersSet.isEmpty()):  # Don't use count method
                        setError("lbl_woopenforyes","lbl_auth_release","")
                        
                  workordersSet=None  # Induce garbage collection
                  
            # Make sure at-least one active authorizer exists if release reqd=Y               
            if (jILbl_rel_reqd == "Y"):
                # Get authroizers using relationship 
                authSet=mbo.getMboSet("LBL_LOCATION2AUTH")
                if (authSet.isEmpty()):
                    setError("lbl_authreqd","lbl_auth_release","")
            
                authSet=None