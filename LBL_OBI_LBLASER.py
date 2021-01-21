################################################################
# Purpose: Script for object level (init) launch ASSET (Laser)
#
# Author : Pankaj Bhide
#
# Date    : May 13, 2016
#
# Revision
# History : 
#
######################################################
from psdi.server import MXServer
from psdi.security import ConnectionKey
from psdi.mbo import AutoKey
from psdi.mbo import Mbo
from psdi.mbo import MboSet
from psdi.mbo import MboSetRemote
from psdi.mbo import MboConstants


if (app=="LBLLASER"):
    
   
    if (onadd==True):      
        # Get object reference    
        objRef = MXServer.getMXServer().getMaximoDD().getMboSetInfo("LBL_LASER")    
        # Get attribute reference
        attRef = objRef.getMboValueInfo("ASSETNUM")    
        # Simulate &AUTOKEY& 
        conKey = ConnectionKey(mbo.getUserInfo())
        con = mbo.getMboServer().getDBConnection(conKey)
        myAutokey = AutoKey(con, attRef, mbo.getUserInfo(), mbo, objRef)        
        tempAutokey=myAutokey.nextValue()   # generate new K Number
        
        
        suffix=tempAutokey[3:] # get unformatted suffix
        # format suffix
        temp1=str(int(suffix)) # convert to integer to get rid of zeros                                   
        suffix=temp1.zfill(5) # prefix zeros               
        jIOAssetnum='LAS' + suffix
        mbo.setValue("status","INACTIVE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    
    jIOAssetnum_readonly=True    
        
              
        
               
               
      
        
       
        
   

    
    
    