################################################################
# Purpose: Script for object level (init) launch any MBO
#
# Author : Pankaj Bhide
#
# Date    : July 23, 2015
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


if (mbo.getName()=="LBL_WRHSFEEDDTL"):
    
    jIOOrgid="LBNL"
    jIOSiteid="FAC"



if (mbo.getName()=="LBL_WOWCDCONDITION"):   
     jIOPoints_readonly=True
        
        
    
    
    