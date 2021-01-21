####################################################
# Purpose: Common script for attribute level action
#          launch for various fields of work order
#          object
#
# Author : Pankaj Bhide
#
# Date    : Aug 7 2015
#
# Revision
# History : Modified Praveen Muramalla Sep, 30 2016
#           Retrieve Supervisor / Lead / Service Group
#           when worktype is ET
#
#           Feb 3,17 Pankaj - Fixed the issue while
#           generating the next work order number.
######################################################

from psdi.server import MXServer
from psdi.mbo  import   MboConstants
from psdi.util import MXFormat
from java.util import Date
from java.util import Calendar
from java.util import HashMap
from psdi.app.item import ItemSetRemote
from psdi.util.logging import MXLoggerFactory



def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def getLblmaxvarvalue(strVarname):
    strLblvarvalue=None
    lblmaxvarSet = MXServer.getMXServer().getMboSet("LBL_MAXVARS", mbo.getUserInfo())
    lblmaxvarSet.setUserWhere("varname='" + strVarname +"' and orgid='" + jIOrgid +"' and siteid='" + jISiteid+"' ")
    if (not lblmaxvarSet.isEmpty()):
                strLblvarvalue=lblmaxvarSet.getMbo(0).getString("varvalue")
    lblmaxvarSet=None
    return strLblvarvalue

def setLBLFacTime(strVarname, strType):

    arr = strVarname.split("-")
   
    myMonth=int(arr[1])-1  # starts with zero
    myDay=int(arr[2])
    myYear=int(arr[0])     
    
    
      
    cal=Calendar.getInstance()
            
    cal.set(Calendar.YEAR,   myYear)
    cal.set(Calendar.MONTH,  myMonth)
    cal.set(Calendar.DAY_OF_MONTH, myDay)
    if (strType=="START"):     
        cal.set(Calendar.HOUR_OF_DAY, 7)
        cal.set(Calendar.MINUTE, 0)
        cal.set(Calendar.SECOND, 1)
    if (strType=="END"):
        cal.set(Calendar.HOUR_OF_DAY,23)
        cal.set(Calendar.MINUTE, 59)
        cal.set(Calendar.SECOND, 1)

    return cal.getTime()
                            
   

myLogger = MXLoggerFactory.getLogger("maximo.script.customscript")

ctx = HashMap()
ctx.put("mbo",mbo)
myLogger.debug("PRB at start")


if ( jIOrgid == 'LBNL' and jISiteid == 'FAC'):
    
    
    
    if (jIFieldname=="TARGSTARTDATE" or jIFieldname=="TARGCOMPDATE" or jIFieldname=="SCHEDSTART" or jIFieldname=="SCHEDFINISH"):
        
        if (not mbo.isNull("TARGSTARTDATE")):
            date1=MXFormat.dateToSQLString(mbo.getDate("TARGSTARTDATE"))
            date2=setLBLFacTime(date1,"START")
            mbo.setValue("TARGSTARTDATE", date2, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

        if (not mbo.isNull("TARGCOMPDATE")):
            date1=MXFormat.dateToSQLString(mbo.getDate("TARGCOMPDATE"))
            date2=setLBLFacTime(date1,"END")
            mbo.setValue("TARGCOMPDATE", date2, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

        if (not mbo.isNull("SCHEDSTART")):
            date1=MXFormat.dateToSQLString(mbo.getDate("SCHEDSTART"))
            date2=setLBLFacTime(date1,"START")
            mbo.setValue("SCHEDSTART", date2, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

        if (not mbo.isNull("SCHEDFINISH")):
            date1=MXFormat.dateToSQLString(mbo.getDate("SCHEDFINISH"))
            date2=setLBLFacTime(date1,"END")
            mbo.setValue("SCHEDFINISH", date2, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)


    ###############################
    # Duration for MAXIMO Scheduler
    ###############################

    if (jIFieldname=='ESTDUR'):
          strLblestdur=str(mbo.getFloat("estdur"))
          mbo.setValue("lbl_estdur", strLblestdur, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

    ################
    # Reported by
    #################
    if (jIFieldname=="REPORTEDBY"):


        if (isBlank(mbo.getString("wo1")== True)):
            mbo.setValue("wo1", mbo.getString("reportedby"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

        if (isBlank(mbo.getString("onbehalfof")== True)):
            mbo.setValue("onbehalfof", mbo.getString("reportedby"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

        # If the phone is empty and the look up into phone table
        # with the desired reportedby

        strOldReportedby=""
        strOldReportedby=mbo.getMboValue("reportedby").getPreviousValue().asString()
        if (isBlank(mbo.getString("phone"))== True) or (strOldReportedby != mbo.getString("reportedby")):
            # Get reference to phone  collection
            phoneSet = MXServer.getMXServer().getMboSet("PHONE", mbo.getUserInfo())
            strWhere = "personid='" + mbo.getString("reportedby") + "'"

            phoneSet.setUserWhere(strWhere)
            if (not  phoneSet.isEmpty()):
                mbo.setValue("phone", phoneSet.getMbo(0).getString("phonenum"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            phoneSet = None
            strWhere = None


    #################################################
    if (jIFieldname=="JPNUM"):

         # Get Release status
        service.invokeScript("LBL_LIB_GETRELEASESTATUS",ctx)
        # The variable "strReleaseStatus" is returned from the library script
        strReleaseStatus=str(ctx.get("strReleaseStatus"))

        mbo.setValue("lbl_release_status", strReleaseStatus,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 

    #################
    # Work type
    #################
    if (jIFieldname=="WORKTYPE"):

        

        # Get Release status
        service.invokeScript("LBL_LIB_GETRELEASESTATUS",ctx)
        # The variable "strReleaseStatus" is returned from the library script
        strReleaseStatus=str(ctx.get("strReleaseStatus"))
        mbo.setValue("lbl_release_status", strReleaseStatus,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        
        #######################################################################################
        # If emerency work type, then, set target start/end and scheduled start/end dates
        # as today's date for starting 7 AM and for end 11:59 pm
        #######################################################################################
        
        if (mbo.getString("worktype")== 'EM'):
            
            cal1=Calendar.getInstance()
            cal2=Calendar.getInstance()
            
            cal2.set(Calendar.YEAR,   cal1.get(Calendar.YEAR))
            cal2.set(Calendar.MONTH,   cal1.get(Calendar.MONTH))
            cal2.set(Calendar.DATE,   cal1.get(Calendar.DATE))
            
            cal2.set(Calendar.HOUR,   7)
            cal2.set(Calendar.MINUTE, 0)
            cal2.set(Calendar.SECOND,   1)
            
            mbo.setValue("TARGSTARTDATE",cal2.getTime(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("SCHEDSTART",cal2.getTime(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                       
            cal2.set(Calendar.HOUR,   23)
            cal2.set(Calendar.MINUTE, 59)
            cal2.set(Calendar.SECOND,  0)
            mbo.setValue("TARGCOMPDATE",cal2.getTime(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("SCHEDFINISH",cal2.getTime(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
        #logger = mbo.getMboLogger()
       

        ## Set schedule start and end date for worktype='CM-OS'

        if (mbo.getString("worktype")== 'CM-OS'):

            mbo.setValue("schedstart", MXServer.getMXServer().getDate(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            cal=Calendar.getInstance()
            cal.setTime(MXServer.getMXServer().getDate())
            cal.add(Calendar.DATE, +1)  # next day
            mbo.setValue("schedfinish",cal.getTime(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

        # Get FAM Information
        strOwnergroup=""
        strOwner=""
        strFAMCombined=""
        strPlanner_group=""
        service.invokeScript("LBL_LIB_GETFAMINFO",ctx)
        # The variable "strReleaseStatus" is returned from the library script
        strFAMInfo=str(ctx.get("strFAMInfo"))

        if (isBlank(strFAMInfo) == False):
            strFAMCombined=strFAMInfo.split("_")

        # for each word in the line:
        for i, val in enumerate(strFAMCombined):

            if (i==0):
                strOwnergroup=val
            if (i==1):
                strOwner=val
            if (i==2):
                strPlanner_group=val

        mbo.setValue("lbl_famid", strOwnergroup,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        mbo.setValue("lbl_fammanager", strOwner,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        #mbo.setValue("lbl_planner_group", strPlanner_group,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

        if (mbo.getString("worktype")== 'ET'):
            strWoEstSupervisor=getLblmaxvarvalue("WOESTREQ_SUPERVISOR")
            strWoEstLead=getLblmaxvarvalue("WOESTREQ_LEAD")
            #strWoEstCommodityGroup=getLblmaxvarvalue("WOESTREQ_COMMODITYGROUP")
            strWoEstCommodityGroup="FAESTIMATE"


            mbo.setValue("SUPERVISOR", strWoEstSupervisor, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("LEAD",strWoEstLead, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("COMMODITYGROUP",strWoEstCommodityGroup, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)


   

    #################################################
    # Location, commodity group, COMMODITY, assetnum
    #################################################
    if (jIFieldname=="LOCATION" or jIFieldname=="COMMODITYGROUP" or jIFieldname=="ASSETNUM" or jIFieldname=="COMMODITY" ):


         # Get Release status
        service.invokeScript("LBL_LIB_GETRELEASESTATUS",ctx)
        # The variable "strReleaseStatus" is returned from the library script
        strReleaseStatus=str(ctx.get("strReleaseStatus"))

        mbo.setValue("lbl_release_status", strReleaseStatus,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

        # Added by Pankaj on 11/25/15 as per request from John C and Tammy T
        # Bring the values of  conditional release and escort required for that location to the work order.
        strWhere="siteid='" + mbo.getString("siteid") + "' and location='" + mbo.getString("location") + "'"
        locationsSet= MXServer.getMXServer().getMboSet("LOCATIONS", mbo.getUserInfo())

        locationsSet.setUserWhere(strWhere)
        if (not locationsSet.isEmpty()):

             mbo.setValue("lbl_escort_reqd", locationsSet.getMbo(0).getString("lbl_escort_reqd"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             mbo.setValue("lbl_condition_rel", locationsSet.getMbo(0).getString("lbl_cond_release"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             mbo.setValue("LBL_CONDITION_REL_LONGDESCRIPTION", locationsSet.getMbo(0).getString("lbl_comments_condr"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        locationsSet=None



        if (jIFieldname=="LOCATION" or jIFieldname=="COMMODITY" or jIFieldname=="ASSETNUM" ):

            strOwnergroup=""
            strOwner=""
            strPlanner_group=""

            # Get FAM Information
            service.invokeScript("LBL_LIB_GETFAMINFO",ctx)
            # The variable "strReleaseStatus" is returned from the library script
            strFAMInfo=str(ctx.get("strFAMInfo"))

            if (isBlank(strFAMInfo) == False):
                strFAMCombined=strFAMInfo.split("_")


                # for each word in the line:
                for i, val in enumerate(strFAMCombined):

                    if (i==0):
                        strOwnergroup=val
                    if (i==1):
                        strOwner=val
                    if (i==2):
                        strPlanner_group=val
               

            mbo.setValue("lbl_famid", strOwnergroup,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("lbl_fammanager",      strOwner,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            # Do not derive the value of planner group Panakj Mar 5, 19
            #if (isBlank(strPlanner_group) == False):
            #    mbo.setValue("lbl_planner_group", strPlanner_group,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            #if (isBlank(strPlanner_group) == True):
            #     mbo.setValueNull("lbl_planner_group", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                 
            # Per Beth S and Tammy T - Asset number should not auto populated after user enters location  
            if (jIFieldname=="LOCATION"):
                if (mbo.isNull("PMNUM")==True):
                    mbo.setValue("assetnum", "",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
        ########################################################            
        #JIRA EF-8907 Bring over field from asset to work order
        ########################################################            
        if (jIFieldname=="ASSETNUM"):
            
            if isBlank(mbo.getString("assetnum") == True):
                mbo.setValueNull("lbl_assetcritical", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            
            if isBlank(mbo.getString("assetnum") == False):
                 
                strWhere="siteid='" + mbo.getString("siteid") + "' and assetnum='" + mbo.getString("assetnum") + "'"
                assetSet= MXServer.getMXServer().getMboSet("ASSET", mbo.getUserInfo())

                assetSet.setUserWhere(strWhere)
                if (not assetSet.isEmpty()):
                    mbo.setValue("lbl_assetcritical", assetSet.getMbo(0).getString("lbl_assetcritical"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetSet=None
                        
                
                

    #####################
    # Work order number
    #######################
    if (jIFieldname=="WONUM"):
        lblmaxvarsSet= MXServer.getMXServer().getMboSet("LBL_MAXVARS", mbo.getUserInfo())
        # Read the desired length of the work order
        # from lbl_maxvars table

        strWhere="varname='LBL_WOLENGTH' and orgid='" + jIOrgid + "' and siteid='" + jISiteid +  "'"

        lblmaxvarsSet.setUserWhere(strWhere)
        lblmaxvars= lblmaxvarsSet.getMbo(0)
        intWoLength=int(lblmaxvars.getString("varvalue"))
        lblmaxvarsSet = None

        # If the length of the generated work order number is greater
        # than the desired length, then, format the number
        if (len(mbo.getString("wonum")) > intWoLength):

             prefix=mbo.getString("wonum")[0]  # get prefix
             suffix=mbo.getString("wonum")[1:] # get unformatted suffix
             # format suffix
             #temp1=str(int(suffix)) # convert to integer to get rid of zeros
             # Revised by Pankaj on 2/3/17 
             temp=suffix.lstrip('0')
             suffix=temp.zfill(intWoLength-1) # prefix zeros

             # Associate formatted suffix to work order number
             temp1=prefix + suffix
             mbo.setValue("wonum", temp1,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
             #Make it read-only
             mbo.setFieldFlag("WONUM", mbo.READONLY, 1)
             
    ##########################################################################
    # Planner group
    # If the value of the planner group is not null, then,
    # get the default planner for the planner group and assign to lbl_planner
    ##########################################################################
    if (jIFieldname=="LBL_PLANNER_GROUP"):
        mbo.setValue("lbl_planner", "", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        if (isBlank(mbo.getString("LBL_PLANNER_GROUP")) == False):
            
            persongroupteamSet= MXServer.getMXServer().getMboSet("PERSONGROUPTEAM", mbo.getUserInfo())
                        
            strWhere="persongroup='" + mbo.getString("LBL_PLANNER_GROUP") + "' and groupdefault=1"
            persongroupteamSet.setUserWhere(strWhere)
            if (not persongroupteamSet.isEmpty()):            
                mbo.setValue("lbl_planner", persongroupteamSet.getMbo(0).getString("resppartygroup"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            persongroupteamSet = None         
            
        

    ######################
    # Walk through number
    #######################
    if (jIFieldname=="LBL_WKTHRUID"):

        # If value of previous walk thru id is not null
        # then, delete all its associated records
        if (isBlank(lbl_wkthruid_previous) == False):

            remoteSet= mbo.getMboSet("LBL_WO2WOWKTHRU")
            if (not remoteSet.isEmpty()):
                 lngWOWkthruOwnerid= remoteSet.getMbo(0).getLong("lbl_wowkthruid")

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            remoteSet= mbo.getMboSet("LBL_WO2WOWKTHOPS")
            if (not remoteSet.isEmpty()):

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            remoteSet= mbo.getMboSet("LBL_WO2WOWKTHHAZ")
            if (not remoteSet.isEmpty()):

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            # Added to cleanup wosafetlink records JIRA EF-4634
            remoteSet= mbo.getMboSet("LBL_WO2WOSAFETLINK")
            if (not remoteSet.isEmpty()):

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            remoteSet= mbo.getMboSet("LBL_WO2WOWKTHMAT")
            if (not remoteSet.isEmpty()):

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            remoteSet= mbo.getMboSet("LBL_WO2WOWKTHRESALL")
            if (not remoteSet.isEmpty()):

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            remoteSet= mbo.getMboSet("LBL_WO2WOWKFEEDBACK")
            if (not remoteSet.isEmpty()):

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            strWhere  = " ownerid=" + str(mbo.getInt("WORKORDERID")) + " and DOCTYPE='WKTHRU' and ownertable='LBL_WOWKTHRU' "
            remoteSet = MXServer.getMXServer().getMboSet("DOCLINKS", mbo.getUserInfo())
            remoteSet.setUserWhere(strWhere)
            if (not remoteSet.isEmpty()):
                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            #Also delete from wplabor and wpitem
            remoteSet= mbo.getMboSet("WPLABOR")
            if (not remoteSet.isEmpty()):

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

            remoteSet= mbo.getMboSet("WPITEM")
            if (not remoteSet.isEmpty()):

                 intCount=remoteSet.count()
                 for i in xrange(intCount):
                     remoteSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)


        if (isBlank(mbo.getString("lbl_wkthruid")) == False):

            remoteSet = MXServer.getMXServer().getMboSet("LBL_WKTHRU", mbo.getUserInfo())
            remoteSet.setUserWhere("orgid='" + jIOrgid + "' and siteid='" + jISiteid + "' and wkthruid='" + mbo.getString("lbl_wkthruid") +"'")
            if (not remoteSet.isEmpty()):
                newRemoteset=mbo.getMboSet("LBL_WO2WOWKTHRU")
                newRow=newRemoteset.add()
                newRow.setValue("orgid",  jIOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("siteid", jISiteid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("wonum", mbo.getString("wonum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("description", remoteSet.getMbo(0).getString("description"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("DESCRIPTION_LONGDESCRIPTION",remoteSet.getMbo(0).getString("DESCRIPTION_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("WKTHRUID",remoteSet.getMbo(0).getString("WKTHRUID"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("PLANNING_REQD",remoteSet.getMbo(0).getString("PLANNING_REQD"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("PLANNING_REQD_LONGDESCRIPTION",remoteSet.getMbo(0).getString("PLANNING_REQD_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("ACCEPT_CRITERIA",remoteSet.getMbo(0).getString("ACCEPT_CRITERIA"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("ACCEPT_CRITERIA_LONGDESCRIPTION",remoteSet.getMbo(0).getString("ACCEPT_CRITERIA_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("FEEDREV_LESNLRN",remoteSet.getMbo(0).getString("FEEDREV_LESNLRN"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("FEEDREV_LESNLRN_LONGDESCRIPTION",remoteSet.getMbo(0).getString("FEEDREV_LESNLRN_LONGDESCRIPTION"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("SCOPE_OF_WORK",remoteSet.getMbo(0).getString("SCOPE_OF_WORK"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("SCOPE_OF_WORK_LONGDESCRIPTION",remoteSet.getMbo(0).getString("SCOPE_OF_WORK_LONGDESCRIPTION"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("ACCESS_LOCATION",remoteSet.getMbo(0).getString("ACCESS_LOCATION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                newRow.setValue("ACCESS_LOCATION_LONGDESCRIPTION",remoteSet.getMbo(0).getString("ACCESS_LOCATION_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

                #*****************************
                #LBL_WOWKTHRUOPS
                #*****************************
                mbosetremote1 = MXServer.getMXServer().getMboSet("LBL_WKTHRUOPS", mbo.getUserInfo())
                mbosetremote1.setUserWhere("orgid='" + jIOrgid + "' and siteid='" + jISiteid + "' and wkthruid='" + mbo.getString("lbl_wkthruid") +"'")

                if (not mbosetremote1.isEmpty()):
                    WOWkthruOps = mbo.getMboSet("LBL_WO2WOWKTHOPS")
                    intCount=mbosetremote1.count()
                    for i in xrange(intCount):
                            newWOWkthruOps=WOWkthruOps.add()
                            newWOWkthruOps.setValue("orgid", jIOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruOps.setValue("siteid",  jISiteid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruOps.setValue("wonum", mbo.getString("wonum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruOps.setValue("description",mbosetremote1.getMbo(i).getString("description"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruOps.setValue("DESCRIPTION_LONGDESCRIPTION",mbosetremote1.getMbo(i).getString("DESCRIPTION_LONGDESCRIPTION"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruOps.setValue("WKTHRUID",mbosetremote1.getMbo(i).getString("WKTHRUID"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruOps.setValue("OPSEQUENCE",mbosetremote1.getMbo(i).getInt("OPSEQUENCE"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruOps.setValue("OPDURATION",mbosetremote1.getMbo(i).getDouble("OPDURATION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

                            #JIRA EF-4444
                            newWOWkthruOps.setValue("CRAFT",mbosetremote1.getMbo(i).getString("CRAFT"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruOps.setValue("QUANTITY",mbosetremote1.getMbo(i).getInt("quantity"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

                 # Insert record into WPLABOR JIRA EF-4446
                WPLaborSet= mbo.getMboSet("WPLABOR")
                intCount=mbosetremote1.count()
                for i in xrange(intCount):

                    newWPLabor=WPLaborSet.add()
                    newWPLabor.setValue("orgid", jIOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newWPLabor.setValue("siteid",  jISiteid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newWPLabor.setValue("wonum", mbo.getString("wonum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newWPLabor.setValue("craft",       mbosetremote1.getMbo(i).getString("craft"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    #newWPLabor.setValue("lbl_wkthruid",mbosetremote1.getMbo(i).getString("WKTHRUID"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newWPLabor.setValue("lbl_opsequence",mbosetremote1.getMbo(i).getInt("OPSEQUENCE"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newWPLabor.setValue("laborhrs",mbosetremote1.getMbo(i).getDouble("OPDURATION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newWPLabor.setValue("quantity",mbosetremote1.getMbo(i).getInt("quantity"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newWPLabor.setValue("LBL_OPDESCRIPTION", mbosetremote1.getMbo(i).getString("description"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    if (isBlank(mbosetremote1.getMbo(i).getString("DESCRIPTION_LONGDESCRIPTION")) == False):
                        newWPLabor.setValue("LBL_OPDESCRIPTION_LONGDESCRIPTION", mbosetremote1.getMbo(i).getString("DESCRIPTION_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)



                #*****************************
                #LBL_WOWKTHRUHAZ
                #*****************************

                mbosetremote1 = MXServer.getMXServer().getMboSet("LBL_WKTHRUHAZ", mbo.getUserInfo());
                mbosetremote1.setUserWhere("orgid='" + jIOrgid + "' and siteid='" + jISiteid + "' and wkthruid='" + mbo.getString("lbl_wkthruid") +"'")

                if (not mbosetremote1.isEmpty()):
                        WOWkthruhaz= mbo.getMboSet("LBL_WO2WOWKTHHAZ")
                        intCount=mbosetremote1.count()
                        for i in xrange(intCount):
                            lblWkthruHaz= WOWkthruhaz.add()
                            lblWkthruHaz.setValue("orgid", jIOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            lblWkthruHaz.setValue("siteid", jISiteid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            lblWkthruHaz.setValue("wkthruid", mbosetremote1.getMbo(i).getString("WKTHRUID"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            lblWkthruHaz.setValue("hazardid", mbosetremote1.getMbo(i).getString("hazardid"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            lblWkthruHaz.setValue("wonum", mbo.getString("wonum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)


                #*******************
                #LBL_WOWKTHRUMAT
                #******************
                mbosetremote1 = MXServer.getMXServer().getMboSet("LBL_WKTHRUMAT", mbo.getUserInfo())
                mbosetremote1.setUserWhere("orgid='" + jIOrgid + "' and siteid='" + jISiteid + "' and wkthruid='" + mbo.getString("lbl_wkthruid") +"'")

                if (not mbosetremote1.isEmpty()):
                    WOWkthruMat = mbo.getMboSet("LBL_WO2WOWKTHMAT")
                    intCount=mbosetremote1.count()
                    for i in xrange(intCount):
                            newWOWkthruMat=WOWkthruMat.add()
                            newWOWkthruMat.setValue("orgid", jIOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruMat.setValue("siteid",  jISiteid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruMat.setValue("wonum", mbo.getString("wonum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruMat.setValue("itemnum",mbosetremote1.getMbo(i).getString("itemnum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruMat.setValue("WKTHRUID",mbosetremote1.getMbo(i).getString("WKTHRUID"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruMat.setValue("quantity",mbosetremote1.getMbo(i).getDouble("quantity"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruMat.setValue("ITEMDESCRIPTION",mbosetremote1.getMbo(i).getString("ITEMDESCRIPTION"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruMat.setValue("ITEMDESCRIPTION_LONGDESCRIPTION",mbosetremote1.getMbo(i).getString("ITEMDESCRIPTION_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruMat.setValue("LOCATION_INFO",mbosetremote1.getMbo(i).getString("LOCATION_INFO"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

                    # Insert record into wpmaterial JIRA EF-4446
                    WPMaterialSet= mbo.getMboSet("WPMATERIAL")
                    intCount=mbosetremote1.count()
                    itemRemote1= MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo())

                    for i in xrange(intCount):

                        newWpMaterial=WPMaterialSet.add()
                        newWpMaterial.setValue("orgid", jIOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                        newWpMaterial.setValue("siteid",  jISiteid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                        newWpMaterial.setValue("wonum", mbo.getString("wonum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                        newWpMaterial.setValue("itemnum",mbosetremote1.getMbo(i).getString("itemnum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                        newWpMaterial.setValue("itemqty",mbosetremote1.getMbo(i).getDouble("quantity"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

                        #Get item description
                        itemRemote1.reset()
                        itemRemote1.setUserWhere("itemnum='" + mbosetremote1.getMbo(i).getString("itemnum") +"'")

                        if (not itemRemote1.isEmpty()):
                            newWpMaterial.setValue("DESCRIPTION",itemRemote1.getMbo(0).getString("DESCRIPTION"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)

                        newWpMaterial.setValue("LOCATION","ITEMMASTER" ,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    itemRemote1=None
                #*******************
                #LBL_WOWKTHRURES
                #******************
                mbosetremote1 = MXServer.getMXServer().getMboSet("LBL_WKTHRURES", mbo.getUserInfo())
                mbosetremote1.setUserWhere("orgid='" + jIOrgid + "' and siteid='" + jISiteid + "' and wkthruid='" + mbo.getString("lbl_wkthruid") +"'")

                if (not mbosetremote1.isEmpty()):
                    WOWkthruRes = mbo.getMboSet("LBL_WO2WOWKTHRESALL")
                    intCount=mbosetremote1.count()
                    for i in xrange(intCount):
                            newWOWkthruRes=WOWkthruRes.add()

                            newWOWkthruRes.setValue("orgid", jIOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("siteid",  jISiteid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("wonum", mbo.getString("wonum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("resource_type",mbosetremote1.getMbo(i).getString("resource_type"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("WKTHRUID",mbosetremote1.getMbo(i).getString("WKTHRUID"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("SEQUENCE",mbosetremote1.getMbo(i).getInt("SEQUENCE"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("EHS_SUPPORT",mbosetremote1.getMbo(i).getString("EHS_SUPPORT"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("EHS_SUPPORT_COMMENTS",mbosetremote1.getMbo(i).getString("EHS_SUPPORT_COMMENTS"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERMITS",mbosetremote1.getMbo(i).getString("PERMITS"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERMITS_COMMENTS",mbosetremote1.getMbo(i).getString("PERMITS_COMMENTS"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERMIT_NUMBER",mbosetremote1.getMbo(i).getString("PERMIT_NUMBER"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERMIT_RESPONSIBLE_INDIVIDUAL",mbosetremote1.getMbo(i).getString("PERMIT_RESPONSIBLE_INDIVIDUAL"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERMITS_COMMENTS_LONGDESCRIPTION",mbosetremote1.getMbo(i).getString("PERMITS_COMMENTS_LONGDESCRIPTION"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("DRAWINGS",mbosetremote1.getMbo(i).getString("DRAWINGS"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("DRAWINGS_COMMENTS",mbosetremote1.getMbo(i).getString("DRAWINGS_COMMENTS"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("CRAFT",mbosetremote1.getMbo(i).getString("CRAFT"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("CRAFT_COMMENTS",mbosetremote1.getMbo(i).getString("CRAFT_COMMENTS"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("CRAFT_COMMENTS_LONGDESCRIPTION",mbosetremote1.getMbo(i).getString("CRAFT_COMMENTS_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("CRAFT_DURATION",mbosetremote1.getMbo(i).getDouble("CRAFT_DURATION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("EHS_SUPPORT_COMMENTS_LONGDESCRIPTION",mbosetremote1.getMbo(i).getString("EHS_SUPPORT_COMMENTS_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("EHS_SUPPORT_CONT",mbosetremote1.getMbo(i).getString("EHS_SUPPORT_CONT"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERSONID",mbosetremote1.getMbo(i).getString("PERSONID"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERSON_PHONE",mbosetremote1.getMbo(i).getString("PERSON_PHONE"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERSON_FUNCTION",mbosetremote1.getMbo(i).getString("PERSON_FUNCTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PERSON_FUNCTION_LONGDESCRIPTION",mbosetremote1.getMbo(i).getString("PERSON_FUNCTION_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PLAN_TEAM_DESC",mbosetremote1.getMbo(i).getString("PLAN_TEAM_DESC"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PLAN_TEAM_DESC_LONGDESCRIPTION",mbosetremote1.getMbo(i).getString("PLAN_TEAM_DESC_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("PLAN_TEAM_DURATION",mbosetremote1.getMbo(i).getDouble("PLAN_TEAM_DURATION"),   MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruRes.setValue("RES_DURATION",mbosetremote1.getMbo(i).getDouble("RES_DURATION"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)


                #*******************
                #LBL_WOWKTHRUFEEDBK
                #******************
                mbosetremote1 = MXServer.getMXServer().getMboSet("LBL_WKTHRUFEEDBK", mbo.getUserInfo())
                mbosetremote1.setUserWhere("orgid='" + jIOrgid + "' and siteid='" + jISiteid + "' and wkthruid='" + mbo.getString("lbl_wkthruid") +"'")

                if (not mbosetremote1.isEmpty()):
                    WOWkthruFeedbk = mbo.getMboSet("LBL_WO2WOWKFEEDBACK")
                    intCount=mbosetremote1.count()
                    for i in xrange(intCount):
                            newWOWkthruFeedbk=WOWkthruFeedbk.add()
                            newWOWkthruFeedbk.setValue("orgid", jIOrgid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruFeedbk.setValue("siteid",  jISiteid, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruFeedbk.setValue("wonum", mbo.getString("wonum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruFeedbk.setValue("FEEDBK_DTL",mbosetremote1.getMbo(i).getString("FEEDBK_DTL"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruFeedbk.setValue("FEEDBK_DTL_LONGDESCRIPTION",mbosetremote1.getMbo(i).getString("FEEDBK_DTL_LONGDESCRIPTION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruFeedbk.setValue("FEEDBK_RESP",mbosetremote1.getMbo(i).getString("FEEDBK_RESP"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruFeedbk.setValue("PERSONID",mbosetremote1.getMbo(i).getString("PERSONID"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruFeedbk.setValue("INITIATE_WO",mbosetremote1.getMbo(i).getBoolean("INITIATE_WO"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                            newWOWkthruFeedbk.setValue("WKTHRUID",mbosetremote1.getMbo(i).getString("WKTHRUID"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)