###################################################### 
# Purpose: Common script for attribute level validate
#          launch for various fields of work order 
#          object
#
# Author : Pankaj Bhide
#
# Date    : Aug 12 2015
#
# Revision
# History : 
#
######################################################

from psdi.server import MXServer
from psdi.mbo  import   MboConstants
from java.util import Date
from java.util import Calendar
from java.util import HashMap
from psdi.util.logging import MXLoggerFactory




def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams",errparm)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
    
    
    

logger = mbo.getMboLogger()
ctx = HashMap()
ctx.put("mbo",mbo)   


if ( jIOrgid == 'LBNL' and jISiteid == 'FAC'):
    
    
    ##########################
    # Status of the work order
    ###########################
    if (jIFieldname=="STATUS"):
        
        boolError=False
        #boolCanChangeStatus=False
        strOldStatus=mbo.getMboValue("status").getPreviousValue().asString()
        #service.log("PRB old status " + strOldStatus)
        
        #JIRA EF-7889 Do not allow parent work order to CLOSE or CANCEL
        # if any of its child is not closed
        if ((jIStatus=="WCLOSE" or jIStatus=="CLOSE" or jIStatus=="CAN" or jIStatus=="COMP") and (mbo.getBoolean("haschildren")==True)):
            
            boolCanClose=True
            woancestorSet = mbo.getMboSet("LBL_WOANCESTORS")               
            if (not woancestorSet.isEmpty()):
                intCount=woancestorSet.count()                        
                for i in xrange(intCount):
                    #strWhere1  = " orgid='LBNL' and siteid='FAC' and wonum='" +  woancestorSet.getMbo(i).getString("wonum") + "' and historyflag=0 and PARENTCHGSSTATUS=0 "
                    # Revision as per  Tammy - Check the work order that are not completed,closed or cancelled
                    strWhere1  = " orgid='LBNL' and siteid='FAC' and wonum='" +  woancestorSet.getMbo(i).getString("wonum") + "' and PARENTCHGSSTATUS=0 and status in (select p.value from synonymdomain p where p.domainid='WOSTATUS' and p.maxvalue not in ('CLOSE','COMP','CAN'))"
                    workorderSet1= MXServer.getMXServer().getMboSet("workorder", mbo.getUserInfo())
                    workorderSet1.setUserWhere(strWhere1)
                    if (not workorderSet1.isEmpty()):
                        boolCanClose=False;
                        workorderSet1.close()
                        workorderSet1=None
                        break
            woancestorSet.close()
            woancestorSet=None
            
            if (boolCanClose !=True):
                setError("lbl_cannotclosechildopen","workorder",mbo.getString("wonum"))
                boolError=True
                
        
        # For release work order scheduled start/end dates are mandatory
        # when the status is changed to ASSIGNED
        # Do not perform this check for tool pouch (class structure id=00002246)
        boolError=False
        if ((jIStatus=="ASSIGNED" or jIStatus_internal=="INPRG" or jIStatus_internal == "COMP" or jIStatus_internal=="CLOSE") and (mbo.getString("classstructureid") != "00002246")):

            
            ###############################################################################################
            #JIRA 7894
            # Find out whether the work type requires FAM so that validation for scheduled start/end date
            # can be fired
            ###############################################################################################
            boolFamReqd=False
            strWhere1  = " orgid='LBNL' and worktype='" + mbo.getString("worktype") + "'"
            maxWorktypeSet = MXServer.getMXServer().getMboSet("worktype", mbo.getUserInfo())
            maxWorktypeSet.setUserWhere(strWhere1)
            if (not maxWorktypeSet.isEmpty()):
                                           
                if (maxWorktypeSet.getMbo(0).getBoolean("lbl_famreqd")== True):
                    boolFamReqd=True
            maxWorktypeSet=None
            
            #if (mbo.getString("LBL_RELEASE_STATUS") in ('REQUIRED','REQUEST FOR INFORMATION','RELEASED')):
            if (boolFamReqd == True and mbo.getBoolean("istask")== False):
                if (mbo.getMboValueData("SCHEDSTART").isNull() == True):
                    setError("lbl_schedstartnull","workorder",mbo.getString("wonum"))
                    boolError=True
                       
                if (mbo.getMboValueData("SCHEDFINISH").isNull() == True):
                    setError("lbl_schedfinishnull","workorder",mbo.getString("wonum"))
                    boolError=True      
      
        
        # Trying to change to INPRG and further is not allowed for the work order that needs
        # release. It must be preceeded by SCHD
        
        if (boolError==False):
                  
            #if (jIStatus_internal=="INPRG" or jIStatus_internal == "COMP" or jIStatus_internal=="CLOSE"):
            #    if ((mbo.getString("lbl_release_status")=="REQUIRED" or mbo.getString("lbl_release_status") =="REQUEST FOR INFORAMTION") and strOldStatus !="SCHD"):
            #        
            #        setError("lbl_inprgnotallowed","workorder",mbo.getString("wonum"))
            #        boolError=True                                    
        
            if (mbo.getString("lbl_release_status")=="REQUIRED" and jIStatus_internal !="WAPPR"  and jIStatus_internal !="CAN" and jIStatus !="WREL"):
                
                # Following are approved status, but Facilities wants allowing them to change their status before WREL
                # These status values are stored in lbl_maxvars table
                strWhere1  = " orgid='LBNL'  and siteid='FAC' and varname='ALLOW_APPR_BEF_WREL' and varvalue='" + jIStatus + "'"
                lblMaxVarsSet = MXServer.getMXServer().getMboSet("lbl_maxvars", mbo.getUserInfo())
                lblMaxVarsSet.setUserWhere(strWhere1)
                if (lblMaxVarsSet.isEmpty()):   
                    setError("lbl_wrellocked","workorder",mbo.getString("wonum"))
                    boolError=True
                lblMaxVarsSet=None    
            
        
        # only allowable status after WREL are REL or RFI  
        if (boolError == False and strOldStatus is not None and strOldStatus =="WREL" ):
            if (mbo.getString("status") !="REL" and mbo.getString("status") !="RFI" ):
                
                setError("lbl_wrellocked","workorder",mbo.getString("wonum"))
                boolError=True
                
        # The prior status of the work order has to be either WREL or RFI for REL to work        
        if (boolError == False and mbo.getString("status") == "REL"):
            if (strOldStatus !="WREL" and strOldStatus !="RFI"):
                setError("lbl_lrelnoallowed","workorder",mbo.getString("wonum"))
                boolError=True
                
                       
        if (boolError == False and jIStatus=="SCHD" or jIStatus=="WREL"):
    
            # The validations with respect to scheduled start/end are not required
            # as per JIRA EF-5386.
            #
            #if (mbo.getMboValueData("schedstart").isNull() == True):
            #        setError("lbl_schedstartnull","workorder",mbo.getString("wonum"))
            #        boolError=True
                       
            #if (mbo.getMboValueData("schedfinish").isNull() == True):
            #        setError("lbl_schedfinishnull","workorder",mbo.getString("wonum"))
            #        boolError=True
            if (mbo.getString("LBL_RELEASE_STATUS") in ('REQUIRED','REQUEST FOR INFORMATION','WAITING RELEASE','RELEASED')):
                
                if (mbo.getMboValueData("TARGSTARTDATE").isNull() == True):
                        setError("lbl_targstartnull","workorder",mbo.getString("wonum"))
                        boolError=True
                           
                if (mbo.getMboValueData("TARGCOMPDATE").isNull() == True):
                        setError("lbl_targcompnull","workorder",mbo.getString("wonum"))
                        boolError=True      
                    
        if (boolError == False and jIStatus=="WPLAN"):
            
            #if ((isBlank(mbo.getString("location")) == True) or (isBlank(mbo.getString("glaccount")) == True) or (isBlank(mbo.getString("lbl_planner_group")) == True)):           
            #JIRA EF-9121 No need to have plann group for WPLAN 
            if ((isBlank(mbo.getString("location")) == True) or (isBlank(mbo.getString("glaccount")) == True)):
  
                  setError("lbl_locglacctnullwplan","workorder",mbo.getString("wonum"))
                  boolError=True    
                  
            if (mbo.getString("lbl_release_status")=="UNKNOWN"):
                setError("lbl_relstatusnotknownwplan","workorder",mbo.getString("wonum"))
                boolError=True    
                
        # Supervisor is not requred for PLAN          
        if (boolError == False and jIStatus=="PLAN"):
            if ((isBlank(mbo.getString("location")) == True) or (isBlank(mbo.getString("glaccount")) == True) or (isBlank(mbo.getString("worktype")) == True) or (isBlank(mbo.getString("lbl_planner_group")) == True)): # or (isBlank(mbo.getString("supervisor")) == True)  ):
                  setError("lbl_fillforplan","workorder",mbo.getString("wonum"))
                  boolError=True
                          
        # Check whether user belongs to FA_FAM group. If the user belongs to that group
        # then the only status that the user can change is either WPLAN, REL, CAN
                     
        if (boolError == False):
                strWhere1 =" groupname in ('FAC_FAM') " 
                strWhere1 +=" and   upper(userid)=" + "'" + user.upper() + "'"
                
                maxgroupuserset = MXServer.getMXServer().getMboSet("groupuser", mbo.getUserInfo())
                maxgroupuserset.setUserWhere(strWhere1)
                
                if (not maxgroupuserset.isEmpty()):
                    # Added WPLANSUP JIRA EF-6134
                    # Added additional status values as per JIRA EF-6408
                    #if (jIStatus != "WPLAN" and jIStatus != "REL" and jIStatus != "CAN" and jIStatus != "WPLANSUP"):
                    # Added WSCH1 as per JIRA EF-6693
                    # Use domain instead of hardcoding the values
                    #if (jIStatus != "WPLAN" and jIStatus != "REL" and jIStatus != "CAN" and jIStatus != "WPLANSUP" and jIStatus != "WAPPR" and jIStatus != "VENDOR" and jIStatus != "WSHUT" and jIStatus != "WSCH1"):
                    
                    strWhere1=" domainid='LBL_FAMWOSTATUS' and value='" + jIStatus +"'"
                    myALNDomainSet= MXServer.getMXServer().getMboSet("ALNDOMAIN", mbo.getUserInfo())
                    myALNDomainSet.setUserWhere(strWhere1)
        
                    if (myALNDomainSet.isEmpty()):                        
                        setError("lbl_restrictfamwostatus","workorder",mbo.getString("wonum"))
                        myALNDomainSet=None 
                        maxgroupuserset=None   
                        boolError=True
                    myALNDomainSet=None
                    maxgroupuserset=None    
    
        if (boolError == False):
        
            # Allow cancellation of work order without any condition
            if (jIStatus != "CAN"):
                
               # Validations if the new status is beyond WAPPR and old status=WAPPR
               stroldtempstatus=strOldStatus
               stroldtempstatus=MXServer.getMXServer().getMaximoDD().getTranslator().toInternalString("WOSTATUS",stroldtempstatus)
           
               
               # Status getting changed from WAPPR To APPR
               if (jIStatus_internal != "WAPPR" and stroldtempstatus=="WAPPR"):
    
    
                   # Get the release status based upon the latest field values
                   service.invokeScript("LBL_LIB_GETRELEASESTATUS",ctx)       
                   strReleaseStatus=str(ctx.get("strReleaseStatus"))
                                                     
                   #if (strReleaseStatus != mbo.getString("lbl_release_status")):
                   #    setError("lbl_inconsistantrelease","workorder",mbo.getString("wonum"))
                   #    boolError=True
                   #    ##mbo.setValue("lbl_release_status", strReleaseStatus,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                   
                   # Release status can not be null or unknown
                   if (strReleaseStatus is None or strReleaseStatus=="UNKNOWN"):
                       setError("lbl_unknownrelease","workorder",mbo.getString("wonum"))
                       boolError=True
    
    
                   # Work type can not be blank
                   if (isBlank(mbo.getString("worktype")) == True):
                       setError("lbl_worktypenull_appr","workorder",mbo.getString("wonum"))
                       boolError=True
    
                   if (boolError == False):
    
                       # Find out whether the work type is chargeable or not
                       boolChargeable=True
                       strWhere1  = " orgid='LBNL' and worktype='" + mbo.getString("worktype") + "'"
                       maxWorktypeSet = MXServer.getMXServer().getMboSet("worktype", mbo.getUserInfo())
                       maxWorktypeSet.setUserWhere(strWhere1)
                       if (not maxWorktypeSet.isEmpty()):
                        
                           if (maxWorktypeSet.getMbo(0).getString("type") is not None and
                               maxWorktypeSet.getMbo(0).getString("type")=="NOCHARGE"):
    
                               boolChargeable=False
                       maxWorktypeSet=None
    
                       # Additional validations only if work order is chargeable
                       if (boolChargeable==True):
    
                           if (isBlank(mbo.getString("location")) == True):
                               setError("lbl_locationnull_appr","workorder",mbo.getString("wonum"))
                               boolError=True
                               
                           # Supervisor not mandatory for approval
                           #if (isBlank(mbo.getString("supervisor")) == True):
                           #    setError("lbl_supervisornull_appr","workorder",mbo.getString("wonum"))
                           #    boolError=True
        
                           if (isBlank(mbo.getString("glaccount")) == True):
                               setError("lbl_glaccountnull_appr","workorder",mbo.getString("wonum"))
                               boolError=True
        
                           # JIRA EF-10133 Allow changing status to complete if glaccount is invalid 
                           if (boolError == False and (jIStatus_internal != "COMP" and jIStatus_internal != "CLOSE" and jIStatus_internal != "CAN" )):                                     
                           
                               #Find whether the glaccount is active and it should not be a work order
                               strWhere1  =" GLACCOUNT='" + mbo.getString("glaccount") +"'"
                               strWhere1 +=" AND active=1 "
                               strWhere1 +=" AND NOT EXISTS (select 1 from workorder where wonum='" + mbo.getString("glaccount") +"') "
                               glacctSet = MXServer.getMXServer().getMboSet("CHARTOFACCOUNTS", mbo.getUserInfo())
                               glacctSet.setUserWhere(strWhere1)
                               if (glacctSet.isEmpty()):
                                    glacctSet=None
                                    setError("lbl_glaccountinvalid_appr","workorder",mbo.getString("wonum"))
                                    boolError=True

                               glacctSet=None

                               #If the user specifies any parent, then parent must have glaccount
                               if (isBlank(mbo.getString("parent")) == False):
                                   strWhere1  =" orgid='LBNL' and siteid='FAC' and wonum='" + mbo.getString("parent") + "'"
                                   workorderSet = MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())
                                   workorderSet.setUserWhere(strWhere1)
                                   if (workorderSet.isEmpty()):
                                        workorderSet=None
                                        setError("LblWOvalidate_parent2glaccount","workorder",mbo.getString("wonum"))
                                        boolError=True

                                   if (isBlank(workorderSet.getMbo(0).getString("glaccount")) == True):
                                        workorderSet=None
                                        setError("LblWOvalidate_parent2glaccount","workorder",mbo.getString("wonum"))
                                        boolError=True

                                   workorderSet=None
    
     

    ####################
    # Parent work order
    #####################
    if (jIFieldname=="PARENT"):            
       
        if (isBlank(mbo.getString("parent")) == False):
      
        
            # Check whether the release status of the parent work order
            workorderSet = MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())       
            strWhere  = "orgid='" + jIOrgid + "' and siteid='" + jISiteid +"'"
            strWhere += " and wonum='" + mbo.getString("parent") + "'"

                 
            workorderSet.setUserWhere(strWhere)
            if (not workorderSet.isEmpty()):
                strReleaseStatus = workorderSet.getMbo(0).getString("lbl_release_status")
              
                if ((strReleaseStatus is not None) and (strReleaseStatus=="WAITING RELEASE")):
                    
                        workorderSet = None
                        setError("lbl_parentwrel", "workorder", "for work order: " +mbo.getString("parent"))
                else:
                        workorderSet = None
                        
    #################################
    # Scheduled start/finish dates
    # JIRA EF-5386
    #################################
    if (jIFieldname=="SCHEDSTART"  and mbo.getString("LBL_RELEASE_STATUS") in ('REQUIRED','REQUEST FOR INFORMATION','WAITING RELEASE','RELEASED')):
        
                                                                                           
        boolError=False
        
        if (mbo.getMboValueData("TARGSTARTDATE").isNull() == True):            
                setError("lbl_targstartnull","workorder",mbo.getString("wonum"))
                boolError=True        
        if (mbo.getMboValueData("TARGCOMPDATE").isNull() == True):
                    setError("lbl_targcompnull","workorder",mbo.getString("wonum"))
                    boolError=True    
                    
        if (boolError == False):          
            
            if (mbo.getMboValueData("SCHEDSTART").isNull() == False):   
                        
                if (mbo.getDate("SCHEDSTART").before(mbo.getDate("TARGSTARTDATE"))):
                    setError("lbl_schedtargstartinvalid","workorder",mbo.getString("wonum"))
                    boolError=True
                
                if (mbo.getDate("SCHEDSTART").after(mbo.getDate("TARGCOMPDATE"))):            
                    setError("lbl_schedtargstartinvalid","workorder",mbo.getString("wonum"))
                    boolError=True
    
    
    if (jIFieldname=="SCHEDFINISH"  and mbo.getString("LBL_RELEASE_STATUS") in ('REQUIRED','REQUEST FOR INFORMATION','WAITING RELEASE','RELEASED')):
                        
        boolError=False
        
        if (mbo.getMboValueData("TARGSTARTDATE").isNull() == True):            
                setError("lbl_targstartnull","workorder",mbo.getString("wonum"))
                boolError=True        
        if (mbo.getMboValueData("TARGCOMPDATE").isNull() == True):
                    setError("lbl_targcompnull","workorder",mbo.getString("wonum"))
                    boolError=True    
                    
        if (boolError == False):          
                              
            if (mbo.getMboValueData("SCHEDFINISH").isNull() == False):  
                                    
                if (mbo.getDate("SCHEDFINISH").before(mbo.getDate("TARGSTARTDATE"))):
                    setError("lbl_schedtargfinishinvalid","workorder",mbo.getString("wonum"))
                    boolError=True
                    
                if (mbo.getDate("SCHEDFINISH").after(mbo.getDate("TARGCOMPDATE"))):            
                    setError("lbl_schedtargfinishinvalid","workorder",mbo.getString("wonum"))
                    boolError=True
                
    if (jIFieldname=="TARGSTARTDATE"):
                        
        boolError=False
        
        if (mbo.getMboValueData("TARGSTARTDATE").isNull() == True):
            if (mbo.getMboValueData("SCHEDSTART").isNull() == False):
                setError("lbl_targstartnull","workorder",mbo.getString("wonum"))
                boolError=True 
                
        if (mbo.getMboValueData("SCHEDSTART").isNull() == False):
            if (mbo.getDate("TARGSTARTDATE").after(mbo.getDate("SCHEDSTART"))):
                setError("lbl_targstartinvalid","workorder",mbo.getString("wonum"))
                boolError=True
                
        if (mbo.getMboValueData("SCHEDFINISH").isNull() == False):
            
            if (mbo.getDate("TARGSTARTDATE").after(mbo.getDate("SCHEDFINISH"))):
                setError("lbl_targstartinvalid","workorder",mbo.getString("wonum"))
                boolError=True     
                                
                
    if (jIFieldname=="TARGCOMPDATE"):
                        
        boolError=False
        
        if (mbo.getMboValueData("TARGCOMPDATE").isNull() == True):
            if (mbo.getMboValueData("SCHEDSTART").isNull() == False):
                setError("lbl_targcompnull","workorder",mbo.getString("wonum"))
                boolError=True 
        
        
        if (mbo.getMboValueData("SCHEDSTART").isNull() == False):
            
            if (mbo.getDate("TARGCOMPDATE").before(mbo.getDate("SCHEDSTART"))):
                setError("lbl_targcompinvalid","workorder",mbo.getString("wonum"))
                boolError=True   
        
        if (mbo.getMboValueData("SCHEDFINISH").isNull() == False):
            
            if (mbo.getDate("TARGCOMPDATE").before(mbo.getDate("SCHEDFINISH"))):
                setError("lbl_targcompinvalid","workorder",mbo.getString("wonum"))
                boolError=True
                            
    # JIRA EF-6151            
    if (jIFieldname=="LBL_PLANNER_GROUP"):
        
        
        if (mbo.getString("status") !='WPLAN' and mbo.getString("status") !='WAPPR' and mbo.getString("status") !='INFO' ):
                
            setError("lbl_plannergroupnochange","workorder",mbo.getString("wonum"))
            boolError=True
                
            # Check whether work order is in the the workflow
            #wfInstSet = MXServer.getMXServer().getMboSet("wfinstance", mbo.getUserInfo())       
            #strWhere  =" ownertable='WORKORDER' and ownerid=" + str(mbo.getInt("workorderid")) + " and active=1"
                 
            #wfInstSet.setUserWhere(strWhere)
            #if (not wfInstSet.isEmpty() and mbo.getString("status") !='WPLAN'):               
            #wfInstSet=None
            
    # JIRA EF-6677            
    if (jIFieldname=="GLACCOUNT"):
        
            # The user should not change the GL Account once the work order is sent to FMS
            if (mbo.getMboValueData("LBL_DTSENTTOFMS").isNull() == False):
                setError("lbl_cannotchangeglacct","workorder",mbo.getString("wonum"))
                boolError=True
                
                

                    
                    
                    
        
                