################################################################
# Purpose: Script for action level launch for MEL number 
#
# Author : Pankaj Bhide
#
# Date    : July 18,2019
#
# Revision
# History : 
#
######################################################E

#Output Variables
#@var jIO_Assetnum : ASSETNUM

'''@summary: 
         Assign uniquely generated MEL numbner for Assetnum for a newly created Key MEL if Application Name is "LBLMEL"
                  :&APPNAME& in ('LBLMEL')
         If the generated KNumber is already assigned, create a new MEL number by invoking the autokey.nextvalue()        
'''

from psdi.server import MXServer
from psdi.security import ConnectionKey
from psdi.mbo import AutoKey
from psdi.mbo import Mbo
from psdi.mbo import MboSet
from psdi.mbo import MboSetRemote


# If a MELNumber already exists display warning message 
if  jIO_Assetnum:
    errorkey='ClearMELNumToGenerateNew'
    errorgroup='asset'    

if (app=="LBLMEL" and onadd==True and mbo.getBoolean("lbl_ismel")==True):
    # Get object reference    
    objRef = MXServer.getMXServer().getMaximoDD().getMboSetInfo("ASSET")

    # Get attribute reference
    attRef = objRef.getMboValueInfo("LBL_MEL_AUTONUM")

    # Simulate &AUTOKEY& 
    conKey = ConnectionKey(mbo.getUserInfo())
    con = mbo.getMboServer().getDBConnection(conKey)
    myAutokey = AutoKey(con, attRef, mbo.getUserInfo(), mbo, objRef)

    
    # Asset MBO SET
    mbosetAsset = MXServer.getMXServer().getMboSet("ASSET", mbo.getUserInfo())
    
    strQuote ="'"
    strWhere1 = " orgid=" + strQuote  + "LBNL" + strQuote  + " and siteid=" + strQuote + "FAC" + strQuote
    MELnumberDontExist = True
    
    # Generate a unique KNumber, that is not assigned to an existing Asset or Key Asset
    while MELnumberDontExist:
        tempAutokey=myAutokey.nextValue()   # generate new MEL Number

        prefix=tempAutokey[:3]              # get prefix
        suffix=tempAutokey[4:]              # get suffix
        
                 
        temp1=str(int(suffix)) # convert to integer to get rid of zeros                                   
        suffix=temp1.zfill(7) # prefix zeros
             
        
        strMELNumber = prefix + suffix

        # Update the where clause with newly generated K Number to check if it already exists.
        strWhere2 = " and assetnum = " + strQuote  + strMELNumber + strQuote ;
        strWhere  = strWhere1 + strWhere2      
        
        #Check if the new KNumber is associated with existing Asset
        mbosetAsset.setWhere(strWhere)
        mbosetAsset.reset()
    
        if mbosetAsset.isEmpty():
            print " MELNumber = "+ strMELNumber + " is not assigned to a different MEL Asset"
            MELnumberDontExist = False
            jIO_Assetnum       = strMELNumber
            jIO_Assetnum_readonly=True