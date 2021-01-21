################################################################
# Purpose: Script for object level (init) launch for lbl_fam 
#          and its children tables
#
# Author : Pankaj Bhide
#
# Date    : June 28, 2016
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


if (mbo.getName() == "LBL_FAM"):
    if (onadd==True):
        jIOFamid_readonly=False
    else:
        jIOFamid_readonly=True



if (mbo.getOwner() is not None and mbo.getOwner().getName().startswith("LBL_FAM")==True):    
    
    mbo.setValue("famid", mbo.getOwner().getString("famid"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    

    
    