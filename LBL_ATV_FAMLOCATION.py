############################################################
# Purpose: Script for checking whether location  is 
#          duplicated or not
#
# Author : Pankaj Bhide
#
# Date    : June 28 2016
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

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

boolError=False

if (ondelete == False):
    
        
    if (isBlank(mbo.getString("location")) == True):
        
         ctx = HashMap()
         ctx.put("paramErrorkey","lbl_famlocationisnull")
         ctx.put("paramErrorgroup","lbl_fam")
         ctx.put("paramParams","")
         service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
         boolError=True
                

    
    else:
        
                  
        thisSet=mbo.getThisMboSet()
        intCount=thisSet.count()
            
        # Create an empty list and append all manager id into the list        
        myList = []        
        for i in xrange(intCount):
            if (thisSet.getMbo(i).toBeDeleted() == False):
                thisRow = thisSet.getMbo(i)
                myList.append(thisRow.getString("location"))
            
        
        # If the length of the list and length lists set (unique) is equal
        # then there are no duplicates.   
        if len(myList)!=len(set(myList)):                         
                  thisSet = None
                  ctx = HashMap()
                  ctx.put("paramErrorkey","lbl_duplicatefamloc")
                  ctx.put("paramErrorgroup","lbl_fam")
                  ctx.put("paramParams","")
                  service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
                  
        #Building should be unique across all FAMS
        buildingSet = MXServer.getMXServer().getMboSet("LBL_FAMLOCATION", mbo.getUserInfo())       
        strWhere = "location='" + mbo.getString("location") + "'" 
                        
        buildingSet.setUserWhere(strWhere)
        if (not  buildingSet.isEmpty()):
            ctx = HashMap()
            ctx.put("paramErrorkey","lbl_famlocexists")
            ctx.put("paramErrorgroup","lbl_fam")
            ctx.put("paramParams","")
            service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
                
            buildingSet = None
            strWhere = None  
            
            boolError=True        
       