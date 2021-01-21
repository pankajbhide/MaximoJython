####################################################
# Purpose: Common script for attribute level action
#          launch for auto numbers
#
# Author : Pankaj Bhide
#
# Date    : Sept 19 2017
#
# Revision
# History : 
######################################################

from psdi.server import MXServer
from psdi.mbo  import   MboConstants
from java.util import Date
from java.util import Calendar
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

if (onadd == True):
    
    if (jIFieldname=="HAZARDID"):
        
          
        if (len(mbo.getString("HAZARDID")) > 10):  
    
             prefix=mbo.getString("HAZARDID")[:3]  # get prefix
             suffix=mbo.getString("HAZARDID")[4:] # get unformatted suffix
                      
             temp=suffix.lstrip('0')
             suffix=temp.zfill(7) # prefix zeros
             
             # Associate formatted suffix to work order number
             temp1=prefix + "-" +  suffix
             mbo.setValue("HAZARDID", temp1,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             #Make it read-only
             mbo.setFieldFlag("HAZARDID", mbo.READONLY, 1)
             
    if (jIFieldname=="PRECAUTIONID"):
        
          
        if (len(mbo.getString("PRECAUTIONID")) > 10):  
    
             prefix=mbo.getString("PRECAUTIONID")[:3]  # get prefix
             suffix=mbo.getString("PRECAUTIONID")[4:] # get unformatted suffix
                      
             temp=suffix.lstrip('0')
             suffix=temp.zfill(7) # prefix zeros
             
             # Associate formatted suffix to work order number
             temp1=prefix + "-" + suffix
             mbo.setValue("PRECAUTIONID", temp1,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             #Make it read-only
             mbo.setFieldFlag("PRECAUTIONID", mbo.READONLY, 1)
    
    
    
    
    if (jIFieldname=="JPNUM"):
        
          
        if (len(mbo.getString("JPNUM")) > 10):  # JIRA EF-7087
    
             prefix=mbo.getString("JPNUM")[:2]  # get prefix
             suffix=mbo.getString("JPNUM")[3:] # get unformatted suffix
                      
             temp=suffix.lstrip('0')
             suffix=temp.zfill(8) # prefix zeros
             
             # Associate formatted suffix to work order number
             temp1=prefix + suffix
             mbo.setValue("JPNUM", temp1,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             #Make it read-only
             mbo.setFieldFlag("JPNUM", mbo.READONLY, 1)
             
       
    if (jIFieldname=="PMNUM"):
        
        if (len(mbo.getString("pmnum")) > 8):
    
             prefix=mbo.getString("pmnum")[:2]  # get prefix
             suffix=mbo.getString("pmnum")[3:] # get unformatted suffix
             # format suffix
             #temp1=str(int(suffix)) # convert to integer to get rid of zeros
             # Revised by Pankaj on 2/3/17 
             temp=suffix.lstrip('0')
             suffix=temp.zfill(8) # prefix zeros
    
             # Associate formatted suffix to work order number
             temp1=prefix + suffix
             mbo.setValue("pmnum", temp1,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             #Make it read-only
             mbo.setFieldFlag("pmnum", mbo.READONLY, 1)
             
        