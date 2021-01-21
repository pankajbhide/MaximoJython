################################################################
# Purpose: Script for object level launch for lbl_workorderext
#
# Author : Pankaj Bhide
#
# Date    : Aug 10, 2015
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
from psdi.util import MXApplicationException
from java.util import HashMap

def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams","")
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)


if ( jIOrgid == 'LBNL' and jISiteid == 'FAC'):
          
    # If the status of the work order is not equal to WAPPR, then, mark the fields
    # as read-only.
    thismbo=mbo.getOwner()
    
    if (thismbo is not None ):
        strWOStatus=mbo.getOwner().getString("status") # work status
        
        strWhere  =" domainid=" + "'" + "WOSTATUS" + "'" +" and maxvalue=" + "'" + "WAPPR" + "'"
        strWhere +=" and value=" + "'" + strWOStatus +"'"
        synonymdomainSet= MXServer.getMXServer().getMboSet("synonymdomain", mbo.getUserInfo())        
        synonymdomainSet.setUserWhere(strWhere)
        
        if (not synonymdomainSet.isEmpty()):
            synonymdomainSet = None
            boolwappr=True
        else:
            synonymdomainSet = None
            boolwappr=False
                    
        
        if (boolwappr != True):
            ##attrhashtable = mbo.getAttrHash()
            WO1_PHONE_readonly = True
            BUILDING_readonly = True
            ROOM_readonly = True
            LOCATION_NOTES_readonly = True
            FIRST_AVL_DATETIME_readonly = True
            SCHED_ISSUES_readonly = True
            SCHED_ISSUES_DTL_readonly = True
            BUILDING_MAINT_readonly = True
            ACCOMP_COND_PROB_readonly = True
            PRIOR_WO_readonly = True
            PRIOR_WONUM_readonly = True
            WARRANTY_ISSUE_readonly = True
            WARRANTY_ISS_DTL_readonly = True
            ESTIMATE_REQD_readonly = True
            SAFETY_ISSUE_readonly = True
            WARRANTY_ISSUE_readonly = True
            HAZARDS_readonly = True
            HAZARDS_DTL_readonly = True
            FOLLOW_STOP_WO_readonly = True
            FOLLOW_STOP_WONUM_readonly = True
            FOLLOW_STOP_DTL_readonly = True
            SELF_WO_readonly = True
            EST_HRS_readonly = True
            ASSET_DESC_readonly = True
            PARENT_WO_EXISTS_readonly = True
            PARENT_WONUM_readonly = True      
                
               
               
    if ((onadd == True)  or  (onupdate ==True)):
        
        boolError=False
        # Validations on various fields 
              
        if (jIEst_hrs is not None and jIEst_hrs <= 0.00): 
          
            boolError=True
            setError("lbl_esthrszero","workorder","") 
               
       # If scheduling issue are indicated, then, it must be followed up its details
        if (jISched_issues == True):
            if (jISched_issues_dtl is None):
                boolError=True
                setError("lbl_scheddtlnull","workorder"," ")
                
       # If hazards are indicated, then, it must be followed up its details
        if (jIHazards == True):
            if (jIHazards_dtl is None):
                boolError=True
                setError("lbl_hazardsnull","workorder"," ")
                  
        # If Prior WO indicated, then, it must be followed up its details
        if (jIPrior_wo == True):
            if (jIPrior_wonum is None):
                boolError=True
                setError("lbl_priorwonull","workorder"," ") 
                
        # If warranty issue are indicated, then, it must be followed up its details
        if (jIWarranty_issue == True):
            if (jIWarranty_iss_dtl is None):
                boolError=True
                setError("lbl_warrantynull","workorder"," ")        
                
                         
         # If follow up work order are indicated, then, it must be followed up its details
        if (jIFollow_stop_wo == True):
            if (jIFollow_stop_wonum is None):
                boolError=True
                setError("lbl_followwonull","workorder"," ")
         # If warranty issue are indicated, then, it must be followed up its details
        if (jIParent_wo_exists == True):
            if (jIParent_wonum is None):
                boolError=True
                setError("lbl_parentwonull","workorder"," ")      
                                
            
                
        if (boolError == False):
                
            maximo = MXServer.getMXServer()
            jOChangedate= maximo.getDate()
            jOChangeby = user  # variable provided by scripting framework
            
           