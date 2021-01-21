'''
Created on September 07, 2016

@author: pmuramalla

Input Variables
@var jI_Orgid : ORGID
@var jI_Siteid : SITEID
@var jI_Assettype : ASSETTYPE

Output Variables
@var jIO_Assetnum : ASSETNUM

@summary: 
         Assign uniquely generated KNumber for Assetnum for a newly created Key Asset if Application Name is "LBL_KEYS"
                  :&APPNAME& in ('LBL_KEYS')
         If the generated KNumber is already assigned, create a new KNumber by invoking the autokey.nextvalue()        
'''

from psdi.server import MXServer
from psdi.security import ConnectionKey
from psdi.mbo import AutoKey
from psdi.mbo import Mbo
from psdi.mbo import MboSet
from psdi.mbo import MboSetRemote

# If a KNumber already exists display warning message 
if  jIO_Assetnum:
    errorkey='ClearKNumberToGenerateNew'
    errorgroup='asset'    

if (app=="LBL_KEYS" and onadd==True and jI_Assettype == 'KEY'):
    # Get object reference    
    objRef = MXServer.getMXServer().getMaximoDD().getMboSetInfo("ASSET")

    # Get attribute reference
    attRef = objRef.getMboValueInfo("LBL_KNUMBER")

    # Simulate &AUTOKEY& 
    conKey = ConnectionKey(mbo.getUserInfo())
    con = mbo.getMboServer().getDBConnection(conKey)
    myAutokey = AutoKey(con, attRef, mbo.getUserInfo(), mbo, objRef)

    
    # Asset MBO SET
    mbosetAsset = MXServer.getMXServer().getMboSet("ASSET", mbo.getUserInfo())
    
    strQuote ="'"
    strWhere1 = " orgid=" + strQuote  + jI_Orgid + strQuote  + " and siteid=" + strQuote + jI_Siteid + strQuote
    KnumberDontExist = True
    
    # Generate a unique KNumber, that is not assigned to an existing Asset or Key Asset
    while KnumberDontExist:
        tempAutokey=myAutokey.nextValue()   # generate new K Number

        prefix=tempAutokey[0]               # get prefix
        suffix=tempAutokey[1:]              # get suffix
        suffix=str(int(suffix))                  # convert to integer to truncate leading zeros

        strKNumber = prefix + suffix

        # Update the where clause with newly generated K Number to check if it already exists.
        strWhere2 = " and assetnum = " + strQuote  + strKNumber + strQuote ;
        strWhere  = strWhere1 + strWhere2      
        
        #Check if the new KNumber is associated with existing Asset
        mbosetAsset.setWhere(strWhere)
        mbosetAsset.reset()
    
        if mbosetAsset.isEmpty():
            print " KNumber = "+ strKNumber + " is not assigned to a different KEY Asset"
            KnumberDontExist = False
            jIO_Assetnum       = strKNumber