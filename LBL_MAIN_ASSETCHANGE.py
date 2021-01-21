##########################################################################
# Purpose: Script for changing asset data 

# Author : Pankaj Bhide
#
# Date    : May 15 2017
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

def getLocDesc(strLocation,runAsUserInfo1):
    strLocDesc=None
   
    locationsSet = MXServer.getMXServer().getMboSet("LOCATIONS", runAsUserInfo1)
    locationsSet.setUserWhere("siteid='FAC' and location='" + strLocation+"' and disabled=0")
    if (not locationsSet.isEmpty()):
                strLocDesc=locationsSet.getMbo(0).getString("description")
                if (isBlank(strLocDesc) == True):
                    strLocDesc="TBD"
    locationsSet=None      
   
    return strLocDesc

def getCompanyDesc(strMfr,runAsUserInfo1):
    strMfrDesc=None
    companiesSet = MXServer.getMXServer().getMboSet("COMPANIES", runAsUserInfo1)
    companiesSet.setUserWhere("company='" + strMfr+"'" )
    if (not companiesSet.isEmpty()):
                strMfrDesc=companiesSet.getMbo(0).getString("name")
    companiesSet=None      
    return strMfrDesc

def getDomainDesc(strDomain, strValue,runAsUserInfo1):
    strDomainDesc=None
    DomainsSet = MXServer.getMXServer().getMboSet("ALNDOMAIN", runAsUserInfo1)
    DomainsSet.setUserWhere("domainid='" + strDomain+"' and value='" + strValue +"'" )
    if (not DomainsSet.isEmpty()):
                strDomainDesc=DomainsSet.getMbo(0).getString("description")
    DomainsSet=None      
    return strDomainDesc


###########################################
# Function to insert record into log table
###########################################
def insert_asset_log(lbl_assetupd_logRemote, runAsUserInfo1,strOldAssetnum, strAssetnum, strLogType, strLog_description):
  
    lbl_assetupd_log=lbl_assetupd_logRemote.add()
    lbl_assetupd_log.setValue("assetnum",     strAssetnum, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    lbl_assetupd_log.setValue("log_type",     strLogType, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    lbl_assetupd_log.setValue("old_assetnum", strOldAssetnum, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    lbl_assetupd_log.setValue("log_description", strLog_description, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    lbl_assetupd_log.setValue("changedate", MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    lbl_assetupd_logRemote.save()
    
#########################################################
       
# Open MXServer session
mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")


# Create SetRemotes
assetSetRemote           = MXServer.getMXServer().getMboSet("ASSET", runAsUserInfo1)
assetSetRemote2          = MXServer.getMXServer().getMboSet("ASSET", runAsUserInfo1)
assetupd_detailsSetRemote= MXServer.getMXServer().getMboSet("LBL_ASSETUPD_DETAILS", runAsUserInfo1)
lbl_assetupd_logRemote   = MXServer.getMXServer().getMboSet("lbl_assetupd_log", runAsUserInfo1)

route_stopRemote         = MXServer.getMXServer().getMboSet("route_stop", runAsUserInfo1)
jpassetsplinkRemote      = MXServer.getMXServer().getMboSet("jpassetsplink", runAsUserInfo1)
pmRemote                 = MXServer.getMXServer().getMboSet("pm", runAsUserInfo1)
doclinksSetRemote        = MXServer.getMXServer().getMboSet("doclinks", runAsUserInfo1)
doclinksSetRemote2       = MXServer.getMXServer().getMboSet("doclinks", runAsUserInfo1)

 
assetupd_detailsSetRemote.setUserWhere(" 1=1 order by lbl_assetupd_detailsid") # existing record
assetupd_detailsSetRemote.reset()

# Read all the rows from assetupd_detailsSet collection 
if (not assetupd_detailsSetRemote.isEmpty()):
   
    intCount=assetupd_detailsSetRemote.count()
    # Loop through each row from the collection
    for i in xrange(intCount):
        
        boolError=False
        boolAssetToBeAdded=False
        strExistingAssetnum=assetupd_detailsSetRemote.getMbo(i).getString("existing_assetnum").strip()
        strNewAssetnum     =assetupd_detailsSetRemote.getMbo(i).getString("assetnum").strip()
        strDesiredStatus   =assetupd_detailsSetRemote.getMbo(i).getString("asset_status").strip()
        strAssetnum=""
        
        # The data has to come from a file           
        strTemp=assetupd_detailsSetRemote.getMbo(i).getString("inputfilename")
        if (isBlank(strTemp) == True):
            boolError=True
            insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strExistingAssetnum,strExistingAssetnum, "ERROR","Input file name is blank")
        
        
        #########################################
        #   Existing asset and not a new asset  #
        #########################################
        if (isBlank(strNewAssetnum)==True and isBlank(strExistingAssetnum)==False):

            strAssetnum=strExistingAssetnum
            print "Processing for an existing asset " + strAssetnum              
            # Find out whether the asset exists, if not log as error and continue reading next record 
            assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + strAssetnum + "'")
            assetSetRemote.reset() 
            
            if (assetSetRemote.isEmpty()):
               
                insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strAssetnum,strAssetnum,"ERROR","Existing asset does not exist.")
                assetupd_detailsSetRemote.getMbo(i).setValue("status","ERROR: Existing asset does not exist",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetupd_detailsSetRemote.getMbo(i).setValue("statusdate",MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                continue
                                
            assetSet=assetSetRemote.getMbo(0)
            
            strLocation=assetSet.getString("location")
            strDescription=assetSet.getString("description")
            strLblAssetclassification =assetSet.getString("lbl_asset_classification")
            strAssetMfr=assetSet.getString("manufacturer")
            strAssetSerialnum=assetSet.getString("serialnum")
            strAssetModel=assetSet.getString("lbl_model")
                  
        ##################################################    
        # New asset is not replaced by an existing asset #
        ##################################################  
        if (isBlank(strNewAssetnum)==False and isBlank(strExistingAssetnum)==True):
   
            strAssetnum=strNewAssetnum
            print "Processing for new asset " + strAssetnum
            # Find out whether the asset exists, if exists log as error and continue reading next record
            
            assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + strAssetnum + "'")
            assetSetRemote.reset() 
            
            if (not assetSetRemote.isEmpty()):
               
                insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strAssetnum,strAssetnum,"WARNING","New asset already exists.")
                assetupd_detailsSetRemote.getMbo(i).setValue("status","WARNING: New asset already exists",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetupd_detailsSetRemote.getMbo(i).setValue("statusdate",MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetSet=assetSetRemote.getMbo(0)
            else:
                assetSet=assetSetRemote.add()
                assetSet.setValue("assetnum", strAssetnum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)                
                                    
                boolAssetToBeAdded=True    
                
            #Initialize the values 
            strLocation="zzBlankzz"
            strDescription="zzBlankzz"
            strLblAssetclassification ="zzBlankzz"
            strAssetMfr="zzBlankzz"
            strAssetSerialnum="zzBlankzz"
            strAssetModel="zzBlankzz"      
    
        #########################################    
        # New asset is replaced by an old asset #
        #########################################
        if (isBlank(strNewAssetnum)==False and isBlank(strExistingAssetnum)==False):
            
            print "Processing new asset " + strNewAssetnum + " replacing with " + strExistingAssetnum
            
            # Ensure new asset does not exist
            assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + strNewAssetnum + "'")
            assetSetRemote.reset() 
            
            if (not assetSetRemote.isEmpty()):
               
                insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strNewAssetnum,strNewAssetnum,"WARNING","New asset " + strNewAssetnum + "  to be replaced by an existing asset already exists.")
                assetupd_detailsSetRemote.getMbo(i).setValue("status","WARNING: New asset " + strNewAssetnum + " to be replaced by an existing asset  already exists",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetupd_detailsSetRemote.getMbo(i).setValue("statusdate",MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            
            # Ensure existing asset exists
            assetSetRemote2.setUserWhere("siteid='FAC' and assetnum='" + strExistingAssetnum + "'")
            assetSetRemote2.reset() 
            
            if (assetSetRemote2.isEmpty()):               
                insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strExistingAssetnum,strExistingAssetnum,"WARNING","Existing asset " + strExistingAssetnum + "  to be replaced by a new asset does not exist.")
                assetupd_detailsSetRemote.getMbo(i).setValue("status","WARNING: Existing asset " + strExistingAssetnum + " to be replaced by a new asset does not exist",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetupd_detailsSetRemote.getMbo(i).setValue("statusdate",MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            else:                
                #Now decommission the existing asset              
                if (assetSetRemote2.getMbo(0).getString("status") != "DECOMMISSIONED"):
                    assetSetRemote2.getMbo(0).changeStatus('DECOMMISSIONED', False, True, True, True) # rollToAllChildren, removeFromActiveRoutes, removeFromActiveSP,changePMStatus
                    assetSetRemote2.save()
                  
            
            # Add the new asset which is replaced by an old asset
            assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + strNewAssetnum + "'")
            assetSetRemote.reset() 
            
            if (assetSetRemote.isEmpty()):                
                assetSet=assetSetRemote.add()                
                assetSet.setValue("assetnum", strNewAssetnum, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetSet.setValue("lbl_oldassetnum",  strExistingAssetnum, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            else:
                assetSet=assetSetRemote.getMbo(0)
                assetSet.setValue("lbl_oldassetnum",  strExistingAssetnum, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
            boolAssetToBeAdded=True
            
                
            #Initialize the values 
            strLocation="zzBlankzz"
            strDescription="zzBlankzz"
            strLblAssetclassification ="zzBlankzz"
            strAssetMfr="zzBlankzz"
            strAssetSerialnum="zzBlankzz"
            strAssetModel="zzBlankzz"
             
            strAssetnum=strNewAssetnum    
                            
        
        if (isBlank(strAssetnum) != True):
            print "now processing assetnum : " +    strAssetnum
         
            # Update location if different (move, modify)           
            if (strLocation != assetupd_detailsSetRemote.getMbo(i).getString("location")):
                # Validate new location
                strTemp=getLocDesc(assetupd_detailsSetRemote.getMbo(i).getString("location"),runAsUserInfo1)
                 
                if (isBlank(strTemp) == True):
                    boolError=True
                    insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strAssetnum,strAssetnum, "ERROR","Invalid location " +assetupd_detailsSetRemote.getMbo(i).getString("location"))
                else:
                    if (boolAssetToBeAdded == True): # Do not perform move-modify - just change the location
                        assetSet.setValue("location", assetupd_detailsSetRemote.getMbo(i).getString("location"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
          
                    else:
                        
                        assetSet.moveAssetWithinNonInventory(assetupd_detailsSetRemote.getMbo(i).getString("location"),"Changed by script", MXServer.getMXServer().getDate(), "IT-BS-MXINTADM", "","", False,False,False) # wonum, toParent, checkMismatch, checkOccupied,updateWo
                        assetSetRemote.save()
                      
                        
                        # Refetch MBO
                        assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + strAssetnum + "'")
                        assetSetRemote.reset()             
                        if (not assetSetRemote.isEmpty()):
                            assetSet=assetSetRemote.getMbo(0)                

             
            # Update description if different
            
            if (strDescription != assetupd_detailsSetRemote.getMbo(i).getString("description")):
                if (isBlank(assetupd_detailsSetRemote.getMbo(i).getString("description"))== True):
                    boolError=True
                    insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strAssetnum,strAssetnum,"ERROR","Asset description should not be blank")
                else:
                    assetSet.setValue("description", assetupd_detailsSetRemote.getMbo(i).getString("description"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

            # Update classification if different
            if (strLblAssetclassification != assetupd_detailsSetRemote.getMbo(i).getString("classification")):
                assetSet.setValue("lbl_asset_classification", assetupd_detailsSetRemote.getMbo(i).getString("classification"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
          
            # Update if manufacturer different
           
            if (strAssetMfr != assetupd_detailsSetRemote.getMbo(i).getString("manufacturer")):
                
                if (isBlank(assetupd_detailsSetRemote.getMbo(i).getString("manufacturer"))== True):
                    assetSet.setValue("manufacturer", "",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                else:
                                        
                    # Validate manufacturer
                    strTemp=getCompanyDesc(assetupd_detailsSetRemote.getMbo(i).getString("manufacturer"),runAsUserInfo1)
                    
                    if (isBlank(strTemp) == True):
                        boolError=True
                        insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strAssetnum,strAssetnum,"ERROR","Invalid manufacturer " + assetupd_detailsSetRemote.getMbo(i).getString("manufacturer"))
                    else:                  
                        assetSet.setValue("manufacturer", assetupd_detailsSetRemote.getMbo(i).getString("manufacturer"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                          

            # Update if model different
            if (strAssetModel != assetupd_detailsSetRemote.getMbo(i).getString("model")):
                assetSet.setValue("lbl_model", assetupd_detailsSetRemote.getMbo(i).getString("model"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
          
            # Update if serialnum different
            if (strAssetSerialnum != assetupd_detailsSetRemote.getMbo(i).getString("serialnum")):
                assetSet.setValue("serialnum", assetupd_detailsSetRemote.getMbo(i).getString("serialnum"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)    
            
            
            strStartTemp=assetupd_detailsSetRemote.getMbo(i).getString("strategy")
            if (isBlank(strStartTemp)==False):
                
                strStrategyCombined=strStartTemp.split("-")
                   
                # for each word in the line:
                strStrategy=""
                for j, val in enumerate(strStrategyCombined):
                    if (j==0):
                        strStrategy=val
                        strStrategy=strStrategy.strip()
                # Validate strategy
                
                strTemp=getDomainDesc("LBL_ASSETSTRATEGY", strStrategy, runAsUserInfo1)
                if (isBlank(strTemp) == True):
                    
                    boolError=True
                    insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strAssetnum,strAssetnum,"ERROR","Invalid strategy " + strStrategy)
                else:                  
                    assetSet.setValue("lbl_strategy", strStrategy,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    strStartTemp=assetupd_detailsSetRemote.getMbo(i).getString("strategy_comments")    
                    if (isBlank(strStartTemp)==False):
                        assetSet.setValue("LBL_STRATEGY_LONGDESCRIPTION", strStartTemp,  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
                     
            if (boolError == False):
                assetupd_detailsSetRemote.getMbo(i).setValue("status","SUCESSS: Record successfully updated",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetupd_detailsSetRemote.getMbo(i).setValue("statusdate", MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetSet.setValue("CHANGEBY", "IT-BS-MXINTADM",  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetSet.setValue("CHANGEDATE", MXServer.getMXServer().getDate(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            
                insert_asset_log(lbl_assetupd_logRemote,runAsUserInfo1,strAssetnum, strAssetnum, "SUCCESS", "Record successfully updated")
            else:
                assetupd_detailsSetRemote.getMbo(i).setValue("status", "ERROR: Error in updating asset record",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                assetupd_detailsSetRemote.getMbo(i).setValue("statusdate", MXServer.getMXServer().getDate(),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                
            assetSetRemote.save()
                    
            # Refetch MBO
            
            assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + strAssetnum + "'")
            assetSetRemote.reset()             
            if (not assetSetRemote.isEmpty()):
                assetSet=assetSetRemote.getMbo(0)                
    
            # If desired status is decommissioned and the existing status is not decommissioned then, decommissioned the asset 
            if (strDesiredStatus.upper()=='DECOMISSIONED' or strDesiredStatus.upper()=='DECOMMISSIONED'): 
                    assetSet.changeStatus('ACTIVE', False, True, True, True) # rollToAllChildren, removeFromActiveRoutes, removeFromActiveSP,changePMStatus
                    assetSetRemote.save()
                    time.sleep(1)
                    
                    # Re-fetch
                    assetSetRemote.setUserWhere("siteid='FAC' and assetnum='" + strAssetnum + "'")
                    assetSetRemote.reset()             
                    if (not assetSetRemote.isEmpty()):
                        assetSet=assetSetRemote.getMbo(0)
                        assetSet.changeStatus('DECOMMISSIONED', False, True, True, True) # rollToAllChildren, removeFromActiveRoutes, removeFromActiveSP,changePMStatus
                        assetSetRemote.save()
                        
                     
            # If desired status is Operating and the existing status is not Operating then, change status to Operating 
            if (strDesiredStatus.upper()=='OPERATING' and assetSet.getString("status") !='OPERATING'):
                    assetSet.changeStatus('OPERATING', False, True, True, True) # rollToAllChildren, removeFromActiveRoutes, removeFromActiveSP,changePMStatus
                    assetSetRemote.save()    
                        
           
            #assetSetRemote.getMbo(0).changeStatus('OPERATING', True, True, True, True) # rollToAllChildren, removeFromActiveRoutes, removeFromActiveSP,changePMStatus
            #assetSetRemote.getMbo(0).moveAssetWithinNonInventory("069-0102D","Changed by script", MXServer.getMXServer().getDate(), "IT-BS-MXINTADM", "","", False,False,False) # wonum, toParent, checkMismatch, checkOccupied,updateWo
            #dupasset2=assetSetRemote.getMbo(0).duplicate()
            #dupasset2.setValue("orgid",'LBNL',MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            #dupasset2.setValue("siteid",'FAC',MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            #dupasset2.setValue("assetnum",'DUPLASSET3',MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            #dupasset2.setValue("description",'Duplicated asset3 from API',MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            #dupasset2.setValue("status",'OPERATING',MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
             
                         
assetupd_detailsSetRemote.save()

#########################################################################        
# Phase-2 to update the references of jpassetsplink, route_stop and PMs.
#########################################################################
assetSetRemote.setUserWhere("siteid='FAC' and lbl_oldassetnum is not null")
assetSetRemote.reset() 
            
if (not assetSetRemote.isEmpty()):
    intCount=assetSetRemote.count()
    # Loop through each row from the collection
    for i in xrange(intCount):
        
        ###################################### 
        # Update route_stop, replace assetnum
        ######################################
        strAssetnum=assetSetRemote.getMbo(i).getString("lbl_oldassetnum") # Replacement
        
        if (isBlank(strAssetnum)== False):
               
            print "updating route_stops for " + strAssetnum
            
            route_stopRemote.setUserWhere("siteid='FAC' and assetnum='" + strAssetnum + "'")
            route_stopRemote.reset()
            if (not route_stopRemote.isEmpty()):                
                    intCount2=route_stopRemote.count()
                    for j in xrange(intCount2):
                        route_stopRemote.getMbo(j).setValue("lbl_oldassetnum",strAssetnum, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                        route_stopRemote.getMbo(j).setValue("assetnum", assetSetRemote.getMbo(i).getString("assetnum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            route_stopRemote.save()
              
            ########################################## 
            # Update jpassetsplink, replace assetnum
            ###########################################
            print "updating jpassetsplink for " + strAssetnum
            
            jpassetsplinkRemote.setUserWhere("siteid='FAC' and assetnum='" + strAssetnum + "'")
            jpassetsplinkRemote.reset()
            if (not jpassetsplinkRemote.isEmpty()):
                intCount2=jpassetsplinkRemote.count()
                for j in xrange(intCount2):                                  
                    jpassetsplinkRemote.getMbo(j).setValue("lbl_oldassetnum",strAssetnum, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    jpassetsplinkRemote.getMbo(j).setValue("assetnum", assetSetRemote.getMbo(i).getString("assetnum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            jpassetsplinkRemote.save()
            
            ########################################## 
            # Update PM , replace assetnum
            ###########################################
            print "updating PMs for " + strAssetnum
            
            pmRemote.setUserWhere("siteid='FAC' and assetnum='" + strAssetnum+ "'")
            pmRemote.reset()
            if (not pmRemote.isEmpty()):
               
                intCount2=pmRemote.count()
                for j in xrange(intCount2):
                    pmRemote.getMbo(j).setValue("lbl_oldassetnum",strAssetnum, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    pmRemote.getMbo(j).setValue("assetnum", assetSetRemote.getMbo(i).getString("assetnum"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    pmRemote.getMbo(j).setValue("status","ACTIVE", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                    
            pmRemote.save()
            lbl_assetupd_logRemote.save()                
            
##################################################################################
# Phase-3 add attached document to the new assets replaced by the existing assets.
##################################################################################
assetSetRemote.setUserWhere(" asset.assetnum in (select distinct a.lbl_oldassetnum from asset a  where a.lbl_oldassetnum is not null) ")
assetSetRemote.reset()

if (not assetSetRemote.isEmpty()):
    intCount=assetSetRemote.count()
    # Loop through each row from the collection
    for i in xrange(intCount):
                
        doclinksSetRemote.setWhere("ownertable='ASSET' and ownerid=" +str(assetSetRemote.getMbo(i).getInt("assetuid")))
        doclinksSetRemote.reset()
        if (not doclinksSetRemote.isEmpty()):
               
                intCount3=doclinksSetRemote.count()
                for k in xrange(intCount3):
                    # Get asstuid of the new asset
                    assetSetRemote2.setWhere("siteid='FAC' and lbl_oldassetnum='" +assetSetRemote.getMbo(i).getString("assetnum") + "'")
                    assetSetRemote2.reset()
                    if (not assetSetRemote2.isEmpty()):
                        doclinksSetRemote2.setWhere ("ownertable='ASSET' and ownerid=" + str(assetSetRemote2.getMbo(0).getInt("assetuid")))
                        doclinksSetRemote2.reset()
                        
                        if (doclinksSetRemote2.isEmpty()):                            
                                                         
                            doclinksSet=doclinksSetRemote2.add()
                            doclinksSet.setValue("document", doclinksSetRemote.getMbo(k).getString("document"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            doclinksSet.setValue("doctype",  doclinksSetRemote.getMbo(k).getString("doctype"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            doclinksSet.setValue("ownertable","ASSET", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            doclinksSet.setValue("printthrulink",doclinksSetRemote.getMbo(k).getInt("printthrulink"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            doclinksSet.setValue("copylinktowo", doclinksSetRemote.getMbo(k).getInt("copylinktowo"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            doclinksSet.setValue("docinfoid",    doclinksSetRemote.getMbo(k).getInt("docinfoid"),     MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            doclinksSet.setValue("ownerid",      assetSetRemote2.getMbo(0).getInt("assetuid"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                    
                    doclinksSetRemote2.save()
            


            