##########################################################################
# Purpose: Script for inserting rows in labtrans MBO based upon the JSON
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
laborsetRemote= MXServer.getMXServer().getMboSet("laborcraftrate", runAsUserInfo1)


conKey = mxServer.getSystemUserInfo().getConnectionKey()



################################################################################
# If siteid and work order are not null then, get reference of tooltrans records
################################################################################

con = mxServer.getDBManager().getConnection(conKey)

myLogger.debug("PRB number of records in LBNLBATCH : " + str(len(reqData)))

for i in range(len(reqData)):

    obj=reqData[i]
    row_count =row_count + 1
    
    obj["_data"]["transdate"] ="" if ( not "transdate" in obj["_data"])  else obj["_data"]["transdate"]  
    obj["_data"]["enterdate"] ="" if ( not "enterdate" in obj["_data"])  else obj["_data"]["enterdate"]     
    obj["_data"]["payrate"] ="" if ( not "payrate" in obj["_data"])  else obj["_data"]["payrate"]     
    obj["_data"]["laborcode"] ="" if ( not "laborcode" in obj["_data"])  else obj["_data"]["laborcode"]     
    obj["_data"]["lt1"] ="" if ( not "lt1" in obj["_data"])  else obj["_data"]["lt1"]
    obj["_data"]["memo"] ="" if ( not "memo" in obj["_data"])  else obj["_data"]["memo"]  
    obj["_data"]["regularhrs"] ="" if ( not "regularhrs" in obj["_data"])  else obj["_data"]["regularhrs"]     
    obj["_data"]["startdate"] ="" if ( not "startdate" in obj["_data"])  else obj["_data"]["startdate"]     
    obj["_data"]["linecost"] ="" if ( not "linecost" in obj["_data"])  else obj["_data"]["linecost"]     
    obj["_data"]["financialperiod"] ="" if ( not "financialperiod" in obj["_data"])  else obj["_data"]["financialperiod"]     
    obj["_data"]["linecost"] ="" if ( not "linecost" in obj["_data"])  else obj["_data"]["linecost"]     
    obj["_data"]["refwo"] ="" if ( not "refwo" in obj["_data"])  else obj["_data"]["refwo"]    
                         
    transdate=obj["_data"]["transdate"] # yyyy-mm-dd 
    enterdate=obj["_data"]["enterdate"] 
    laborcode=obj["_data"]["laborcode"] 
    payrate=obj["_data"]["payrate"]
    lt1=obj["_data"]["lt1"]
    memo=obj["_data"]["memo"] 
    regularhrs=obj["_data"]["regularhrs"] 
    startdate=obj["_data"]["startdate"] 
    linecost=obj["_data"]["linecost"] 
    financialperiod=obj["_data"]["financialperiod"] 
    refwo=obj["_data"]["refwo"]
   
    assetnum=""
    gldebitacct=""
    location=""
    
    strWhere1 =" orgid='LBNL' and siteid='FAC' and wonum='" + refwo + "'"
    wosetRemote.setUserWhere(strWhere1)
    if (not wosetRemote.isEmpty()):
        assetnum=wosetRemote.getMbo(0).getString("assetnum")
        location=wosetRemote.getMbo(0).getString("location")
        gldebitacct=wosetRemote.getMbo(0).getString("glaccount")
    # craft=obj["_data"]["craft"]
    craft=""
        
    strWhere1 =" laborcode='" + laborcode +"' and defaultcraft=1 "
    laborsetRemote.setUserWhere(strWhere1)
    if (not laborsetRemote.isEmpty()):
        craft=laborsetRemote.getMbo(0).getString("craft")
   # assetnum=obj["_data"]["assetnum"]
   # gldebitacct=obj["_data"]["gldebitacct"]
   # location=obj["_data"]["location"]
    
    strInsert= "insert into labtrans "
    strInsert += " ( TRANSDATE, LABORCODE, CRAFT, PAYRATE, " 
    strInsert += "  ASSETNUM , REFWO, REGULARHRS, ROLLUP, "                 
    strInsert += "  PREMIUMPAYHOURS, ENTERBY, ENTERDATE, TRANSTYPE, " 
    strInsert += "  OUTSIDE, GLDEBITACCT, LINECOST, ENTEREDASTASK,   "  
    strInsert += "  FINANCIALPERIOD, LOCATION, LT1, MEMO, "
    strInsert += "  STARTDATE, GENAPPRSERVRECEIPT, LABTRANSID, ORGID, " 
    strInsert += "  SITEID) values "
    strInsert += "   (?, ?,?,?,"
    strInsert += "   ?, ?,?,?,"
    strInsert += "   ?, ?,?,?,"
    strInsert += "   ?, ?,?,?,"
    strInsert += "   ?, ?,?,?,"
    strInsert += "   ?, ?, ?,?,"
    strInsert += "   ?)"

    
    myStatement1 = con.prepareStatement("SELECT labtransseq.NEXTVAL myid FROM DUAL")             
    rs=myStatement1.executeQuery()
    while rs.next():       
        labtransid=rs.getLong("myid")
        
    myStatement1=None 
    rs=None

    preparedStmt = con.prepareStatement(strInsert)
   
    preparedStmt.setDate     (1,Date.valueOf(transdate))
    preparedStmt.setString   (2,laborcode )      
    preparedStmt.setString   (3,craft ) # craft
    preparedStmt.setDouble   (4,float(payrate) )
    preparedStmt.setString   (5,assetnum ) # assetnum
    preparedStmt.setString   (6,refwo)
    preparedStmt.setDouble   (7,float(regularhrs))
    preparedStmt.setInt      (8,0) #rollup
    preparedStmt.setInt      (9,0)#prempayhours
    preparedStmt.setString   (10,"IT-BS-MXINTADM")
    preparedStmt.setDate     (11,Date.valueOf(enterdate))
    preparedStmt.setString   (12,"WORK")
    preparedStmt.setInt      (13,0) #outside
    preparedStmt.setString   (14,gldebitacct) #
    preparedStmt.setDouble   (15,float(linecost))
    preparedStmt.setInt      (16,0) #enteredtask
    preparedStmt.setString   (17,financialperiod)
    preparedStmt.setString   (18,location) # location
    preparedStmt.setString   (19,lt1) 
    preparedStmt.setString   (20,memo) 
    preparedStmt.setDate     (21,Date.valueOf(startdate))
    preparedStmt.setInt      (22,1) #genappr
    preparedStmt.setLong     (23,long(labtransid))
    preparedStmt.setString   (24,"LBNL")
    preparedStmt.setString   (25,"FAC")  
    

    preparedStmt.executeUpdate()
    preparedStmt.close()
   
    
try:
    con.commit()
     
    

except:
    con.rollback()
    
finally:

    con.close()
    mxServer.getDBManager().freeConnection(conKey)

wosetRemote=None  
laborsetRemote=None
preparedStmt.close()  




     

