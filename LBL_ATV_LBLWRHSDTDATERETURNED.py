############################################################
# Purpose: Script for attribute level launch
#          lbl_wrhsfeeddtl.date_returned
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
from java.util import Calendar
from java.util import HashMap

def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams","")
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)


if ( jIOrgid == 'LBNL' and jISiteid == 'FAC'):
       
      boolError=False
       
      if (jIDate_received is not None):
                      
           if (jIDate_returned < jIDate_received):                                               
               setError("lbl_dtrecd_dtreturn","lbl_wrhsfeed", " ")
               boolError=True
               
           if (boolError == False):
               
                 strWhere   = " FINANCIALPERIOD=(SELECT MIN(C.FINANCIALPERIOD) FROM FINANCIALPERIODS C"
                 strWhere  +="  WHERE  (NVL(C.CLOSEDBY,' ') NOT LIKE '%STR%') AND C.ORGID='" + jIOrgid +  "') "
                 financialperiodsSet= MXServer.getMXServer().getMboSet("FINANCIALPERIODS", mbo.getUserInfo())
                 financialperiodsSet.setUserWhere(strWhere)
                 if (financialperiodsSet.isEmpty()):
                      setError("lbl_invalid_dtreturn","lbl_wrhsfeed"," ")
                      boolError=True
                 if (boolError == False):
                     if (financialperiodsSet.getMbo(0).getDate("periodstart") > jIDate_returned):
                         setError("lbl_invalid_dtreturn","lbl_wrhsfeed", " ")
                
                 financialperiodsSet=None