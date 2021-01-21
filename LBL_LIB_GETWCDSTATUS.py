#######################################################
# Purpose: Library script for returning the
#          WCD status of the work orders 
#
# Author : Pankaj Bhide
#
# Date    : Aug 4, 2015
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


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

    
strWCDStatus=""

 #logger = mbo.getMboLogger()   
 #logger.info("PRB mbo name : " + mbo.getName()) 

#######################################################
# Please note that mbo referred in this script is an
# "argument" passed by the call script. 
#######################################################

if (mbo.getString("lbl_wcd_status")=="FINALIZED" or 
    mbo.getString("lbl_wcd_status")=="DRAFT" ):
    strWCDStatus=mbo.getString("lbl_wcd_status")
    
else:
    
    if (isBlank(strWCDStatus) == True):
                        
        if (isBlank(mbo.getString("worktype"))== True):
            strWCDStatus="UNKNOWN"
            
    if (isBlank(strWCDStatus) == True):     
        strWhere="worktype=" + "'" + mbo.getString("worktype") +"'"      
        worktypeSet= MXServer.getMXServer().getMboSet("WORKTYPE", mbo.getUserInfo())
        worktypeSet.setUserWhere(strWhere)
                
        
        if (not worktypeSet.isEmpty()):
            strWcdreqd=worktypeSet.getMbo(0).getString("lbl_wcd_reqd") 
            
            if (strWcdreqd=="N"):
                worktypeSet=None
                strWCDStatus="NOT REQUIRED"
                
    if (isBlank(strWCDStatus) == True):
            
        if (isBlank(mbo.getString("lbl_destgroup"))== False ):
            strWhere="domainid='LBL_EXMPT_WCD_DG' and value='" +  mbo.getString("lbl_destgroup") + "'"
            alnDomainSet= MXServer.getMXServer().getMboSet("ALNDOMAIN", mbo.getUserInfo())
            alnDomainSet.setUserWhere(strWhere)
            
            if (not alnDomainSet.isEmpty()):
                alnDomainSet=None
                strWCDStatus="NOT REQUIRED"
                
    if (isBlank(strWCDStatus) == True):
         
        if (isBlank(mbo.getString("leadcraft"))== False ):
            strWhere="domainid='LBL_WCD_LEADCRAFT' and value='" +  mbo.getString("leadcraft") + "'"
            alnDomainSet= MXServer.getMXServer().getMboSet("ALNDOMAIN", mbo.getUserInfo())
            alnDomainSet.setUserWhere(strWhere)
            if (alnDomainSet.isEmpty()):
                alnDomainSet=None
                strWCDStatus= "NOT REQUIRED"
      
    if (isBlank(strWCDStatus) == True):
          strWCDStatus="REQUIRED"
        
