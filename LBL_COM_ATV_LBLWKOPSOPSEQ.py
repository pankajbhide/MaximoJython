############################################################
# Purpose: Script for checking whether operation seq number is 
#          duplicated or not
#
# Author : Pankaj Bhide
#
# Date    : Mar 6, 2015
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


if ( ondelete == False):
    
    if (jIOpsequence <=0):
      ctx = HashMap()
      ctx.put("paramErrorkey","lbl_wkopseq>0")
      ctx.put("paramErrorgroup","lbl_wkthruops")
      ctx.put("paramParams","")
      service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)  
    else:
                                      
        thisSet=mbo.getThisMboSet()
        intCount=thisSet.count()
                
        # Create an empty list and append all opsequence into the list        
        myList = []        
        for i in xrange(intCount):
            if (thisSet.getMbo(i).toBeDeleted() == False):
                thisRow = thisSet.getMbo(i)
                myList.append(thisRow.getInt("opsequence"))
                
            
            # If the length of the list and length lists set (unique) is equal
            # then there are no duplicates.   
            if len(myList)!=len(set(myList)):                         
                      thisSet = None
                      ctx = HashMap()
                      ctx.put("paramErrorkey","lbl_duplicatewkthruops")
                      ctx.put("paramErrorgroup","lbl_wkthruops")
                      ctx.put("paramParams","")
                      service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
                      
     