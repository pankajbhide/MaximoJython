############################################################
# Purpose: Script for attribute level launch
#          lbl_wrhsfeeddtl.date_received
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
       
       if (jIDate_received is not None):
                      
           cal=Calendar.getInstance()                      
           todayDate=MXServer.getMXServer().getDate() # Current date
           
           
           if (jIDate_received > todayDate):
               setError("lbl_invaliddaterecd","lbl_wrhsfeed", " ")