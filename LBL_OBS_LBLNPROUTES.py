# Purpose: Object level (save) on LBL_NP_ROUTES
#
# Author : Pankaj Bhide
#
# Date    : June 25, 2020
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

# to get the non persistent object of the dialog we need a small trick
mbo = mboset.getMbo(0)
boolError=False

if (isBlank(mbo.getString("action"))== True):
    setError("lbl_actionnotnull","lbl_np_routes","")
    boolError=True
        
if (isBlank(mbo.getString("craft"))== True):
    setError("lbl_craftnotnull","lbl_np_routes","")
    boolError=True
        
if (mbo.getMboValueData("startdate").isNull() == True):
    setError("lbl_startdatenotnull","lbl_np_routes","")
    boolError=True
        

vCurrentDate = SimpleDateFormat("MM/dd/yyyy").format(Date())
startdate= SimpleDateFormat("MM/dd/yyyy").format(mbo.getDate("startdate"))
if (startdate <  vCurrentDate):
    setError("lbl_startdate<currentdate","lbl_np_routes","")
    boolError=True
    
     
if (boolError==False):
           
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    wosetRemote= mxServer.getMboSet("WORKORDER", runAsUserInfo1)  
    routestopRemote=mxServer.getMboSet("route_stop", runAsUserInfo1)     
    assignmentRemote=mxServer.getMboSet("assignment", runAsUserInfo1)
    
    mboWorkorder=wosetRemote.add()    
    strWonum=mboWorkorder.getString("wonum")
    strCraft=mbo.getString("craft")
    strAction=mbo.getString("action")
    
    mboWorkorder.setValue("orgid", "LBNL", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("siteid", "FAC", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("location", "076", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("description", "PSPS activities scheduled on " + mbo.getString("startdate") + " for " + mbo.getString("action"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("route", mbo.getString("route"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("worktype", "PD", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("TARGSTARTDATE", mbo.getString("startdate"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    mboWorkorder.setValue("changedate" ,MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
    mboWorkorder.setValue("changeby" ,"IT-BS-MXINTADM", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mboWorkorder.setValue("leadcraft", mbo.getString("craft"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    
    assignmentRemote=mboWorkorder.getMboSet("ASSIGNMENT")
    wosetRemote.save()
    
    # Add rows in assignment
    strWhere1   =" orgid='LBNL' and siteid='FAC' and route='" + mbo.getString("route") +"'";
    rowsSet= mxServer.getMboSet("route_stop", mbo.getUserInfo())
    rowsSet.setUserWhere(strWhere1)
    if (not rowsSet.isEmpty()):  
        
        intCount=rowsSet.count()
                
        for i in xrange(intCount):
            assignment=assignmentRemote.add()
            assignment.setValue("orgid", "LBNL", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            assignment.setValue("siteid", "FAC", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            assignment.setValue("lbl_assetnum", rowsSet.getMbo(i).getString("assetnum"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            assignment.setValue("lbl_assignseq", rowsSet.getMbo(i).getString("stopsequence"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            assignment.setValue("laborhrs", rowsSet.getMbo(i).getString("totalworkunits"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            assignment.setValue("wonum", strWonum, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            assignment.setValue("craft", strCraft, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            #assignment.setValue("lbl_description", strAction +  ":" + rowsSet.getMbo(i).getString("assetnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            assignment.setValue("lbl_assigntype",strAction,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            assignment.setValue("lbl_changedate" ,MXServer.getMXServer().getDate(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
            assignment.setValue("lbl_changeby" ,"IT-BS-MXINTADM", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            assignmentRemote.save()
            
            
              
                
    warngroup = "lbl_np_routes"
    warnkey = "WOCreated"
    warnparams = [strWonum]            
                

