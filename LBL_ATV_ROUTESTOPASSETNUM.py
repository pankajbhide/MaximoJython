############################################################
# Purpose: Script for attribute level launch of
#          lbl_sp_charge_dist.charged_to_percent
#
# Author : Pankaj Bhide
#
# Date    : Sept 25, 2015
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

if (ondelete==False):
    
    if (mbo.getOwner() is not None):
    
        strRoutetype=mbo.getOwner().getString("lbl_routetype")
        if (strRoutetype=="FEG" and interactive==True and app=="LBLFEG"):
            
            strWhere1  = " orgid='LBNL' and siteid='FAC' and route='" + mbo.getString("route") + "' and assetnum='" + mbo.getString("assetnum") + "'"
            routestopSet = MXServer.getMXServer().getMboSet("route_stop", mbo.getUserInfo())
            routestopSet.setUserWhere(strWhere1)
            if (not routestopSet.isEmpty()):
                setError("lbl_assetuniqueroutestop","route"," ")
            routestopSet=None
            
            thisSet=mbo.getThisMboSet()
            intCount=thisSet.count()-1
                
            for i in xrange(intCount):
                        
                if (thisSet.getMbo(i).toBeDeleted() == False):
                    if (thisSet.getMbo(i).getString("assetnum")==mbo.getString("assetnum")):
                        setError("lbl_assetuniqueroutestop","route"," ")
                    
                
                              
    
        
   