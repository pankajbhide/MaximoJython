###############################################################
# Purpose: Script for object  level (save) launch 
#          on LBL_WOWCDCONDITION
#
# Author : Pankaj Bhide
#
# Date    : August 25, 2015
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

    
def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
    # Get all the records having point > 0 and find out
    #its highest level number. Find out the sum of the points
    # for the highest level number. Determine WCD based upon
    # the total points
    
    dblTotalpoints=0
    intCategory=0
    intHigestLevel=0
    mboThisSet = mbo.getThisMboSet()
    arrayList = []       
    if (not mboThisSet.isEmpty()):
                
        intCount=mboThisSet.count()                           
        for i in xrange(intCount): 
            if (isBlank(mboThisSet.getMbo(i).getString("answer"))== False):
                arrayList.append(int(mboThisSet.getMbo(i).getInt("wcd_level")))
                
        if (len(arrayList) >0):            
            arrayList.sort(reverse=True)
            intHigestLevel=arrayList[0]
            
    #Get the total of points for the highest level number
    if (not mboThisSet.isEmpty()):
                
        intCount=mboThisSet.count()                           
        for i in xrange(intCount): 
            if  (mboThisSet.getMbo(i).getInt("wcd_level")==intHigestLevel and mboThisSet.getMbo(i).getDouble("points") >=0):
                dblTotalpoints +=mboThisSet.getMbo(i).getInt("points")
                
                
       
    #Find out the WCD level by comparing total points
    wcdCategorySet = MXServer.getMXServer().getMboSet("LBL_WCDCATEGORY", mbo.getUserInfo())       
    strWhere = "ACTIVE = 1 and wcd_level = " + str(intHigestLevel)
          
    wcdCategorySet.setUserWhere(strWhere)
    if (not wcdCategorySet.isEmpty()):
        intCount=wcdCategorySet.count()                           
        for i in xrange(intCount):
            wcdCategory = wcdCategorySet.getMbo(i)
         
            if ((dblTotalpoints >= wcdCategory.getDouble("MIN_TOTALPOINTS")) and (dblTotalpoints <= wcdCategory.getDouble("MAX_TOTALPOINTS"))):
                intCategory = wcdCategory.getInt("LBL_WCDCATEGORY")
                
                break
            
     
    maximo = MXServer.getMXServer()
    jOChangedate= maximo.getDate()
    jOChangeby = user  # variable provided by scripting framework
    
    wo=mbo.getOwner()
    if (wo is not None):
        wo.setValue("lbl_wcdcatg_calc", str(intCategory),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        wo.setValue("lbl_wcdlvl_calc",  intHigestLevel, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        wo.setValue("lbl_wcdtotalpoints", dblTotalpoints,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        if (isBlank(wo.getString("lbl_wcdcatg_finl")) == True):
            wo.setValue("lbl_wcdcatg_finl", str(intCategory),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)