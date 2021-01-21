#######################################################################
# Purpose: Script for object level  launch LBL_AUTH_RELEASE
#
# Author : Pankaj Bhide
#
# Date    : Aug 19, 2015
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


if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
    if (onadd == True or onupdate == True):
            
        maximo = MXServer.getMXServer()
        jOChangedate= maximo.getDate()
        jOChangeby = user  # variable provided by scripting framework
        
    if (ondelete == True):
            
            # Before deleting, find out whether there are any pending work orders that have
            # open (passed approval). If find, then, display error message
            boolError=False
            strWhere1  = "orgid='LBNL' and siteid='FAC' and status='WREL'  and location='" + mbo.getString("location") + "'"
            strWhere1 +=" and worktype not in (select a.worktype from worktype a where a.lbl_rel_reqd is not null and a.lbl_rel_reqd='N') "
            workordersSet= MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())
            workordersSet.setUserWhere(strWhere1)
            if (not workordersSet.isEmpty()):  # Don't use count method
                     setError("lbl_woopenforyes","lbl_auth_release","")   
                     boolError=True     
            workordersSet=None  
                 
            if (boolError==False):
                
                # if the row needs to be deleted, then, there needs to be at-least one
                # active authorizer present 
                if (mbo.getOwner() is not None and mbo.getOwner().getName()=="LOCATIONS"):
                    strRelReqd=mbo.getOwner().getString("lbl_rel_reqd")
                    if(isBlank(strRelReqd) == False and strRelReqd=="Y"):
                        thisSet=mbo.getThisMboSet()
                        intCount=thisSet.count()
                        intAuthcount=0
                        for i in xrange(intCount):
        
                              thisRow = thisSet.getMbo(i)
                              if (thisRow.toBeDeleted() == False):        
                                  if (isBlank(thisRow.getString("personid")) == False):
                                                                                                                          
                                      intAuthcount=intAuthcount +1
                                  
                        if (intAuthcount ==0):
                            setError("lbl_authreqd","lbl_auth_release"," ")
                        thisSet=None    
                          
   