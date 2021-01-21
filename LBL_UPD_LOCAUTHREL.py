##########################################################################
# Purpose: Script for updating locations and lbl_auth_Release from 
#          TAD application
#
# Author : Pankaj Bhide
#
# Date    : May 16 2019
#
# Revision
# History :
#
###########################################################################
from psdi.server import MXServer
from com.ibm.json.java import JSONObject
from org.python.core.util import StringUtil
from com.ibm.tivoli.maximo.oslc import OslcUtils
from com.ibm.tivoli.maximo.oslc.provider.OslcRequest import *
from psdi.mbo  import   MboConstants

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

query_string=request.getQueryParam("sequence_no")


#############################################################################################################################################
# Parse query string (delimited by pipe) to get sequence number and user id
# Now read all the locations from lbl_tadselectedlocs where  personid=<user id> and sequence_no=<sequence_no>
# For each location read - set the value of "locations.lbl_rel_reqd="N"
#
#PRB sequence number"2019/05/16:14:36:45:945|813149"
#PRB authinfo: 813149-Y-N,019809-N-N,016323-N-N
#PRB rel reqd: Y

# Parse request body for the following JSON
#[{"lbl_escort_reqd":"N","lbl_cond_release":"N","lbl_comments_condr":"","lbl_rel_reqd":"Y","authinfo":"813149-Y-N,019809-N-N,016323-N-N"} ]
# 

# Delete all the records from lbl_auth_release for all the above locations

# Now insert the records into "lbl_auth_release" for all the above locations with proper authinfo
# Finally re-update locations MBO with the requisite lbl_rel_reqd.
############################375050#################################################################################################################



strSequenceno=""
for item in query_string:
    
    strSequenceno +=item
  



#Parse sequence_number
strTemp=strSequenceno.split("|")

strSeqSelectedRecords=strTemp[0]
strUserid=strTemp[1]


##################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently comment#################

# Get Response body 
resp = str(requestBody)  
# Convert to JSON Array
reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(resp))

# Navigate elements from array 
strAuthInfo=""
strRelReqd=""
strCondRel=""
strEscortReqd=""
strCommentsCondr=""

for i in range(len(reqData)):
    
    strAuthInfo=reqData.get(i).get("authinfo")
    strRelReqd=reqData.get(i).get("lbl_rel_reqd")
    strCondRel=reqData.get(i).get("lbl_cond_release")
    strEscortReqd=reqData.get(i).get("lbl_escort_reqd")
    strCommentsCondr=reqData.get(i).get("lbl_comments_condr")
    

 

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
 

conKey = mxServer.getSystemUserInfo().getConnectionKey()
con = mxServer.getDBManager().getConnection(conKey)





##########################################################################
# Update locations.lbl_rel_reqd to N so that the corresponding records
# from lbl_auth_release can be deleted. 
##########################################################################
locationsSet= MXServer.getMXServer().getMboSet("locations", runAsUserInfo1)

strWhere = " orgid='LBNL' and siteid='FAC' "        
strWhere +=" and location in (select a.location from lbl_tadselectedlocs a where a.sequence_no='" + strSeqSelectedRecords +"' and ";
strWhere +=" a.personid='" + strUserid +"' )"

strDelete= " delete from lbl_auth_release where " + strWhere

stmtDelete=con.prepareStatement(strDelete)
stmtDelete.executeUpdate()
try:
    stmtDelete.close()
    con.commit()

except:
    con.rollback()


# At the end of the program release the db connection to the pool
mxServer.getDBManager().freeConnection(conKey)
stmtDelete=None
conn=None


lblauthrelSet= MXServer.getMXServer().getMboSet("lbl_auth_release", runAsUserInfo1)
    
'''locationsSet.reset() # clears the contents of collection - mset refers to locations
locationsSet.setWhere(strWhere) # populate collection with new where clause
    
if (not locationsSet.isEmpty()):
    intCount=locationsSet.count()
    for i in xrange(intCount):
        locationsSet.getMbo(i).setValue("lbl_rel_reqd", "N", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        
locationsSet.save()
#############################################################################
#Delete the existing records in lbl_auth_release for the selected locations
##############################################################################



  
lblauthrelSet.reset() # clears the contents of collection - mset refers to locations
lblauthrelSet.setWhere(strWhere) # populate collection with new where clause
    
if (not lblauthrelSet.isEmpty()):
    intCount=lblauthrelSet.count()
    for i in xrange(intCount):
        lblauthrelSet.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        
          
lblauthrelSet.save()
'''

    
######################################    
# Insert data into lbl_auth_release   
##################################### 
 
locationsSet= MXServer.getMXServer().getMboSet("locations", runAsUserInfo1)

locationsSet.reset() # clears the contents of collection - mset refers to locations
locationsSet.setWhere(strWhere) # populate collection with new where clause
    
if (not locationsSet.isEmpty()):

    intCount=locationsSet.count()
    
    for i in xrange(intCount):
        
        #split strAuthInfo based upon comma
        if  (strAuthInfo !="DELETED"):
            
            listAuthList=strAuthInfo.split(",")
            
            for strAuthRel in listAuthList:
                
                strtemp2=strAuthRel.split("-")
                strAuthorizer=strtemp2[0]
                strIsPrimary=strtemp2[1]
                strReceiveEmail=strtemp2[2]
                if (strAuthorizer !="DELETED"):
                    newAuthRelease=lblauthrelSet.add()
                    newAuthRelease.setValue("orgid",locationsSet.getMbo(i).getString("orgid"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("siteid",locationsSet.getMbo(i).getString("siteid"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("location",locationsSet.getMbo(i).getString("location"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("building_number",locationsSet.getMbo(i).getString("lo1"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("floor_number",locationsSet.getMbo(i).getString("lo2"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("room_number",locationsSet.getMbo(i).getString("lo3"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("lbl_roof_level",locationsSet.getMbo(i).getString("lbl_roof_level"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("personid",strAuthorizer, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("isprimary",strIsPrimary, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("receive_email",strReceiveEmail, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("changeby", runAsUserInfo1.getUserName(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
                    newAuthRelease.setValue("changedate",mxServer.getDate(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            
            lblauthrelSet.save()
        
        locationsSet.getMbo(i).setValue("lbl_rel_reqd",strRelReqd , MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        locationsSet.getMbo(i).setValue("lbl_cond_release",strCondRel , MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        locationsSet.getMbo(i).setValue("lbl_escort_reqd",strEscortReqd , MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        locationsSet.getMbo(i).setValue("lbl_comments_condr",strCommentsCondr , MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        locationsSet.getMbo(i).setValue("changeby", runAsUserInfo1.getUserName(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        locationsSet.getMbo(i).setValue("changedate",mxServer.getDate(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
        
        
locationsSet.save()


# Cleanup old lbl_tadselectedlocs

 
lblTadselectedlocs= MXServer.getMXServer().getMboSet("lbl_tadselectedlocs", runAsUserInfo1)
lblTadselectedlocs.reset()  
lblTadselectedlocs.setWhere("changedate <= sysdate-1 ") # populate collection with new where clause
    
if (not lblTadselectedlocs.isEmpty()):
    intCount=lblTadselectedlocs.count()
    for i in xrange(intCount):
        lblTadselectedlocs.getMbo(i).delete(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
lblTadselectedlocs.save()

lblTadselectedlocs=None
        
          
lblauthrelSet.save()
        
    
lblauthrelSet=None
locationsSet=None




################################################################


resp = JSONObject()
resp.put("lbl_upd_locauthrel","success")
responseBody = resp.serialize(True)