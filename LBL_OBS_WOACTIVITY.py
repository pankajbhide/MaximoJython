###############################################################
# Purpose: Script for object level launch for woactivity
#          (before save)
# 
# Author : Pankaj Bhide
#
# Date    : August 13, 2015
#
# Revision
# History : 
#
######################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

logger = mbo.getMboLogger()
ctx = HashMap()
ctx.put("mbo",mbo)  

# Inherit the values of Supervisor,Glaccount from the parent if not already specified

if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
   
    if (mbo.getString("status") !="CLOSE" and mbo.getString("status") !="CAN"):
       
       
        if (mbo.isNew() == True):
            # Release status is always not required for task work orders 
            if (isBlank(mbo.getString("lbl_release_status"))== True):
                  mbo.setValue("lbl_release_status", "NOT REQUIRED",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                
          
                        
        if (isBlank(mbo.getString("parent")) == False ):
                        
            
            parentWoSet=mbo.getMboSet("parent")
            if (not parentWoSet.isEmpty()):
                 owner=parentWoSet.getMbo(0)
                                 
                # Release status is always not required for task work orders 
                 if (isBlank(mbo.getString("lbl_release_status"))== True):
                    mbo.setValue("lbl_release_status", "NOT REQUIRED",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                      
                  
                 if (isBlank(mbo.getString("supervisor")) == True):
                     mbo.setValue("supervisor", owner.getString("supervisor"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                        
                        
                 if (isBlank(mbo.getString("glaccount")) == True):
                     mbo.setValue("glaccount", owner.getString("glaccount"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
                        
                 if (isBlank(mbo.getString("wo5"))==True):
                     mbo.setValue("wo5", owner.getString("wo5"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    
                              
                 if (isBlank(mbo.getString("leadcraft"))== True):
                     mbo.setValue("leadcraft", owner.getString("leadcraft"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                   
                               
                
                 