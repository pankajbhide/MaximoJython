#######################################################################
# Purpose: Script for object level  launch LBL_OBS_LBLSPCRHEDIST
#
# Author : Pankaj Bhide
#
# Date    : Sept 25 , 2015
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

boolError=False
    
if (onadd == True or onupdate == True):
    
    if (mbo.getOwner() is not None):
    
        boolDisabled=mbo.getOwner().getBoolean("disabled")
        strChargeable=mbo.getOwner().getString("gisparam2")
        
        if (boolDisabled==True or strChargeable=="N"):
            setError("lbl_inactiveroom","lbl_sp_charge_dist","")  
            boolError=True
        
        # Validate that the total percent should be = 100 
        dblTotalPercent=0.0    
        thisSet=mbo.getThisMboSet()
        intCount=thisSet.count()
        
        for i in xrange(intCount):
                
                if (thisSet.getMbo(i).toBeDeleted() == False):
                
                    if (isBlank(thisSet.getMbo(i).getString("proj_act_id")) == True):
                        setError("lbl_projactidisnull","financial","")  
                        boolError=True
                        
                    if (boolError==False):
                        while True:
                            try:
                                num = float(thisSet.getMbo(i).getDouble("CHARGED_TO_PERCENT") or '')
                                break
                            except ValueError:
                                setError("lbl_invalidchargedtopercent","lbl_sp_charge_dist"," ")
                                boolError=True
                                  
                    
                if (boolError==False):             
                            
                    if (thisSet.getMbo(i).toBeDeleted() == False):
                        dblTotalPercent = dblTotalPercent + thisSet.getMbo(i).getDouble("charged_to_percent")
                                        
        if (boolError==False and dblTotalPercent != 100.0):
            setError("lbl_totalpercentnot100","lbl_sp_charge_dist","")  
            boolError=True
                       
           
        
    if (boolError == False):
        
            
        maximo = MXServer.getMXServer()
        mbo.setValue("changedate",maximo.getDate(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        mbo.setValue("changeby"  ,user, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        
      
        if (mbo.getOwner() is not None):
             
            if (onadd == True):                                                 
                 mbo.setValue("building_number", mbo.getOwner().getString("lo1"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                 mbo.setValue("floor_number",    mbo.getOwner().getString("lo2"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                 mbo.setValue("room_number",     mbo.getOwner().getString("lo3"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                 mbo.setValue("location",        mbo.getOwner().getString("location"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                 mbo.setValue("orgid",           mbo.getOwner().getString("orgid"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                 mbo.setValue("siteid",          mbo.getOwner().getString("siteid"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            strDivisioncomments=mbo.getOwner().getString("lo15")
            mbo.getOwner().setValue("lo15",strDivisioncomments, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             
            strOrglevel2=mbo.getOwner().getString("lo8")
            mbo.getOwner().setValue("lo8",strOrglevel2,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
               
            strOrglevel3=mbo.getOwner().getString("lo9")
            mbo.getOwner().setValue("lo9",strOrglevel3, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
               
            strOrglevel4=mbo.getOwner().getString("lo10")
            mbo.getOwner().setValue("lo10",strOrglevel4, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)                     
                             
                             
            mbo.getOwner().setValue("changedate",maximo.getDate(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.getOwner().setValue("changeby"  ,user, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                             
        