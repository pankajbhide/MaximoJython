#############################################
# Purpose: Library script for returning the
#          release status of the work orders 
#
# Author : Pankaj Bhide
#
# Date    : Aug 5, 2015
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

    
strReleaseStatus=""


logger = mbo.getMboLogger()   
 #logger.info("PRB mbo name : " + mbo.getName()) 

#######################################################
# Please note that mbo referred in this script is an
# "argument" passed by the call script. 
#######################################################

strStatus=mbo.getString("status")

# For new work order status could be null 
if (isBlank(strStatus)== True):
    strStatus='WAPPR'
    
strReleaseStatus=mbo.getReleaseStatus(strStatus)

####################################################################
# All the following lines have been commented as the release status 
# is presently derived from the "getReleaseStatus" method of the java
# class associated with work order object.

# The release status also needs to be derived from "changestatus" method.
# Since, I could not find an easier way of calling jython function from
# a java class, I decided to keep the logic of finding release status
# in java class itself.
#
# #For task work order, the release status is always not required.
# 
# 
# 
# if (mbo.getBoolean("istask") == True):
#     strReleaseStatus="NOT REQUIRED"
#     
# if (isBlank(mbo.getString("location"))== True):
#      strReleaseStatus="UNKNOWN"
#   
#  
# if (isBlank(strReleaseStatus) == True):
#     
#     # Do not find out release status if the release status is  RELEASED or WAITING RELEASE
#     
#     if (mbo.getString("lbl_release_status")=="RELEASED" or
#         mbo.getString("lbl_release_status")=="WAITING RELEASE"):
#             strReleaseStatus=mbo.getString("lbl_release_status")
#                           
#     # IF RFI do not derive new status as long as location, worktype and commodity group do not change     
#     if ((mbo.getString("lbl_release_status")=="REQUEST FOR INFORMATION" ) and
#         (mbo.getString("location")==mbo.getMboValue("location").getPreviousValue().asString()) and
#         (mbo.getString("worktype")==mbo.getMboValue("worktype").getPreviousValue().asString()) and
#         (mbo.getString("commoditygroup")==mbo.getMboValue("commoditygroup").getPreviousValue().asString())):
#             strReleaseStatus=mbo.getString("lbl_release_status")
#         
#               
# if (isBlank(strReleaseStatus) == True):
#     
#     # If the work order reaches beyond INPRG, then do not derive
#     # release status. Return the release status as it is.
# 
#     strWhere   =" domainid='WOSTATUS' and maxvalue in ('INPRG','COMP','CLOSE') "
#     strWhere  +=" and value='" + mbo.getString("status") + "'"
#     
#     synonymdomainSet= MXServer.getMXServer().getMboSet("SYNONYMDOMAIN", mbo.getUserInfo())
#     synonymdomainSet.setUserWhere(strWhere)                
#         
#     if (not synonymdomainSet.isEmpty()):
#         strReleaseStatus=mbo.getString("lbl_release_status")
#         synonymdomainSet=None
#         
# 
# if (isBlank(strReleaseStatus) == True):        
#     # Find out whether the location requires release
#     
#     strWhere   =" siteid='"        + mbo.getString("siteid")   + "'"
#     strWhere  +=" and location='"  + mbo.getString("location") + "'"
#     
#     locationsSet= MXServer.getMXServer().getMboSet("LOCATIONS", mbo.getUserInfo())
#     locationsSet.setUserWhere(strWhere)                
#   
#     
#     if (not locationsSet.isEmpty()):
#         strRelReqd=locationsSet.getMbo(0).getString("lbl_rel_reqd")
#         
#         if (strRelReqd =="N"):
#              strReleaseStatus="NOT REQUIRED"
#         
#             
#     locationsSet=None
#     
#     
# if (isBlank(strReleaseStatus) == True):
#     
#     #  Now check whether the location belongs to infrastructure system.
#     #  If it belongs to, then, release_status=NOT REQUIRED
#     strWhere  =" siteid='"+ mbo.getString("siteid") +"'"
#     strWhere +=" and location='" + mbo.getString("location") +"'"
#     strWhere +=" and " + "'" + mbo.getString("location") +"'" 
#     strWhere +=" in (select b.location from locancestor b where b.siteid='" 
#     strWhere += mbo.getString("siteid") + "'" + " and b.ancestor='I' and b.location='" 
#     strWhere += mbo.getString("location") +"')"
#     locationsSet= MXServer.getMXServer().getMboSet("LOCATIONS", mbo.getUserInfo())
#     locationsSet.setUserWhere(strWhere)                
#         
#     if (not locationsSet.isEmpty()):
#         strReleaseStatus="NOT REQUIRED"
#     locationsSet=None
#     
#     
# if (isBlank(strReleaseStatus) == True):
#     # Look for the value of commodity group (service group) in alndomain=LBL_EXEMPT_REL_SG
#     # If found, then, release not required.      
#         
#     if (isBlank(mbo.getString("commoditygroup")) == False):
#         
#         strWhere   =" domainid='LBL_EXEMPT_REL_SG' "
#         strWhere  +=" and value='" + mbo.getString("commoditygroup") + "'"
#         
#         alnDomainSet= MXServer.getMXServer().getMboSet("ALNDOMAIN", mbo.getUserInfo())
#         alnDomainSet.setUserWhere(strWhere)                
#         
#         if (not alnDomainSet.isEmpty()):
#              strReleaseStatus="NOT REQUIRED"
#         alnDomainSet=None
#         
# 
# if (isBlank(strReleaseStatus) == True):
#     # Check whether the work type required release
#     
#     if (isBlank(mbo.getString("worktype")) == False):
#         
#         strWhere="worktype=" + "'" + mbo.getString("worktype") +"'"      
#         worktypeSet= MXServer.getMXServer().getMboSet("WORKTYPE", mbo.getUserInfo())
#         worktypeSet.setUserWhere(strWhere)
#                 
#         
#         if (not worktypeSet.isEmpty()):
#             strRelReqd=worktypeSet.getMbo(0).getString("lbl_rel_reqd") 
#             
#             if (strRelReqd=="N"):
#                 strReleaseStatus="NOT REQUIRED"
#                                 
#         worktypeSet=None
# 
# 
# if (isBlank(strReleaseStatus) == True):
#             
#     # Parent work order and not PM work order
#           if (mbo.getBoolean("haschildren") == True):
#                                                            
#               if ( (mbo.getString("worktype").lower().startswith('pm')) == False):
#                   strReleaseStatus="NOT REQUIRED"
#                   
#               if (isBlank(strReleaseStatus) == True):
#                   # Release not required if work order generated via PM with route (confined space)
#                   if isBlank(mbo.getString("pmnum") == False):
#                       ## Find out whether the PM is generated from route
#                       strWhere   =" siteid='" + mbo.getString("siteid") + "'"
#                       strWhere  +=" and pmnum='"  + mbo.getString("pmnum") +"'"
#                       pmSet= MXServer.getMXServer().getMboSet("PM", mbo.getUserInfo())
#                       pmSet.setUserWhere(strWhere)                
#                       
#                       if (not pmSet.isEmpty()):
#                           if (isBlank(pmSet.getMbo(0).getString("route")) == False):                           
#                             strReleaseStatus="NOT REQUIRED"
#                       pmSet=None
# 
#                        
# if (isBlank(strReleaseStatus) == True):
#     
#     #  If release is required, then, check at-least one authorizer is active
#     #  for that location
#     
#    strWhere    ="  location='" + mbo.getString("location") + "'" 
#    strWhere   +="  and personid is not null"
#    strWhere   += " and location in (select b.location from lbl_auth_release b, person c "
#    strWhere   +="  where b.location='" + mbo.getString("location") + "'" 
#    strWhere   +="  and b.personid=c.personid and c.lbl_status='A')"
#    locationsSet= MXServer.getMXServer().getMboSet("LBL_AUTH_RELEASE", mbo.getUserInfo())
#    locationsSet.setUserWhere(strWhere)
#    
#    if (not locationsSet.isEmpty()):
#        strReleaseStatus="REQUIRED"
#            
#                      
# if (isBlank(strReleaseStatus) == True):
#         strReleaseStatus="UNKNOWN"     
#         
#        
#        
#########################################################################################

    
    
                        
                       
                    
                      
                      
                      
            

                    
                
        