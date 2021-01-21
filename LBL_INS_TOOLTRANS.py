##########################################################################
# Purpose: Script for inserting rows in tooltrans MBO based upon the JSON
#          payload received
#
# Author : Pankaj Bhide
#
# Date    : Sept 2019
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

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


# Get Site id and work order number from the MBO
#strWonum=mbo.getString("wonum")
#strSite=mbo.getString("siteid")


myLogger = MXLoggerFactory.getLogger("maximo.script.customscript")

myLogger.debug("PRB starting")
####################################################################
# The following block will show how to parse the JSON body sent to 
# HTTP Post request
# Presently commented
###################################################################




reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(requestBody))
row_count=0

mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
wosetRemote= MXServer.getMXServer().getMboSet("WORKORDER", runAsUserInfo1)

conKey = mxServer.getSystemUserInfo().getConnectionKey()

################################################################################
# If siteid and work order are not null then, get reference of tooltrans records
################################################################################

con = mxServer.getDBManager().getConnection(conKey)


for i in range(len(reqData)):

    obj=reqData[i]
    row_count =row_count + 1
    
    obj["_data"]["transdate"] ="" if ( not "transdate" in obj["_data"])  else obj["_data"]["transdate"]  
    obj["_data"]["enterdate"] ="" if ( not "enterdate" in obj["_data"])  else obj["_data"]["enterdate"]     
    obj["_data"]["itemnum"] ="" if ( not "itemnum" in obj["_data"])  else obj["_data"]["itemnum"]     
    obj["_data"]["transdate"] ="" if ( not "transdate" in obj["_data"])  else obj["_data"]["transdate"]     
    obj["_data"]["tt1"] ="" if ( not "tt1" in obj["_data"])  else obj["_data"]["tt1"]
    obj["_data"]["memo"] ="" if ( not "memo" in obj["_data"])  else obj["_data"]["memo"]  
    obj["_data"]["regularhrs"] ="" if ( not "regularhrs" in obj["_data"])  else obj["_data"]["regularhrs"]     
    obj["_data"]["startdate"] ="" if ( not "startdate" in obj["_data"])  else obj["_data"]["startdate"]     
    obj["_data"]["linecost"] ="" if ( not "linecost" in obj["_data"])  else obj["_data"]["linecost"]     
    obj["_data"]["financialperiod"] ="" if ( not "financialperiod" in obj["_data"])  else obj["_data"]["financialperiod"]     
    obj["_data"]["linecost"] ="" if ( not "linecost" in obj["_data"])  else obj["_data"]["linecost"]     
    obj["_data"]["refwo"] ="" if ( not "refwo" in obj["_data"])  else obj["_data"]["refwo"]
            
                         
    transdate=obj["_data"]["transdate"]
    enterdate=obj["_data"]["enterdate"] 
    itemnum=obj["_data"]["itemnum"] 
    tt1=obj["_data"]["tt1"]
    memo=obj["_data"]["memo"] 
    regularhrs=obj["_data"]["regularhrs"] 
    startdate=obj["_data"]["startdate"] 
    linecost=obj["_data"]["linecost"] 
    financialperiod=obj["_data"]["financialperiod"] 
    refwo=obj["_data"]["refwo"]
    #assetnum=obj["_data"]["assetnum"]
    #gldebitacct=obj["_data"]["gldebitacct"]
    #location=obj["_data"]["location"]
    assetnum=""
    gldebitacct=""
    location=""
    
    strWhere1 =" orgid='LBNL' and siteid='FAC' and wonum='" + refwo + "'"
    wosetRemote.setUserWhere(strWhere1)
    if (not wosetRemote.isEmpty()):
        assetnum=wosetRemote.getMbo(0).getString("assetnum")
        location=wosetRemote.getMbo(0).getString("location")
        gldebitacct=wosetRemote.getMbo(0).getString("glaccount")

    strInsert= "insert into tooltrans "
    strInsert += " (TRANSDATE,ITEMNUM,TOOLRATE, ASSETNUM, "         
    strInsert += "  TOOLQTY,  TOOLHRS,ENTERDATE, ENTERBY, "
    strInsert += "  OUTSIDE, ROLLUP, ENTEREDASTASK, TT1, "          
    strInsert += "  LINECOST, FINANCIALPERIOD, GLDEBITACCT, LOCATION, "          
    strInsert += "  REFWO, ORGID, SITEID,MEMO, "          
    strInsert += "  TOOLTRANSID, ITEMSETID, EXCHANGERATE2,LANGCODE, "         
    strInsert += "  HASLD, LINECOST2) values "          
   
    strInsert += "   (?, ?,?,?,"
    strInsert += "   ?, ?,?,?,"
    strInsert += "   ?, ?,?,?,"
    strInsert += "   ?, ?,?,?,"
    strInsert += "   ?, ?,?,?,"
    strInsert += "   ?, ?, ?,?,"
    strInsert += "   ?,?  )"

    
    myStatement1 = con.prepareStatement("SELECT tooltransseq.NEXTVAL myid FROM DUAL")             
    rs=myStatement1.executeQuery()
    while rs.next():       
        tooltransid=rs.getLong("myid")
        
    myStatement1=None 
    rs=None

    preparedStmt = con.prepareStatement(strInsert)
   
    preparedStmt.setDate     (1,Date.valueOf(transdate))
    preparedStmt.setString   (2,itemnum )      
    preparedStmt.setDouble   (3, float(linecost)) # toolrate
    preparedStmt.setString   (4,assetnum) 
    preparedStmt.setDouble   (5,1 ) # toolqty
    preparedStmt.setDouble   (6,0) #hrs
    preparedStmt.setDate     (7,Date.valueOf(enterdate))
    preparedStmt.setString   (8,"IT-BS-MXINTADM")
    preparedStmt.setInt      (9,0) #outside
    preparedStmt.setInt      (10,0) #rollup
    preparedStmt.setInt      (11,0)#enteredtask
    preparedStmt.setString   (12,tt1) 
    preparedStmt.setDouble   (13,float(linecost))
    preparedStmt.setString   (14,financialperiod)
    preparedStmt.setString   (15,gldebitacct)
    preparedStmt.setString   (16,location) # location
    preparedStmt.setString   (17,refwo) 
    preparedStmt.setString   (18,"LBNL")
    preparedStmt.setString   (19,"FAC")  
    preparedStmt.setString   (20,memo) 
    preparedStmt.setLong     (21,long(tooltransid))
    preparedStmt.setString   (22,"ILBNL") 
    preparedStmt.setDouble   (23,1 ) # exchangerate2
    preparedStmt.setString   (24,"EN") 
    preparedStmt.setInt      (25,0)#hasld
    preparedStmt.setDouble   (26,float(linecost)) #linecost2
  
    preparedStmt.execute()
    preparedStmt.close()
    
try:
    con.commit()
    
  
except:
    con.rollback()
    
finally:
       
    con.close()
    mxServer.getDBManager().freeConnection(conKey)    

wosetRemote=None   
preparedStmt.close()  
 
     

