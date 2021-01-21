############################################################
# Purpose: Script for checking whether proj_act_id is 
#          duplicated or not
#
# Author : Pankaj Bhide
#
# Date    : Sept  24, 2015
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
from psdi.mbo  import   MboConstants

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

boolError=False

if (ondelete == False):
    
        if (isBlank(jIProj_act_id)==True):
             ctx = HashMap()
             ctx.put("paramErrorkey","lbl_projactidisnull")
             ctx.put("paramErrorgroup","financial")
             ctx.put("paramParams","")
             service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
             boolError=True
                    
        if (boolError==False):
                       
            thisSet=mbo.getThisMboSet()
            intCount=thisSet.count()
                
            # Create an empty list and append all project_id and activity id into the list        
            myList = []        
            for i in xrange(intCount):
                
                thisRow = thisSet.getMbo(i)
                myList.append(thisRow.getString("proj_act_id"))
                
            
            # If the length of the list and length lists set (unique) is equal
            # then there are no duplicates.   
            if len(myList)!=len(set(myList)):                         
                      thisSet = None
                      ctx = HashMap()
                      ctx.put("paramErrorkey","lbl_duplicateproject_id")
                      ctx.put("paramErrorgroup","lbl_sp_charge_dist")
                      ctx.put("paramParams","")
                      service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
                      
           