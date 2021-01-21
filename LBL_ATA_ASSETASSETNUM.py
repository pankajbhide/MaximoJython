##################################################### 
# Purpose: Script to format auto generated asset num 
#          Also make it read-only.
#
# Author : Pankaj Bhide
#
# Date    : Sept 15, 2017
#
# Revision
# History : 
#
######################################################

from psdi.server import MXServer

if (onadd == True):
    
    # Get reference to lbl_maxvars collection
    lblmaxvarsSet= MXServer.getMXServer().getMboSet("LBL_MAXVARS", mbo.getUserInfo())
        
     # Read the desired length of the work order 
     # from lbl_maxvars table
              
    strWhere="varname='LBL_WKTRHULENGTH' and orgid='" + "LBNL" + "' and siteid='" + "FAC"+  "'"
   

    lblmaxvarsSet.setUserWhere(strWhere)
    lblmaxvars= lblmaxvarsSet.getMbo(0)
    intWkthruLength=int(lblmaxvars.getString("varvalue"))
    lblmaxvarsSet = None
   
    
    # If the length of the generated work order number is greater
    # than the desired length, then, format the number
    if (len(jIOAssetnum) > intWkthruLength):
    
        prefix=jIOAssetnum[:4]  # get prefix
        suffix=jIOAssetnum[5:] # get unformatted suffix
        
                  
        # format suffix
        temp1=str(int(suffix)) # convert to integer to get rid of zeros                                   
        suffix=temp1.zfill(intWkthruLength-len(prefix)) # prefix zeros
        
                     
        # Associate formatted suffix to walk thru id (out-bound variable)
        jIOAssetnum=prefix + suffix
        
    jIOAssetnum_readonly = True