#################################################### 
# Purpose: Validate the value of release requird
#
# Author : Pankaj Bhide
#
# Date    : August 20, 2015
#
# Revision
# History : Dec 6, 2016 Revised script to remove sitid
#
######################################################

from psdi.server import MXServer
from psdi.util import MXApplicationException
from java.util import HashMap


def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams",errparm)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)



if ( jIOrgid == 'LBNL'):
    
    if (mbo.getString("lbl_rel_reqd") is not None):
        
       if (mbo.getString("lbl_rel_reqd") != 'Y' and mbo.getString("lbl_rel_reqd") !='N'):        
           setError("lbl_invalidrelreqd","lbl_auth_release","for work type: " +mbo.getString("worktype"))
       else:
           
           # Allow changing release required =N only
           # if there are zero work orders whose status =WREL against
           # that work type 
           if (mbo.getString("lbl_rel_reqd") =='N'):
        
                        # Check whether the value entered is valid
            # Get reference to person collection
            workorderSet = MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())       
            strWhere = "worktype='" + mbo.getString("worktype") + "'" + " and status in (" +"'" + "WREL" +"'" + ")"                
            workorderSet.setUserWhere(strWhere)
            if (workorderSet.isEmpty()):
                workorderSet = None                
            else:
                workorderSet = None                
                setError("lbl_woopenforyes","lbl_auth_release","for work type: " +mbo.getString("worktype")) 
               