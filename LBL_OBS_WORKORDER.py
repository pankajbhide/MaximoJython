###############################################################
# Purpose: Script for object level launch for workorder
#          (after save)
# 
# Author : Pankaj Bhide
#
# Date    : August 14, 2015
#
# Revision
# History : JIRA EF-4256 Pankaj July 28, 2016
#
#           JIRA EF-4276 Email to FAM after the FAM 
#                        is associated to the work order
#
#           JIRA EF-7090 PM workflow project
#
#           JIRA EF-11458 Do not send notification when
#                         FAM is changed for PM work orders
#           
#            
######################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap
from java.util import Date
from java.util import Calendar
from java.text import SimpleDateFormat
from psdi.mbo import SqlFormat
from psdi.util.logging import MXLoggerFactory


def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams","")
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def getPersonname(strPersonid):
    strPersonname=None
    personSet = MXServer.getMXServer().getMboSet("PERSON", mbo.getUserInfo())
    personSet.setUserWhere("personid='" + strPersonid +"'")
    if (not personSet.isEmpty()):
                strPersonname=personSet.getMbo(0).getString("displayname")
    personSet=None      
    return strPersonname

def getWorktypedesc(strWorktype):
    strWorktypedesc=None
    if (isBlank(strWorktype) == False):
        
        worktypeSet = MXServer.getMXServer().getMboSet("WORKTYPE", mbo.getUserInfo())
        worktypeSet.setUserWhere("worktype='" + strWorktype +"' and woclass='WORKORDER' ")
        if (not worktypeSet.isEmpty()):
                    strWorktypedesc=worktypeSet.getMbo(0).getString("wtypedesc")
        worktypeSet=None      
    return strWorktypedesc

def getWostatusdesc(strWostatus):
    strWostatusdesc=None
    synonymSet = MXServer.getMXServer().getMboSet("SYNONYMDOMAIN", mbo.getUserInfo())
    synonymSet.setUserWhere("value='" + strWostatus +"' and domainid='WOSTATUS' ")
    if (not synonymSet.isEmpty()):
                strWostatusdesc=synonymSet.getMbo(0).getString("description")
    synonymSet=None      
    return strWostatusdesc

def getLblmaxvarvalue(strVarname):
    strLblvarvalue=None
    lblmaxvarSet = MXServer.getMXServer().getMboSet("LBL_MAXVARS", mbo.getUserInfo())
    lblmaxvarSet.setUserWhere("varname='" + strVarname +"' and orgid='LBNL' and siteid='FAC' ")
    if (not lblmaxvarSet.isEmpty()):
                strLblvarvalue=lblmaxvarSet.getMbo(0).getString("varvalue")
    lblmaxvarSet=None      
    return strLblvarvalue

def getPropertyvalue(strProperty):
    strPropertyValue=None
    maxpropvalueSet = MXServer.getMXServer().getMboSet("maxpropvalue", mbo.getUserInfo())
    maxpropvalueSet.setUserWhere("propname='" + strProperty +"'")
    if (not maxpropvalueSet.isEmpty()):
                strPropertyValue=maxpropvalueSet.getMbo(0).getString("propvalue")
    maxpropvalueSet=None      
    return strPropertyValue

def getEmailaddress(strPersonid):
    strEmail=None
    emailSet = MXServer.getMXServer().getMboSet("email", mbo.getUserInfo())
    emailSet.setUserWhere("personid='" + strPersonid +"' and isprimary=1 ")
    if (not emailSet.isEmpty()):
            strEmail=emailSet.getMbo(0).getString("emailaddress")
    emailSet=None      
    return strEmail

#######################################################
# Function to find out day of the week for a given date
#######################################################
def getDayOfWeek(d):
    
    cal=Calendar.getInstance()
    cal.setTime(d)
    dayOfWeek = cal.get(Calendar.DAY_OF_WEEK);
    return dayOfWeek
################################################
# Function to get the modified target start date
# JIRA EF-7090
################################################
def get_target_start_date(d):
    
    dayOfWeek = getDayOfWeek(d)
    cal=Calendar.getInstance()
    cal.setTime(d)
    
    if (dayOfWeek==1):  # 1=Sunday
        cal.add(Calendar.DATE,+1)
        d=cal.getTime()
        
    if (dayOfWeek==7):  # 7=Saturday
        cal.add(Calendar.DATE,+2)
        d=cal.getTime()
        
    #if (dayOfWeek !=1 and dayOfWeek !=7):
    #    while (getDayOfWeek(d) != 2): # 2=Monday 
    #        cal.setTime(d)
    #        cal.add(Calendar.DATE,-1)
    #        d=cal.getTime() 
            
    return d

################################################
# Function to get the modified target finish date
# JIRA EF-7090
################################################
def get_target_comp_date(d, offset):
    print str(d)
    cal=Calendar.getInstance()
    cal.setTime(d)
    cal.add(Calendar.DATE,offset) 
    d=cal.getTime()
    
    return d


##############
myLogger = MXLoggerFactory.getLogger("maximo.script.customscript")
logger = mbo.getMboLogger()
ctx = HashMap()
ctx.put("mbo",mbo)
boolError=False  

    

if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    
    
    if (onadd == True):
        
        myLogger.debug("PRB in add") 
        # Get FAM Information    
        strOwnergroup=""
        strOwner=""
        strFAMCombined=""
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
                                
        mbo.setValue("lbl_famid", strOwnergroup,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        mbo.setValue("lbl_fammanager", strOwner,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    
         
         
       
        # Derive the value of lbl_woenteredby 
        if (isBlank(mbo.getString("lbl_woenteredby"))== True):
            strWhere="upper(loginid)=" + "'" + user.upper() +"'"      
            maxuserSet = MXServer.getMXServer().getMboSet("MAXUSER", mbo.getUserInfo())
            maxuserSet.setUserWhere(strWhere)
            if (not maxuserSet.isEmpty()):
                maxuserSet= maxuserSet.getMbo(0)
                mbo.setValue("lbl_woenteredby", maxuserSet.getString("personid"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            maxuserSet=None
            
        # Add row in work order extension table
        workorderExtSet = mbo.getMboSet("LBL_WO2WOEXT")
        workorderExtSet.add()
        workorderExtSet.setValue("WONUM",mbo.getString("wonum"))
        workorderExtSet.setValue("SITEID",jISiteid)
        workorderExtSet.setValue("ORGID",jIOrgid)
       
        # For confined space project, derive the value of supervisor
        # from its parent work order if not specified
        if (isBlank(mbo.getString("supervisor"))==True and isBlank(mbo.getString("parent"))==False):
            parentWoSet=mbo.getMboSet("parent")
            if (not parentWoSet.isEmpty()):
                mbo.setValue("supervisor", parentWoSet.getMbo(0).getString("supervisor"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            parentWoSet= None
            #logger.info("PRB: getDuplicated: " + str(mbo.getDuplicated()))
            #logger.info("PRB: duplicated: " + str(mbo.duplicated))
            # If the work order is duplicated, then set null values to a few columns
        if (mbo.getDuplicated() == True and mbo.isNew() == True):
                            
            mbo.setValueNull("onbehalfof",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)           
            mbo.setValueNull("COMMODITYGROUP",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            #JIRA EF-6141 set external ref id to null in case of work order duplicate
            mbo.setValueNull("externalrefid",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            mbo.setValueNull("lbl_dtsenttofms",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        
                    
            # In case work order is duplicated, then derive the release status from
            # its location     
            if (isBlank(mbo.getString("location"))==False):
                 
                # Tab
                                            
                # Get Release status
                service.invokeScript("LBL_LIB_GETRELEASESTATUS",ctx)  
                # The variable "strReleaseStatus" is returned from the library script
                strReleaseStatus=str(ctx.get("strReleaseStatus"))
                mbo.setValue("lbl_release_status", strReleaseStatus, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
               
        #########################################################################################       
        # JIRA EF-7090
        # Modify target start/finish date as per the requirements indicated in JIRA EF-7090
        ##########################################################################################
        
        if ((mbo.getString("worktype").startswith("PM") == True) and (isBlank(mbo.getString("pmnum")) == False)):
           
            
            intLbl_targ_strt_fin_days=0
            strWhere="siteid='" + mbo.getString("siteid") + "' and pmnum='" + mbo.getString("pmnum") + "'"  
            pmSet = MXServer.getMXServer().getMboSet("PM", mbo.getUserInfo())
            pmSet.setUserWhere(strWhere)
            if (not pmSet.isEmpty()):
                
                #############################################################
                # JIRA EF-8908 - Bring code compliance from PM to work order 
                #############################################################
                mbo.setValue("lbl_codecompliance", pmSet.getMbo(0).getBoolean("lbl_codecompliance"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                mbo.setValue("LBL_ISPMCRITICAL", pmSet.getMbo(0).getBoolean("LBL_ISPMCRITICAL"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
                #JIRA EF-11179
                mbo.setValue("APPTREQUIRED", pmSet.getMbo(0).getBoolean("LBL_APPTREQUIRED"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

                intLbl_targ_strt_fin_days= pmSet.getMbo(0).getInt("lbl_targ_strt_fin_days")
                strPMPlannergroup=pmSet.getMbo(0).getString("LBL_PLANNER_GROUP")
                if (isBlank(strPMPlannergroup)):
                    strPMPlannergroup='FAPMD'  # Default value 
            pmSet=None
            
                      
            if (mbo.getMboValueData("TARGSTARTDATE").isNull() == False):
                                
                newtargstartdate=get_target_start_date(mbo.getDate("targstartdate"))
                newtargcompdate=get_target_comp_date(newtargstartdate,intLbl_targ_strt_fin_days)
                
                mbo.setValue("targstartdate",newtargstartdate,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                mbo.setValue("targcompdate", newtargcompdate,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                mbo.setValue("SCHEDSTART",newtargstartdate,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                mbo.setValue("SCHEDFINISH", newtargcompdate,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                mbo.setValue("lbl_planner_group", strPMPlannergroup,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                
                
                                 
               
    ############## Common actions before save #############################
               
    if (ondelete == False):
        
        
        
         
       
        ###########################################################################  
        # JIRA EF-4276 Email to FAM after the FAM is associated to the work order
        ###########################################################################
        if (isBlank(mbo.getString("lbl_fammanager")) == False):
            
            strOldFam=mbo.getMboValue("lbl_fammanager").getPreviousValue().asString()
            if (isBlank(strOldFam) == True):
                
                strOldFam="_"
           
            
                
            if (strOldFam !=mbo.getString("lbl_fammanager")):
                                
                strOwnergroup=""
                strOwner=""
                strFAMCombined=""
                #strPlanner_group=""
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
                   #if (i==2):
                   #     strPlanner_group=val
                                                                                  
                mbo.setValue("lbl_famid", strOwnergroup,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                #mbo.setValue("lbl_planner_group", strPlanner_group,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
                
                # Do not send email notification for PM work orders JIRA EF-11458
                if ((mbo.getString("worktype").startswith("PM") == False) and (isBlank(mbo.getString("pmnum")) == True)):
                    
                    strEnvironment=getLblmaxvarvalue("APPLICATION_ENV")
                    strFAMName=getPersonname(mbo.getString("lbl_fammanager"))
                    strReportedbyname=getPersonname(mbo.getString("reportedby"))
                    strMailhost=getPropertyvalue("mail.smtp.host")
                    strFooter=""  
                    strSubjectline="" 
                    strWPCEmail=getLblmaxvarvalue("FACWPC_EMAIL")  
                        
                    if (strEnvironment !="PRODUCTION"):
                            
                        strSubjectline="[TEST] "   
                        strFooter ="<TR><TD>&nbsp;</TD></TR><TR><TD><B>[This email is generated from the TEST data and it does not represent the actual data.]</TD></TR>" 
                                                   
                            
                    strSubjectline +="Facilities Area Manager " + strFAMName + " assigned to the Work Order " + mbo.getString("wonum")
                    strBody  ="<HTML><HEAD><TITLE> " + "Facilities Area Manager " + strFAMName + " assigned to the Work Order " + mbo.getString("wonum") +" </TITLE></HEAD>"
                    strBody +="<BODY>"
                    strBody +="<TABLE>"
                    strBody +="<TR><TD>"
                    #strBody +="<TR><TD>Dear " + strFAMName + "</TD><TR>"
                    strBody +="<TR><TD>&nbsp;</TD></TR>"
                    strBody += "The following work order was entered by " + strReportedbyname + " and is awaiting your approval for planning."
                    strBody +="<TR><TD>&nbsp;</TD></TR>"  
                    #strBody +=" Given below are the details of the work order: "
                    strBody +="<TR><TD>"
                    strBody +="<TABLE BORDER=1 ALIGN=LEFT>"
                    strBody +="<TR><TD><B>Work Order Number</B></TD><TD><B>"  + mbo.getString("wonum") +"</B></TD></TR>"
                    strBody +="<TR><TD><B>Requested work</B></TD><TD><B>" + mbo.getString("description")  +"</B></TD></TR>"
                    #strBody +="<TR><TD><B>Long Description</B></TD><TD><B>" + mbo.getString("description_longdescription")  +"</B></TD></TR>"
                    #strBody +="<TR><TD><B>Work type</B></TD><TD><B>"          + mbo.getString("worktype")  + " - " + getWorktypedesc(mbo.getString("worktype")) +"</B></TD></TR>"
                    strBody +="<TR><TD><B>Reported By</B></TD><TD><B>" +mbo.getString("reportedby")  + " - " + strReportedbyname +"</B></TD></TR>"
                    strBody +="<TR><TD><B>Date Reported</B></TD><TD><B>" + SimpleDateFormat("MM/dd/yyyy").format(mbo.getDate("reportdate"))+"</B></TD></TR>"
                                
                    strBody +="<TR><TD><B>Location</B></TD><TD><B>"  + mbo.getString("location")  +"</B></TD></TR>"
                    #strBody +="<TR><TD><B>Current Status</B></TD><TD><B>"  + jIStatus + " - " + getWostatusdesc(jIStatus)
                       
                    #strBody +="<TR><TD><B>Status Date</B></TD><TD><B>" + SimpleDateFormat("MM/dd/yyyy").format(mbo.getDate("changedate"))+"</B></TD></TR>"
                    #strBody +="<TR><TD><B>Target Start Date</B></TD><TD><B>" +strTargStartDate+"</B></TD></TR>"
                    #strBody +="<TR><TD><B>Target Completion Date</B></TD><TD><B>" +strTargCompDate +"</B></TD></TR>"
                       
                    strBody +="</TABLE>"
                    strBody +="</TD></TR>"
                    
                    strBody +="<TR><TD>&nbsp;</TD></TR>"
                    strBody +="<TR><TD>"
                       
                    strBody +="</TD></TR>"
                    strBody +="<TR><TD>&nbsp;</TD></TR>"
                    strBody += strFooter 
                    strBody +="</TD></TR>"
                    strBody += "</TABLE></BODY></HTML>"
                       
                    strToEmail=""
                       
                    # Email to supervisor and WPC 
                    if (strEnvironment =="PRODUCTION"):
                        strToEmail=getEmailaddress(mbo.getString("lbl_fammanager"))
                    else:
                        strWhere  = " persongroup='FASUPERTEST'" 
                        mbosetremote = MXServer.getMXServer().getMboSet("persongroupteam", mbo.getUserInfo())
                        mbosetremote.setUserWhere(strWhere)
                            
                        if (not mbosetremote.isEmpty()):
                            
                            thismbo=mbosetremote.moveFirst()
                            while thismbo:
                                                                                               
                                if (isBlank(strToEmail) == True):
                                    strToEmail=getEmailaddress(thismbo.getString("resppartygroup")) 
                                else:
                                    strToEmail = strToEmail +"," + getEmailaddress(thismbo.getString("resppartygroup"))   
                                thismbo=mbosetremote.moveNext()
                                
                            mbosetremote=None                        
                                                                           
                    #if (isBlank(strToEmail) == False and strEnvironment =="PRODUCTION"):
                    if (isBlank(strToEmail) == False):
                        mbo.LblSendMail(strMailhost,strWPCEmail , strToEmail, "", strSubjectline,  "HTML", strBody)
                             
                    
        # Actions to be performed until the status of the work order is equal to WAPPR
        if (jIStatus_internal=="WAPPR"):
            
           
            # Get Release status
            service.invokeScript("LBL_LIB_GETRELEASESTATUS",ctx)  
            # The variable "strReleaseStatus" is returned from the library script
            strReleaseStatus=str(ctx.get("strReleaseStatus"))
            
            mbo.setValue("lbl_release_status", strReleaseStatus, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
                               
            # Check whether glaccount is valid or not 
            # This is required because work order can be created
            # from any other external app (e.g. dataSplice etc.) 
            # This is also useful to the work order generated via PM 
            if (isBlank(mbo.getString("glaccount")) == False):
                
                strWhere=" orgid='LBNL' and active=1 and glaccount='" + mbo.getString("glaccount")  + "'"
                projactSet= MXServer.getMXServer().getMboSet("lbl_v_projact", mbo.getUserInfo())
                projactSet.setUserWhere(strWhere)
                if (projactSet.isEmpty()):
                    setError("lbl_invalidglaccount","workorder"," ")
                    boolError=True
                    projactSet=None

            if (boolError==False):
                # Derive the value of lead and lead craft from job plan if they have not indicated
                # on the work order    
           
                if (isBlank(jIStatus)== False and isBlank(mbo.getString("jpnum")) == False):
                          
                    jobplanSet = mbo.getMboSet("JOBPLAN")
                    if (not jobplanSet.isEmpty()):
                        if (isBlank(mbo.getString("lead")) == True):
                            mbo.setValue("lead",jobplanSet.getMbo(0).getString("laborcode"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            
                        if (isBlank(mbo.getString("leadcraft")) == True):
                            mbo.setValue("leadcraft",jobplanSet.getMbo(0).getString("lbl_leadcraft"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            
                    jobplanSet=None       
                                    
            if (boolError==False and  jIStatus_modified == False) or (mbo.isNew() == True):
                # if they are not set on the children work orders until status of parent work order=WAPPR
                ChildrenSet = mbo.getMboSet("CHILDREN")
               
                if (not ChildrenSet.isEmpty()):
                    
                    intCount=ChildrenSet.count()                           
                    for i in xrange(intCount):
                        
                        thisRow = ChildrenSet.getMbo(i)
                        if (thisRow.getString("status") !="CLOSE" and thisRow.getString("status") !="CAN"):                          
                        
                        
                            if (isBlank(thisRow.getString("leadcraft")) == True):
                                thisRow.setValue("leadcraft",mbo.getString("leadcraft"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                           
                            
                             
               
                #######################################################################              
                                       
                                                                 
 
        # Trigger the actions on work order status change                    
        if (jIStatus_modified == True):
            
         
           # Auto populate scheduled start and scheduled end if work order
           # is released without any condition (WPC-2) JIRA EF-7092
           
           # This is not required anymore as per Max W and Tammy T Mar 29,1018
           
           #if (isBlank(mbo.getString("lbl_condition_rel")) == False and mbo.getString("Lbl_condition_rel")=="N"):
           #    if (mbo.getDate("schedstart") is None):
           #        mbo.setValue("schedstart", mbo.getDate("targstartdate"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                   
           #    if (mbo.getDate("schedfinish") is None):
           #        mbo.setValue("schedfinish", mbo.getDate("targcompdate"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            # Get Release status
           service.invokeScript("LBL_LIB_GETRELEASESTATUS",ctx)  
            # The variable "strReleaseStatus" is returned from the library script
           strReleaseStatus=str(ctx.get("strReleaseStatus"))
           mbo.setValue("lbl_release_status", strReleaseStatus, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
           
           # JIRA EF-7829 
           if (jIStatus=="SPRI"):
               mbo.setValueNull("schedstart", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
               mbo.setValueNull("schedfinish", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
           # Datasplice implementation   (set start and stop assignment datetimes to null)  
           if (jIStatus=="WFAM" or jIStatus=='WASSIGN'):
                 
               # if they are not set on the children work orders until status of parent work order=WAPPR
               AssignmentsSet = mbo.getMboSet("ASSIGNMENT")
               
               if (not AssignmentsSet.isEmpty()):
                    
                    intCount=AssignmentsSet.count()                           
                    for i in xrange(intCount):
                        
                        thisRow = AssignmentsSet.getMbo(i)
                
                       
                        if (thisRow.getString("lbl_status") != "WORK-COMP"):
                            
                            thisRow.setValueNull("lbl_startdttm",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            thisRow.setValueNull("lbl_stopdttm",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            thisRow.setValueNull("lbl_status", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            thisRow.setValueNull("laborcode", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                
        #####################################################################                     
       #Trigger for safety components
       # Copy hazards/precaution only if safety plan id is not indicated
       #######################################################################
        boolCopySafety=False 
        wosafetylinkSet= mbo.getMboSet("WOSAFETYLINK")
       
        #myLogger.info("PRB about to start copyng hazads step1")    
        if (isBlank(mbo.getString("safetyplanid")) == True):
           
            strPrevAsset=mbo.getMboValue("assetnum").getPreviousValue().asString()  # .trim()
            strPrevLocation=mbo.getMboValue("location").getPreviousValue().asString() # .trim()
               
               
            if (isBlank(strPrevAsset) == True):
                strPrevAsset="_"
                                      
            if (isBlank(strPrevLocation) == True):
                strPrevLocation="_"
                   
            # Hazards should be copied to the work orders genersted via WRC
            #until they are WAPPR 
            if (wosafetylinkSet.count()==0):
                if (mbo.isNull("wo4")==False and jIStatus_internal=='WAPPR'):
                    boolCopySafety=True

                    
            if   (boolCopySafety== False):
                                    
                if (strPrevLocation != mbo.getString("location")):
                    boolCopySafety=True                   
                if (strPrevAsset != mbo.getString("assetnum")):
                    boolCopySafety=True
                        
                if (mbo.getDuplicated() == True and mbo.isNew() == True):
                    boolCopySafety=False
                   
                                                     
            if (boolCopySafety == True):
                mbo.custom_trigger_safety_components()