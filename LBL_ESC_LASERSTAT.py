################################################################
# Purpose: Script for act ion launch on change of laser status
#
# Author : Pankaj Bhide
#
# Date    : May 20, 2016
#
# Revision
# History :
#
#################################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

boolError=False
strSubjectline=""
strBody=""

logger = mbo.getMboLogger()
strStatus=""
laserSetActive = MXServer.getMXServer().getMboSet("lbl_laser", mbo.getUserInfo())
laserSetInActive = MXServer.getMXServer().getMboSet("lbl_laser", mbo.getUserInfo())
workordersSet = MXServer.getMXServer().getMboSet("workorder", mbo.getUserInfo())
strWhere=""


#######################################
# Check whether the laser is activated
#######################################
strWhere = " orgid='" + mbo.getString("orgid")+ "'" + " and siteid='" + mbo.getString("siteid")+ "'"
strWhere +=" and assetnum='" + mbo.getString("assetnum")+ "'"  
strWhere +=" and status='INACTIVE' and exists (select 1 from lbl_laser_loc a "
strWhere +=" where a.assetnum='" +  mbo.getString("assetnum") +"'" + ")"
laserSetActive.setUserWhere(strWhere)


if (not laserSetActive.isEmpty()):
    maximo = MXServer.getMXServer()
    laserSetActive.getMbo(0).setValue("STATUS","ACTIVE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    laserSetActive.getMbo(0).setValue("STATUSDATE", maximo.getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    strStatus="Active"
else:    
    # Check whether the laser is in-activated
    
    strWhere = " orgid='" + mbo.getString("orgid")+ "'" + " and siteid='" + mbo.getString("siteid")+ "'"
    strWhere +=" and assetnum='" + mbo.getString("assetnum")+ "'"  
    strWhere +=" and status='ACTIVE' and not exists (select 1 from lbl_laser_loc a "
    strWhere +=" where a.assetnum='" +   mbo.getString("assetnum") +"'" + ")"
    laserSetInActive.setUserWhere(strWhere)
        
    if (not laserSetInActive.isEmpty()):
        
        maximo = MXServer.getMXServer()
        laserSetInActive.getMbo(0).setValue("STATUS","INACTIVE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        laserSetInActive.getMbo(0).setValue("STATUSDATE", maximo.getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        strStatus="Inactive"
        
if (isBlank(strStatus) == False):
    laserSetActive.save()
    laserSetInActive.save()
    
    strSubjectline +="Laser "+ mbo.getString("assetnum")+ " status is changed to " +  strStatus  +"."
        
    strBody  ="<HTML><HEAD><TITLE>Laser status changed</TITLE></HEAD>"
    strBody +="<BODY>"
    strBody +="<TABLE>"
    strBody +="<TR><TD>"
   
    strBody +="<TR><TD>&nbsp;</TD></TR>"
    strBody += " The status of Laser " + " "
    strBody +=   mbo.getString("assetnum") + "  is changed to " + strStatus + "."
    strBody +=" Given below are the details of the laser: "
    strBody +="<TR><TD>"
    strBody +="<TABLE BORDER=1 ALIGN=LEFT>"
    strBody +="<TR><TD><B>Laser Number</B></TD><TD><B>"  + mbo.getString("assetnum") +"</B></TD></TR>"
    strBody +="<TR><TD><B>Description</B></TD><TD><B>" + mbo.getString("description")  +"</B></TD></TR>"
    strBody +="<TR><TD><B>Class</B></TD><TD><B>" + mbo.getString("laser_class")  +"</B></TD></TR>"
    strBody +="<TR><TD><B>Medium</B></TD><TD><B>" + mbo.getString("laser_medium")  +"</B></TD></TR>"
    strBody +="</TABLE>"
    strBody +="</TD></TR>"
    strBody +="<TR><TD>&nbsp;</TD></TR>"
    strBody +="</TD></TR>"
    strBody += "</TABLE></BODY></HTML>"
    
    strWhere = " orgid='" + mbo.getString("orgid")+ "'" + " and siteid='" + mbo.getString("siteid")+ "'"
    strWhere +=" and wonum='WFB208'" 
    workordersSet.setUserWhere(strWhere)
    wo=workordersSet.getMbo(0)
    wo.LblSendMail("smtp.lbl.gov", "PBhide@lbl.gov", "PBhide@lbl.gov", "", strSubjectline,  "HTML", strBody)







