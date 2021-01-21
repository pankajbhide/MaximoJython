###############################################################
# Purpose: Script for object level launch for skdactivity
#          (before save)
# 
# Author : Pankaj Bhide
#
# Date    : March 17, 2016
#
# Revision
# History : 
#
###############################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap
from java.util import Date
from java.text import SimpleDateFormat


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



##############

logger = mbo.getMboLogger()
ctx = HashMap()
ctx.put("mbo",mbo)
boolError=False  

######################################################################
# If the new duration is different than the old duration, then
# copy the value of new duration into custom field lbl_duration
# and restore the value of workorder.duration into the new duration.
######################################################################

strOldDuration=mbo.getMboValue("duration").getPreviousValue().asString()
strDuration=mbo.getString("duration")
if (strOldDuration != strDuration):
    jOLbl_duration = jIODuration
    if (jIObjectname=='WORKORDER'):        
        strWhere='workorderid=' + str(jIObjectid)
        workordersSet = MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())
        workordersSet.setUserWhere(strWhere)
        if (not workordersSet.isEmpty()):
             jIODuration=workordersSet.getMbo(0).getDouble("estdur")
        workordersSet= None
             
            
 