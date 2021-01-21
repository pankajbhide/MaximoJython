################################################################
# Purpose: Script for object level (init) launch for lbl_wkthru
#          and its children tables
#
# Author : Pankaj Bhide
#
# Date    : July 14, 2015
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



if (mbo.getOwner() is not None and mbo.getOwner().getName().startswith("LBL")==True):
        
    jIOOrgid=mbo.getOwner().getString("orgid")
    jIOSiteid=mbo.getOwner().getString("siteid")
    jIOWkthruid=mbo.getOwner().getString("wkthruid")
    
if (mbo.getName()=='LBL_WKTHRU'):
    
    jIOOrgid="LBNL"
    jIOSiteid="FAC"
    if (onadd==False):
        jIOWkthruid_readonly=True
        
    
    
    