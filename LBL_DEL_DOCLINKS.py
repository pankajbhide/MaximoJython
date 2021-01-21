########################################################################
# Purpose: Script for deleting doclinks entries for a given work order
# Author : Pankaj Bhide
#
# Date    : January 2020
#
# Revision
# History :
#
######################################################
from psdi.server import MXServer
from com.ibm.json.java import JSONObject
from org.python.core.util import StringUtil
from com.ibm.tivoli.maximo.oslc import OslcUtils
from psdi.util.logging import MXLoggerFactory
from java.sql import *
from java.text import SimpleDateFormat
from psdi.mbo import MboConstants
from psdi.app.doclink import Docinfo
from psdi.app.doclink import DocinfoSet
from psdi.app.doclink import DocinfoSetRemote
from psdi.app.doclink import DoclinksSetRemote
from java.lang import SecurityException
from java.io import File

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def isNull(myObject):
    if (myObject is None):
        return True
    else:
        return False
    
# COMMENT: function to check if the doclink owner is a commlog or the main mbo.
def isCommLogOwner(doclink):
    ownertable = doclink.getString("OWNERTABLE")
    print('**** OWNERTABLE... '+ownertable)
    if (ownertable) == "COMMLOG":
        return True
    return False


# COMMENT: function to delete the commlog doc physical file from the server.
def deletecommlogfilefromserver(docinfo):

    docinfoid = docinfo.getString("DOCINFOID")
    commlogdocsSet = MXServer.getMXServer().getMboSet("COMMLOGDOCS", docinfo.getUserInfo())
    commlogdocsSet.setWhere("DOCINFOID = '"+docinfoid+"'")
    commlogdocsSet.reset()

    print('**** DOCINFOID... '+docinfoid)

    k = 0
    commlogdoc = commlogdocsSet.getMbo(k)
    while (commlogdoc is not None):
        urlname = commlogdoc.getString("URLNAME")
        deleteCfile = File(urlname)
        if(deleteCfile.exists()):
            deleteCfile.delete();
        k = k+1
        commlogdoc.delete(MboConstants.NOACCESSCHECK)
        commlogdoc = commlogdocsSet.getMbo(k);
    #commlogdocsSet.deleteAll(MboConstants.NOACCESSCHECK)
    commlogdocsSet.save(MboConstants.NOACCESSCHECK)


# COMMENT: function to delete the physical file from the server.
def deletefilefromserver(docinfo):
    urlname = docinfo.getString("URLNAME")
    deletefile = File(urlname)
    if (deletefile.exists()):
        print('**** Deleting file... '+urlname)
        deletefile.delete()
        print('**** File Deleted... '+urlname)
        

strWonum=""
strSrnum=""


myLogger = MXLoggerFactory.getLogger("maximo.script.customscript")

myLogger.debug("PRB starting")
####################################################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently commented
###################################################################

#req_data=JSONObject.parse(requestBody)

reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(requestBody))

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
doclinksSet =MXServer.getMXServer().getMboSet("DOCLINKS", runAsUserInfo1)



for i in range(len(reqData)):

    obj=reqData[i]
    
    obj["documentnumber"]="" if ( not "documentnumber" in obj)  else obj["documentnumber"]
    obj["identifiers"]="" if ( not "identifiers" in obj)  else obj["identifiers"]
    
    if (isBlank(obj["documentnumber"])==False and isBlank(obj["documentnumber"])==False):
        strWonum=obj["documentnumber"]
        
    strWhere=" "
    if (isBlank(obj["identifiers"])==False):      
               
        listIdentifiers=obj["identifiers"].split(",")
        
        strWhere1=" and doclinksid not in ( "
        strWhere2=""
        for strTemp in listIdentifiers:
            if (isBlank(strWhere2)):
                strWhere2 = strTemp
            else:
                strWhere2 += "," + strTemp
        strWhere2 += " ) "
        
        strWhere=strWhere1 + strWhere2
            
            
            
            
    doclinksSet.setUserWhere("ownertable='WORKORDER' and createby='IT-BS-MXINTADM' and  ownerid in (select workorderid from workorder where wonum='" + strWonum + "')" + strWhere)
    
    if (not doclinksSet.isEmpty()):      
           
        i = 0
        doclink = doclinksSet.getMbo(i)
        while (doclink != None):
            docinfoSet = doclink.getMboSet("DOCINFO")
            if (docinfoSet is not None):
                j=0
                docinfo = docinfoSet.getMbo(j)
                while (docinfo != None):
                    if (isCommLogOwner(doclink)):
                        deletecommlogfilefromserver(docinfo)
                    else:
                        print('**** deletefilefromserver... ')
                        deletefilefromserver(docinfo)
                        docinfo.delete(MboConstants.NOACCESSCHECK)
                    doclink.delete(MboConstants.NOACCESSCHECK)    
                    j=j+1
                    docinfo = docinfoSet.getMbo(j)  
            i=i+1
            doclink = doclinksSet.getMbo(i)
            
doclinksSet.save()
       
       
resp = JSONObject()

resp.put("result","Successful")    

if (isBlank(strWonum)==False):
    resp.put("documenttype","WORKORDER")       
    resp.put("documentnumber",strWonum)


responseBody = resp.serialize(True)
     

