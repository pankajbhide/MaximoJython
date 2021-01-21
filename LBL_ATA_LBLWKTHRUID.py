##################################################### 
# Purpose: Script to format walk through number 
#          auto generated 
#          by MAXIMO as per LBNL Facilities Rules.
#          Also make it read-only.
#
# Author : Pankaj Bhide
#
# Date    : July 14, 2015
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
              
    strWhere="varname='LBL_WKTRHULENGTH' and orgid='" + jIOrgid + "' and siteid='" + jISiteid +  "'"
   

    lblmaxvarsSet.setUserWhere(strWhere)
    lblmaxvars= lblmaxvarsSet.getMbo(0)
    intWkthruLength=int(lblmaxvars.getString("varvalue"))
    lblmaxvarsSet = None
   
    
    # If the length of the generated work order number is greater
    # than the desired length, then, format the number
    if (len(jIOWkthruid) > intWkthruLength):
    
        prefix=jIOWkthruid[:4]  # get prefix
        suffix=jIOWkthruid[5:] # get unformatted suffix
        
                  
        # format suffix
        temp1=str(int(suffix)) # convert to integer to get rid of zeros                                   
        suffix=temp1.zfill(intWkthruLength-len(prefix)) # prefix zeros
        
                     
        # Associate formatted suffix to walk thru id (out-bound variable)
        jIOWkthruid=prefix + suffix
        
    jIOWkthruid_readonly = True