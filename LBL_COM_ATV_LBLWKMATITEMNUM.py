############################################################
# Purpose: Script for checking whether item number is 
#          duplicated or not
#
# Author : Pankaj Bhide
#
# Date    : July 15, 2015
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
    
    thisSet=mbo.getThisMboSet()
    intCount=thisSet.count() 
    if (onadd==True):
        intCount=intCount-1
            
    for i in xrange(intCount):
        
        thisRow = thisSet.getMbo(i)
        
        if (thisRow.getString("itemnum") == jIItemnum):
              thisSet = None
              ctx = HashMap()
              ctx.put("paramErrorkey","lbl_duplicateItemnum")
              ctx.put("paramErrorgroup","lbl_wkthruops")
              ctx.put("paramParams","")
              service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
           
              break
       