#######################################################
# Purpose: Library script for returning the
#          FAM information
#
# Author : Pankaj Bhide
#
# Date    : Aug 5, 2016
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

    
strFamid=""
strFammanagerid=""
strDelim="_"
strFAMInfo=""
strPlanner_group=""
boolFamreqd=True

#logger = mbo.getMboLogger()   
#logger.info("PRB mbo name : " + mbo.getName())


#######################################################
# Please note that mbo referred in this script is an
# "argument" passed by the call script. 
#######################################################

if (isBlank(mbo.getString("COMMODITY") == False) and (mbo.getString("COMMODITY")=='03' or mbo.getString("COMMODITY")=='09' or mbo.getString("COMMODITY")=='19')):    
    boolFamreqd=False;

if (isBlank(mbo.getString("worktype")) == False and boolFamreqd == True):              
    
    strWhere=" worktype='" + mbo.getString("worktype") + "'"
    
    WorktypeSet= MXServer.getMXServer().getMboSet("worktype", mbo.getUserInfo())
    WorktypeSet.setUserWhere(strWhere)
    if (not WorktypeSet.isEmpty()):
        boolFamreqd=WorktypeSet.getMbo(0).getBoolean("lbl_famreqd")
    
    WorktypeSet=None
        
if (boolFamreqd == True):            

    if (isBlank(mbo.getString("location")) == False):              
                                     
        #Find out FAM id for the given location
        
        strWhere =" location in (select a.lo1 from locations a where a.location='" + mbo.getString("location") + "' "
        strWhere +=" union select b.location from maximo.lbl_v_famlocation b where b.type='I' and "
        strWhere +=" b.location in (select c.ancestor from maximo.locancestor c where c.location='" + mbo.getString("location") + "' ) )"
    
        FAMBldgSet= MXServer.getMXServer().getMboSet("lbl_famlocation", mbo.getUserInfo())
        FAMBldgSet.setUserWhere(strWhere)
                       
                    
        if (not FAMBldgSet.isEmpty()):
            strFamid=FAMBldgSet.getMbo(0).getString("famid")
            
        FAMBldgSet=None
    
            
    if (isBlank(strFamid) == True):
        strFamid="FAMTBD"            
    
    
    #JIRA EF-8636 Added to get default Planner group
    strWhere=" famid='" + strFamid +"'"
    FAMSet=MXServer.getMXServer().getMboSet("lbl_fam", mbo.getUserInfo())
    FAMSet.setUserWhere(strWhere)
                       
                
    if (not FAMSet.isEmpty()):
        strPlanner_group=FAMSet.getMbo(0).getString("planner_group")
        
            
    FAMSet=None
    
    # Tammy T requested to remove this default (Feb 19, 2019)
    #
    #if (isBlank(strPlanner_group)==True):
    #    strPlanner_group="FAP20"
           
            
    # Find out primary manager responsible for the FAM
    strWhere="persongroup='" + strFamid + "' and groupdefault=1"
    FAMMgrSet= MXServer.getMXServer().getMboSet("PERSONGROUPTEAM", mbo.getUserInfo())
    FAMMgrSet.setUserWhere(strWhere)
                
    if (not FAMMgrSet.isEmpty()):
        strFammanagerid=FAMMgrSet.getMbo(0).getString("respparty")
         
    #if (isBlank(strFamid) == False and isBlank(strFammanagerid)== False and isBlank(strPlanner_group)== False):
    #JIRA EF-9121 No need to derive planner group
    if (isBlank(strFamid) == False and isBlank(strFammanagerid)== False ):
        #strFAMInfo=strFamid + strDelim + strFammanagerid + strDelim + strPlanner_group
        strFAMInfo=strFamid + strDelim + strFammanagerid 
    
    
