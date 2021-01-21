#######################################################################
# Purpose: Script for object level launch assignment
#
# Author : Pankaj Bhide
#
# Date    : Feb 14, 19
#
# Revision
# History : 
#
######################################################

from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer

def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams",errparm)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)

    
def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

                                                                
                              

boolStatusCompleted=False
boolChangeWOStatusOnDel=True
assetSetRemote= MXServer.getMXServer().getMboSet("ASSET",  mbo.getUserInfo())

if (mbo.getString("orgid")=="LBNL" and mbo.getString("siteid")=="FAC"):
    
    mbo.setValue("lbl_changedate", MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    mbo.setValue("lbl_changeby",  user,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)        ###############################################################################################
    
    # FOR PSPS change asset status from assignments
    strAssetStatus=mbo.getMboValue("lbl_assetstatus").getCurrentValue().asString()
    strOldAssetStatus=mbo.getMboValue("lbl_assetstatus").getPreviousValue().asString()
    
    if (isBlank(strAssetStatus)== False and isBlank(mbo.getString("lbl_assetnum")== False)):
        if (strAssetStatus != strOldAssetStatus):
           
                assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + mbo.getString("lbl_assetnum") + "'")
                assetSetRemote.reset()             
                if (not assetSetRemote.isEmpty()):
                    assetSet=assetSetRemote.getMbo(0)
                    if (strAssetStatus=="SHUTDOWN"):
                        strAssetStat="SHUTDOWN"
                    if (strAssetStatus=="START"):
                        strAssetStat="OPERATING"
                    if (assetSet.getString("status") != strAssetStat):
                        assetSet.changeStatus(strAssetStat, False, False, False, False) # rollToAllChildren, removeFromActiveRoutes, removeFromActiveSP,changePMStatus
                        assetSetRemote.save()
                assetSetRemote=None
           
    
 

    ###############################################################################################
    # Somehow we realized that assignment start/stop dates coming from datasplice are incorrect
    # Therefore we are setting them with current datetimestamp 
    ###############################################################################################
    '''if (mbo.getMboValueData("LBL_STARTDTTM").isNull() == False):
        
        if (jIOLblStartTime_modified == True):
            if (mbo.getDate("LBL_STARTDTTM").after(MXServer.getMXServer().getDate())):
                mbo.setValue("LBL_STARTDTTM", MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                
    if (mbo.getMboValueData("LBL_STOPDTTM").isNull() == False):
                     
        if (jIOLblStoptime_modified == True):
            if (mbo.getDate("LBL_STOPDTTM").after(MXServer.getMXServer().getDate())):
                mbo.setValue("LBL_STOPDTTM", MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    '''
                
    strWhere1   =" orgid='LBNL' and siteid='FAC' and wonum='" + mbo.getString("wonum") +"'"            
    # Status=DEL or record is getting deleted 
    if (mbo.getString("lbl_status")=="DEL") or (ondelete==True):
       
        lngassignmentid=mbo.getLong("assignmentid")
        
        # Check whether the status of the work order can be changed to WCRAFTSUP if all the
        # assignments are completed.
        
        rowsSet3=MXServer.getMXServer().getMboSet("assignment", mbo.getUserInfo())
        
        rowsSet3.setUserWhere(strWhere1 + " and (lbl_status not like '%COMP%' or lbl_status is null) and  assignmentid !=" + str(lngassignmentid) )
        if (rowsSet3.isEmpty()):
            
            rowsSet= MXServer.getMXServer().getMboSet("workorder", mbo.getUserInfo())
            rowsSet.setUserWhere(strWhere1)
            rowsSet.getMbo(0).changeStatus("WCRAFTSUP",
                                           MXServer.getMXServer().getDate(),
                                           "Status changed via datasplice.",
                                           MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                  
            rowsSet.save()   
            rowsSet=None
        
        if (mbo.getString("lbl_status")=="DEL"):   
            mbo.delete(MboConstants.NOACCESSCHECK)  
                       
              
    if (jIOLblstatus_modified == True ):
        
     
        boolStatusCompleted="COMP" in  mbo.getString("lbl_status")
        
                                                                               
        
        if ((mbo.getString("lbl_status")=="STARTED") or ( boolStatusCompleted == True)):
           
    
            strWOstatus=""
            strWhere1   =" orgid='LBNL' and siteid='FAC' and wonum='" + mbo.getString("wonum") +"'"
            
            rowsSet= MXServer.getMXServer().getMboSet("workorder", mbo.getUserInfo())
            rowsSet.setUserWhere(strWhere1)
          
            if (not rowsSet.isEmpty()): 
                # If LBL_STATUS='STARTED', then check whether the status of the work order=INPRG, if not, then
                # change its status to INPRG
                if (mbo.getString("lbl_status")=="STARTED"):
                    
                    if (rowsSet.getMbo(0).getString("status") != 'INPRG'):
                        strWOstatus="INPRG"
                      
                # If the status starts with COMP, then, find out whether all
                # assignments for that work order are completed, If they are
                # then change the status of the work order to WCRAFTSUP  
                if (boolStatusCompleted  == True):
                    
                    lngassignmentid=mbo.getLong("assignmentid")                                                                                                                                           
                    rowsSet2=MXServer.getMXServer().getMboSet("assignment", mbo.getUserInfo())       
                    rowsSet2.setUserWhere(strWhere1 + " and (lbl_status not like '%COMP%'  or lbl_status is null) and  assignmentid !=" + str(lngassignmentid) )
         
                    if (rowsSet2.isEmpty()):
                        strWOstatus='WCRAFTSUP'
                    rowsSet2=None                        
                    
               
                if (isBlank(strWOstatus)==False):
                    
                   
                    rowsSet.getMbo(0).changeStatus(strWOstatus,
                                            MXServer.getMXServer().getDate(),
                                            "Status changed via datasplice.",
                                            MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                      
                    rowsSet.save()   
                    
            rowsSet=None