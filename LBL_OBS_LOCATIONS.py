#######################################################################
# Purpose: Script for object level launch LOCATIONS
#
# Author : Pankaj Bhide
#
# Date    : April 10, 2015
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


if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
    # Get the user restriction criteria for confined spaces
    strWhere1   =" orgid='LBNL' and siteid='FAC' and restrict_id='CONFSPACE-1' and app='LOCATIONS' "
    rowsSet= MXServer.getMXServer().getMboSet("lbl_restrict_cls", mbo.getUserInfo())
    rowsSet.setUserWhere(strWhere1)
    if (not rowsSet.isEmpty()):  
        # strClause will contain criteria to decide whether the location
        # is of type confined space
        strClause=rowsSet.getMbo(0).getString("clause")
        if (isBlank(strClause)):
            strClause="1=2" 
        # Look into locations table to find out whther the location
        # belongs to confined space
        strWhere1  =" orgid='LBNL' and siteid='FAC' and location='" + jILocation + "'"
        strWhere1 +=" and location " + strClause
        rows2Set= MXServer.getMXServer().getMboSet("locations", mbo.getUserInfo())
        rows2Set.setUserWhere(strWhere1)
        if (not rows2Set.isEmpty()):  # location belongs to confined spaces
            # Now look to see whether the logged in user belongs to the
            # confined space security group
            strWhere1  = "    1=(SELECT 1 "
            strWhere1 +="      from maximo.groupuser a, maximo.lbl_restrict_grp b "
            strWhere1 +="      where a.groupname=b.groupname "
            strWhere1 +="      and   b.orgid='LBNL'  "
            strWhere1 +="      and   b.siteid='FAC'  "
            strWhere1 +="      and   b.restrict_id='CONFSPACE-1'  "
            strWhere1 +="      and   b.app='LOCATIONS'  "
            strWhere1 +="      and   upper(a.userid)=" + "'" + user.upper() + "'"
            strWhere1 +="    )"
            rows3Set= MXServer.getMXServer().getMboSet("organization", mbo.getUserInfo())
            rows3Set.setUserWhere(strWhere1)
            if (rows3Set.isEmpty()):  
                setError("lbl_confspnotallowed","locations","")

        rowsSet=None
        rows2Set=None
        rows3Set=None