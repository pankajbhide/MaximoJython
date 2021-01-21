################################################################
# Purpose: Script for object level launch for lbl_wkthrures
#          (Non init method)
# Author : Pankaj Bhide
#
# Date    : Mar 4, 2015
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
from java.util import HashMap

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
boolError=False

if (ondelete == False):     
    # Validations
    if (jICraft_comments is not None and jICraft is None):
        boolError=True
        setError("lbl_wkthruopresdnull","lbl_wkthruops","") 
        
    if (jIEhs_support_comments is not None and jIEhs_support is None):
        boolError=True
        setError("lbl_wkthruopresdnull","lbl_wkthruops","") 
            
    if (jIPermits_comments is not None and jIPermits is None):
        boolError=True
        setError("lbl_wkthruopresdnull","lbl_wkthruops","") 
    
    if (jIDrawings_comments is not None and jIDrawings is None):
        boolError=True
        setError("lbl_wkthruopresdnull","lbl_wkthruops","")
         
       
            
    if (jIResource_type == "CRAFT" ):   
        if ( jIRes_duration <= 0 and jICraft is not None):
            boolError=True
            setError("lbl_wkthrudur>0","lbl_wkthru"," ")
            
    ############################################################        
    # Check of blank values before saving the record
    ############################################################ 
    if (jIResource_type=="CRAFT"):
        if (isBlank(jICraft) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
            
    if (jIResource_type=="CRAFT"):
        
       while True:
           try:
               num = int(jISequence or '')
               break
           except ValueError:
                setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
                boolError=True
                
       if ( jISequence <= 0): 
            boolError=True
            setError("lbl_wkthruresseq>0","lbl_wkthruops"," ")
                
                       
           
    if (jIResource_type=="PLANNING_TEAM"):
                        
        while True:
           try:
               num = int(jISequence or '')
               break
           except ValueError:
                setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
                boolError=True
        
        while True:
           try:
               num = float(jIPlan_team_duration or '' or 0)
               break
           except ValueError:
                setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
                boolError=True
        
            
        if ( jIPlan_team_duration <= 0):
            boolError=True
            setError("lbl_wkthrudur>0","lbl_wkthru"," ")
            boolError=True                        
            
    if (jIResource_type=="PERMITS"):
        if (isBlank(jIPermits) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
            
    if (jIResource_type=="EHS_SUPPORT"):
        if (isBlank(jIEhs_support) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
            
    if (jIResource_type=="DRAWINGS"):
        if (isBlank(jIDrawings) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
            
    if (jIResource_type=="CONTACTS"):
        if (isBlank(jIPersonid) == True):
            setError("lbl_canotsaveemptyrecord","lbl_wkthru"," ")
            boolError=True
                                                    
                 
    if (boolError == False):
        
        maximo = MXServer.getMXServer()
        jOChangedate= maximo.getDate()
        jOChangeby = user  # variable provided by scripting framework