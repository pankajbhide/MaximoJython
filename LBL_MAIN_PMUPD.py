##########################################################################
# Purpose: Script for changing PM data 

# Author : Pankaj Bhide
#
# Date    : Dec  7 2017
#
# Revision
# History : 
#
######################################################
import time
from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


    
#########################################################
       
# Open MXServer session
mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")


# Create SetRemotes
pmSetRemote           = MXServer.getMXServer().getMboSet("PM", runAsUserInfo1)

pmSetRemote.setUserWhere("status='ACTIVE' and assetnum not in (select b.assetnum from asset b where classstructureid='00001034')")
pmSetRemote.reset()

# Read all the rows from PM collection 
if (not pmSetRemote.isEmpty()):
   
    intCount=pmSetRemote.count()
    # Loop through each row from the collection
    for i in xrange(intCount):
        
        pmSetRemote.getMbo(i).setValue("leadtime","60",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        pmSetRemote.getMbo(i).setValue("changedate", MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        pmSetRemote.getMbo(i).setValue("changeby", "IT-BS-MXINTADM",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        pmSetRemote.getMbo(i).setValue("lbl_targ_strt_fin_days",0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        print "Updated PM record: " + pmSetRemote.getMbo(i).getString("pmnum")
  
     
    pmSetRemote.save()
pmSetRemote.close()
   
                    
         