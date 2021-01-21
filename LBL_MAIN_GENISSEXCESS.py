####################################################################
# Purpose: Script for generating issue entries in matusetrans
#          representing issues of excess items into excess store room
#
# Author : Pankaj Bhide
#
# Date    :
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
from java.util import Date
from java.text import SimpleDateFormat
from java.lang import System
from com.ibm.json.java import JSONObject
from org.python.core.util import StringUtil
from com.ibm.tivoli.maximo.oslc import OslcUtils
from com.ibm.tivoli.maximo.oslc.provider.OslcRequest import *
from psdi.util.logging import MXLoggerFactory

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True



def getAvgCost(strItemnum, strLocation):
    dblAvgcost=None
    invcostSet = MXServer.getMXServer().getMboSet("invcost", runAsUserInfo1)
    invcostSet.setUserWhere("itemnum='" + strItemnum +"' and location='" + strLocation +"'")
    if (not invcostSet.isEmpty()):
                dblAvgcost=invcostSet.getMbo(0).getDouble("avgcost")
    invcostSet=None      
    return dblAvgcost



mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")

conKey = mxServer.getSystemUserInfo().getConnectionKey()
inventorySet= MXServer.getMXServer().getMboSet("inventory", runAsUserInfo1)


# Reads the data from batch_maximo.lbl_excess table that contains rows indicating 
# the item need to be excessed. 
# Get JDBC connection from mxserver

myLogger = MXLoggerFactory.getLogger("maximo.script.customscript")
con = mxServer.getDBManager().getConnection(conKey)


# Prepare to get the data from batch_maximo.lbl_excess_2020table
strSelectStat1="select a.item as item, to_number(a.bal) as quantity, a.loc as loc, a.bin as bin";
strSelectStat1 +=" from batch_maximo.lbl_excess2020 a, maximo.inventory b"; 
strSelectStat1 +=" where  a.item=b.itemnum and b.location=a.loc and a.bin=b.binnum and a.item is not null";

myStatement1 = con.prepareStatement(strSelectStat1)             
Rs1=myStatement1.executeQuery();

#Browse through the record set
while Rs1.next():
    

    #############################################################
    # Iterate through the results set and process each record 
    # from the results set 
    ##########################################################
    
   
    strWhere = " siteid='FAC'"        
    strWhere +=" and itemnum='"   + Rs1.getString("item")+ "'"
    strWhere +=" and location='" + Rs1.getString("loc") + "'"
    strWhere +=" and binnum='" + Rs1.getString("bin") + "'"
    
    myLogger.debug("PRB where : " + strWhere)
        
    inventorySet.reset() # clears the contents of collection - mset refers to INVENTORY
    inventorySet.setWhere(strWhere) # populate collection with new where clause
    
    if (not inventorySet.isEmpty()):
        
        mboInventory=inventorySet.getMbo(0)
        myLogger.debug("PRB found inventory")
        #Invoke the method to create an issue transaction
        mboMatUseTrans=mboInventory.createIssue()
        
        
        dblAvgCost=getAvgCost(Rs1.getString("item"),Rs1.getString("loc"))  
        if (dblAvgCost > 0):
    
            myLogger.debug("PRB proessing item: " + Rs1.getString("item"))
            #Set the values for the mandatory columns
            mboMatUseTrans.setValue("orgid",  "LBNL", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("siteid", "FAC", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("itemnum", Rs1.getString("item"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("binnum", Rs1.getString("bin"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("storeloc", Rs1.getString("loc"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)             
            mboMatUseTrans.setValue("issuetype", "ISSUE", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("memo", "Created via LBNL Batch program", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("quantity", (Rs1.getDouble("quantity")*-1), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("QtyRequested", Rs1.getDouble("quantity"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("unitcost", dblAvgCost, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("linecost", (Rs1.getDouble("quantity")*dblAvgCost), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("actualcost", (Rs1.getDouble("quantity")*dblAvgCost), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("actualdate", mxServer.getDate(),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("EnterBy", "IT-BS-MXINTADM", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("CurrencyCode", "USD", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("ISSUETO", "IT-BS-MXINTADM", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("outside", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("rollup", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("SparePartAdded", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("conversion", 1, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("exchangerate", 1, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("gldebitacct",  "104817.002", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("glcreditacct", "104817.004", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            mboMatUseTrans.setValue("transdate", mxServer.getDate(),    MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION);
            
            inventorySet.save()
    
mboMatUseTrans=None   
Rs1=None
myStatement1=None
con=None
        
 

     