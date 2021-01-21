############################################################
# Purpose: Script for attribute level launch
#          LBL_WHRSFEEDDTL.LBL_ORG_LEVEL_1
#
# Author : Pankaj Bhide
#
# Date    : July 23, 2015
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
    ctx.put("paramParams","")
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

if ( jIOrgid == 'LBNL' and jISiteid == 'FAC'):
       
       if (isBlank(jILbl_org_level_1) == False):
             strWhere    = " craft= '" + jILbl_org_level_1 + "'" 
             strWhere  +="  and lbl_org_level_1 is not null "
             strWhere  +="  and lbl_org_level_2 is null and lbl_org_level_3 is null "
             strWhere  +="  and lbl_org_level_4 is null   and orgid=" + "'" + jIOrgid+ "'" 
             craftSet = MXServer.getMXServer().getMboSet("craft", mbo.getUserInfo())            
             craftSet.setUserWhere(strWhere)
             if (craftSet.isEmpty()):
               setError("lbl_invaliddivision","lbl_wrhsfeed"," ")
               
           
           
                                   
                  
                




                
            
        
            
    
    