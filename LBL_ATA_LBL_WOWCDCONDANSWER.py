#######################################################################
# Purpose: Script for attribute level launch (action)
#           LBL_WOWCDCONDITION.ANSWER
# Author : Pankaj Bhide
#
# Date    : August 24 , 2015
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


logger = mbo.getMboLogger()

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    

    # Determine where to lookup. If sub condition is not null then
    # look into sub condition
    
    condSet = MXServer.getMXServer().getMboSet("LBL_WCDCONDITION", mbo.getUserInfo())       
    strWhere  = "conditionnum=" + str(jIConditionnum) +" and active=1"       
    condSet.setUserWhere(strWhere)
                 
    if (not jISubconditionnum is None and  jISubconditionnum !=0):
        condSet = MXServer.getMXServer().getMboSet("lbl_wcdsubcond", mbo.getUserInfo())       
        strWhere  = "conditionnum=" + str(jIConditionnum) +" and subconditionnum=" + str(jISubconditionnum) + " and active=1"       
        condSet.setUserWhere(strWhere)

    if (not condSet.isEmpty()):
                        
        points=0    
        if (jIAnswer.lower()=="yes"):
             points=condSet.getMbo(0).getDouble("YESPOINT")
        if (jIAnswer.lower() =="no"):
             points=condSet.getMbo(0).getDouble("NOPOINT")
        if (jIAnswer.lower() =="unknown"):
             points=condSet.getMbo(0).getDouble("UNKNOWNPOINT")
            
        jOPoints=points
        jOPoints_readonly=True
     
    condSet=None
                   