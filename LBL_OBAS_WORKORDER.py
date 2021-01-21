################################################################
# Purpose: Script for object level launch for workorder
#          (after save) 
# Author : Pankaj Bhide
#
# Date    : April 21 2017
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
    
    if (jIOStatus_modified == True):
        
        boolInitiateWF=False
        
        strWhere1=" domainid='LBL_MROWKFLWOSTAT' and value='" + jIOStatus +"'"
        myALNDomainSet= MXServer.getMXServer().getMboSet("ALNDOMAIN", mbo.getUserInfo())
        myALNDomainSet.setUserWhere(strWhere1)
        
        if (not myALNDomainSet.isEmpty()):
            boolInitiateWF=True         
        myALNDomainSet=None    
        
        if (boolInitiateWF == True):
            
            strWhere=" processname='FAMRO' and  enabled=1 and active=1 "
            wfprocessSet= MXServer.getMXServer().getMboSet("wfprocess", mbo.getUserInfo())
            wfprocessSet.setUserWhere(strWhere)
            if (not wfprocessSet.isEmpty()):
                boolInitiateWF=True
            else:
                boolInitiateWF=False
            wfprocessSet=None
        
        strWorktype=""        
        if (boolInitiateWF == True):
            if (isBlank(mbo.getString("worktype"))==False):
              
                strWhere1=" worktype='" + mbo.getString("worktype") +"' and lbl_eligmrowkflow=1"
                myworktypeSet= MXServer.getMXServer().getMboSet("WORKTYPE", mbo.getUserInfo())
                myworktypeSet.setUserWhere(strWhere1)
                if (not myworktypeSet.isEmpty()):
                    boolInitiateWF = True
                else:
                    boolInitiateWF = False
                myworktypeSet=None
                           
        
        if(boolInitiateWF==True):
                 
            # Find out whether the work order is already in work flow. 
            # if not, then only, initiate FAMRO work flow.                  
            strWhere1  =" ownerid=" + str(mbo.getInt("workorderid")) + " and assignstatus='ACTIVE' and ownertable='WORKORDER' " 
            strWhere1 +=" and processname in (select b.processname from wfprocess b where b.processname like 'FA%' and b.enabled=1)"
             
            mywfassignmentSet= MXServer.getMXServer().getMboSet("wfassignment", mbo.getUserInfo())
            mywfassignmentSet.setUserWhere(strWhere1)
            
            
            if (not mywfassignmentSet.isEmpty()):
                boolInitiateWF=False
              
            
            mywfassignmentSet=None        
            
            if (boolInitiateWF==True):                                           
                MXServer.getMXServer().lookup("WORKFLOW").initiateWorkflow("FAMRO",mbo)
                           
             
                
