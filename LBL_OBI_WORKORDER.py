################################################################
# Purpose: Script for object level launch for workorder
#          (init only)
# Author : Pankaj Bhide
#
# Date    : July 29 , 2015
#
# Revision
# History : Aug 4, 2016 - Make lbl_fammanager
#
######################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer



if (jIOrgid=="LBNL" and jISiteid=="FAC"):

    # Make the fields read-Only (always)
    if (jIStatus is not None):


        jIOWonum_readonly = True    # work order number

        jIOWo4_readonly=True
        jIOChangeby_readonly=True
        jIOChangedate_readonly=True

        boolAdminUser=False

        # jIFacadmin contains a list of Facilities Administrators separated by comma.
        # This is indicated by a system property titled lbl.fac_admin_logins
        # The following code parses the string and determines  whether the logged in
        # user is admin or not.

        listFacAdmins =  jIFacadmin.split(",")

        for strAdmin in listFacAdmins:

            if (strAdmin.lower()==user.lower()):
                boolAdminUser= True
                break




        if (jIOLbl_dtsenttofms is not None): # and boolAdminUser == False):
            jIOGlaccount_readonly = True

        if (boolAdminUser == False):
           jIOLbl_woenteredby_readonly=True



        #If work order status reaches beyond in progress
        # JIRA EF-5386  -- PRESENTLY COMMENTED FOR SCHEDULER ---
        #if (jIStatus_internal in ('INPRG','COMP','CLOSE')):
        #    mbo.setFieldFlag("TARGSTARTDATE", MboConstants.READONLY,True)
        #    mbo.setFieldFlag("TARGCOMPDATE", MboConstants.READONLY,True)
        #    mbo.setFieldFlag("SCHEDSTART", MboConstants.READONLY,True)
        #    mbo.setFieldFlag("SCHEDFINISH", MboConstants.READONLY,True)

        #If work order status reaches beyond approval
        if (jIStatus_internal != "WAPPR"):
            jIOGlaccount_readonly = True

            #jIOSupervisor_readonly= True
            jIOWorktype_readonly= True

            #jIODescription_readonly = True
            jIOPhone_readonly = True
            jIOWo1_readonly=True
            jIOWo5_readonly=True
            jIOReportedby_readonly=True
            jIOReportdate_readonly=True
            jIOCommoditygroup_readonly=True
            jIOCommodity_readonly=True
            #jIOLeadcraft_readonly=True
            jIOParent_readonly=True
            jIOPmnum_readonly=True
            # Added on Aug 3, 2016
            mbo.setFieldFlag("lbl_fammanager", MboConstants.READONLY,True)
        # JIRA EF=7516
        # Previously these fields were made read-only once the status of the work order
        # is changed to APPR. For PM, the location and asset number is always read-only
        if (jIStatus=="WREL" or (mbo.getString("worktype").startswith("PM") and (jIStatus_internal != "WAPPR"))):
          jIOLocation_readonly =True
          jIOAssetnum_readonly = True