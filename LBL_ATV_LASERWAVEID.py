############################################################
# Purpose: Script for checking whether wavelength  is 
#          duplicated or not
#
# Author : Pankaj Bhide
#
# Date    : May 13, 2016
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
    
    intvar=mbo.getInt("wavelengthid")
    
   
    while True:
           try:
               wavelengthid = int(intvar or '' or 0)
               break
           except ValueError:
                wavelengthid=0
    
    
    if (wavelengthid <=0):
      ctx = HashMap()
      ctx.put("paramErrorkey","wavelengthid>0")
      ctx.put("paramErrorgroup","lbl_laser")
      ctx.put("paramParams","")
      service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)  
    else:
        
        thisSet=mbo.getThisMboSet()
        intCount=thisSet.count()
       
        
        if (onadd==True):
            intCount=intCount-1
                     
            
                
        for i in xrange(intCount):
            
            thisRow = thisSet.getMbo(i)
         
            
            if (thisRow.getInt("wavelengthid") == wavelengthid):
                  thisSet = None
                  ctx = HashMap()
                  ctx.put("paramErrorkey","lbl_duplicatewavelengthid")
                  ctx.put("paramErrorgroup","lbl_laser")
                  ctx.put("paramParams","")
                  service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
                  break
       