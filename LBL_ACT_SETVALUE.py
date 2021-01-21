####################################################
# Purpose: ACTION LAUNCH POINT TO SET VALUE
#
# Author : Pankaj Bhide
#
# Date    : July 26, 2020
#
# Revision
# History : 
#
##########################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer



def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

logger = mbo.getMboLogger()


strMboName=mbo.getName()

if (strMboName=='LBL_WORKORDEREXT'):        
        
        mbo.setValue("last_email_nepa_ceqa",MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        mxServer = MXServer.getMXServer() 
        securityflag = mxServer.getSecurityContext() 
        mxServer.setSecurityCheck(mxServer.SecurityContextFlag.DISABLED ) 
        mbo.getThisMboSet().save() 
        mxServer.setSecurityCheck(securityflag )
        
               
        
        
                
            
            
            
        
        
        
