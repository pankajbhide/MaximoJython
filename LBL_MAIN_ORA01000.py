##########################################################################
# Purpose: Script for activating the GL Components 

# Author : Pankaj Bhide
#
# Date    : Sept 15, 2018
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
from psdi.app.financial import GLComponents

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

myGLComponentsSet = mxServer.getMboSet('GLCOMPONENTS', runAsUserInfo1 )

        

strWhere  =" active=0 and lbl_project_id is not null and lbl_project_id like '101%'"

myGLComponentsSet.setWhere (strWhere)
myGLComponentsSet.reset()

if myGLComponentsSet is not None:
    intCount1=myGLComponentsSet.count()
    # Loop through each row from the collection
    for i in xrange(intCount1):
        
        print "Processing GLComp "  + myGLComponentsSet.getMbo(i).getString("compvalue")
        myGLComponentsSet.getMbo(i).setValue("active",True,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
    myGLComponentsSet.close()
    myGLComponentsSet.save()    