#######################################################
# Purpose: Script for object level before save launch 
#
# Author : Pankaj Bhide
#
# Date    : Aug 22, 2015
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

if (jIOrgid=="LBNL" and jISiteid=="FAC" and  ondelete == False):
    
    #mbo.getOwner().getName()=="LOCATIONS"):
    boolError=False
    
    # Do not allow adding/modifying records is walk through is missing
    if (mbo.getName()== "LBL_WOWKTHRUOPS" or mbo.getName()== "LBL_WOWKTHRURES"):
        
        if (mbo.getOwner() is not None):                      
            if (isBlank(mbo.getOwner().getString("lbl_wkthruid")) == True):
                setError("lbl_wkthrublank","lbl_wkthru","")
                boolError=True               
                
    
    ########################
    if (mbo.getName()== "LBL_WKTHRUFEEDBK" or mbo.getName()== "LBL_WOWKTHRUFEEDBK"):
        if (isBlank(mbo.getString("personid")) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru","")
            boolError=True
    ########################        
    if (mbo.getName()== "LBL_WKTHRUHAZ" or mbo.getName()== "LBL_WOWKTHRUHAZ"):
        if (isBlank(mbo.getString("hazardid")) == True):
            setError("lbl_wkthruhazardnotnull","lbl_wkthruops","")
            boolError=True
    ########################        
    if (mbo.getName()== "LBL_WKTHRUMAT" or mbo.getName()== "LBL_WOWKTHRUMAT"):
        
        if (isBlank(mbo.getString("itemnum")) == True):
            setError("lbl_wkthruitemnotnull","lbl_wkthruops","")
            boolError=True
            
        if (mbo.getFloat("quantity") <= 0) :
            setError("lbl_wkthruitemqty>0","lbl_wkthruops","")
            boolError=True
          
    ########################        
    if (mbo.getName()== "LBL_WKTHRUOPS" or mbo.getName()== "LBL_WOWKTHRUOPS"):
        
        if (mbo.getInt("opsequence") <=0):
            setError("lbl_wkthruopsseq>0","lbl_wkthruops","")
            boolError=True
            
        if (isBlank(mbo.getString("description")) == True):
            setError("lbl_wkthruopsdescnotnull","lbl_wkthruops","")
            boolError=True
    
        if (mbo.getFloat("opduration") <= 0) :
            setError("lbl_wkthruopduration>0","lbl_wkthruops","")
            boolError=True
    ########################   
         
    if (mbo.getName()== "LBL_WKTHRU" or mbo.getName()== "LBL_WOWKTHRU"):
        
        if (isBlank(mbo.getString("description")) == True):
            setError("lbl_wkthrudescnotnull","lbl_wkthruops","")
            boolError=True
                    
    ########################           
    if (mbo.getName()== "LBL_WCDSUBCOND"):
               
        if (mbo.getOwner() is not None):
            if (mbo.getOwner().getBoolean("hassubcondition") == False):
                setError("lblsubcondnotallowed", "workorder","")
                boolError=True
                
                              
            
            if (boolError==False):
                mbo.setValue("conditionnum", mbo.getOwner().getInt("conditionnum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                mbo.setValue("wcd_level",    mbo.getOwner().getInt("wcd_level"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    ########################  
    if (mbo.getName()== "LBL_WCDCONDITION"):
        
        if (mbo.getInt("conditionnum") <=0):
            setError("lbl_field<=0","workorder","Condition number")
            boolError=True
            
        if (isBlank(mbo.getString("description")) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
        
        if (mbo.getInt("yespoint") <=0 and mbo.getInt("nopoint") <=0 and mbo.getInt("unknownpoint") <=0 ) :
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
       
        if (mbo.getInt("wcd_level") <= 0):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
            
        if (boolError == False):
        
            if (onadd==True):
                 
                 # Check whether condition exists or not 
                strWhere1  = "orgid='LBNL' and siteid='FAC' and conditionnum=" +  str(mbo.getInt("Conditionnum"))
                lbl_wcdconditionSet= MXServer.getMXServer().getMboSet("lbl_wcdcondition", mbo.getUserInfo())
                lbl_wcdconditionSet.setUserWhere(strWhere1)
               
                if (not lbl_wcdconditionSet.isEmpty()):  # Don't use count method
                      setError("lbl_wcdcondexists","lbl_wcdcondition","")
                      boolError=True
                lbl_wcdconditionSet= None
                
            #intWcdlevel= mbo.getInt("wcd_level")      
            #strWhere1  = "orgid='LBNL' and siteid='FAC' and conditionnum=" +  str(mbo.getInt("Conditionnum"))
            #lbl_wcdsubconditionSet=MXServer.getMXServer().getMboSet("LBL_WCDSUBCOND", mbo.getUserInfo())
            #lbl_wcdsubconditionSet.setUserWhere(strWhere1)
            
            #if (not lbl_wcdsubconditionSet.isEmpty()): 
                                                                    
                   #intCount=lbl_wcdsubconditionSet.count()
                                                        
                   #for i in xrange(intCount): 
                       #
                       #thismbo=lbl_wcdsubconditionSet.getMbo(i)                           
                       #thismbo.setValue("wcd_level", intWcdlevel, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                       #thismbo.setValue("wcd_level", intWcdlevel, MboConstants.NOACCESSCHECK)

                       
    ######################## 
    if (mbo.getName()== "LBL_WCDCATEGORY"):
        
        if (isBlank(mbo.getString("Lbl_wcdcategory")) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True

        if (isBlank(mbo.getString("description")) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
        
        if (mbo.getInt("min_totalpoints") <=0 and mbo.getInt("Max_totalpoints") <=0) :
            setError("lbl_field<=0","workorder","Mininum/Maximum points")
            boolError=True
            
        if (mbo.getInt("min_totalpoints") >= mbo.getInt("Max_totalpoints")) :
            setError("lbl_badminmaxpoints","workorder","Mininum/Maximum points")
            boolError=True
           
        if (mbo.getInt("wcd_level") <= 0):
            setError("lbl_field<=0","workorder"," WCD Level")
            boolError=True
            
    ######## Every thing is validated ################    
    if (boolError == False):
        
        ######################################################################
        # Sync walk through hazards with work order hazard collection in case
        # of saving into LBL_WOWKHHRUHAZ 
        ######################################################################
        if (mbo.getName()== "LBL_WOWKTHRUHAZ"): 
            owner=mbo.getOwner()
            if (onadd == True):
                owner.wpc_sync_wohazards(owner,mbo, mbo.getString("hazardid"),"ADD")
            
                
        
        if (mbo.getName()== "LBL_WOWKTHRUHAZ"): 
            if (ondelete == True):
                #service.log("PRB on delete fired")
                owner=mbo.getOwner()
                owner.wpc_sync_wohazards(owner,mbo, mbo.getString("hazardid"),"DELETE_WOWKTHRU")   
                                  
                        
        # Common for all mbos    
        maximo = MXServer.getMXServer()
        mbo.setValue("changedate", maximo.getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        mbo.setValue("changeby",   user,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            