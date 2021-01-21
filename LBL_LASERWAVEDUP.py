################################################################
# Purpose: Script for act ion launch to dupliace laser wave
#
# Author : Pankaj Bhide
#
# Date    : May  14, 2016
#
# Revision
# History :
#
#################################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

boolError=False

logger = mbo.getMboLogger()

laserwaveSet = MXServer.getMXServer().getMboSet("lbl_laserwave", mbo.getUserInfo())
strWhere = " orgid='" + jIOOrgid + "'" + " and siteid='" + jIOSiteid + "'"
strWhere +=" and assetnum='" + jIOAssetnum + "'"  
strWhere +="  order by wavelengthid desc"
laserwaveSet.setUserWhere(strWhere)
newwavelengthid=0

if (not laserwaveSet.isEmpty()):
    intCount=laserwaveSet.count()                           
    for i in xrange(intCount):
        newwavelengthid=laserwaveSet.getMbo(i).getInt("wavelengthid")
        newwavelengthid=newwavelengthid+1
        break

strWhere = " orgid='" + jIOOrgid + "'" + " and siteid='" + jIOSiteid + "'"
strWhere +=" and assetnum='" + jIOAssetnum + "'"  
strWhere +=" and wavelengthid=" + str(jIOWavelengthid) 
laserwaveSet.setUserWhere(strWhere)

if (not laserwaveSet.isEmpty()):
    #newlaserwaveSet = MXServer.getMXServer().getMboSet("lbl_laserwave", mbo.getUserInfo())
    newlaserwaveSet=mbo.getOwner().getMboSet("LBL_LASER2WAVE")
    newlaserwave=newlaserwaveSet.add()
    intCount=laserwaveSet.count()                           
    for i in xrange(intCount):
        laserwave=laserwaveSet.getMbo(i) 
        if (i==0):
            newlaserwave.setValue("duplicated","Y",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newlaserwave.setValue("orgid",jIOOrgid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newlaserwave.setValue("siteid",jIOSiteid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newlaserwave.setValue("assetnum",jIOAssetnum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            newlaserwave.setValue("wavelengthid",newwavelengthid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("wavelength") !=0):
                newlaserwave.setValue("wavelength",laserwave.getFloat("wavelength"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("wavelength_min") !=0):    
                newlaserwave.setValue("wavelength_min",laserwave.getFloat("wavelength_min"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("wavelength_max") !=0):  
                newlaserwave.setValue("wavelength_max",laserwave.getFloat("wavelength_max"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("diameter") !=0):  
                newlaserwave.setValue("diameter",laserwave.getFloat("diameter"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("divergence") !=0):  
                newlaserwave.setValue("divergence",laserwave.getFloat("divergence"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if isBlank(laserwave.getString("wavetype") == False):  
                newlaserwave.setValue("wavetype",laserwave.getString("wavetype"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("pulse_width") !=0):  
                newlaserwave.setValue("pulse_width",laserwave.getFloat("pulse_width"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if isBlank(laserwave.getString("pulse_width_uom") == False):  
                newlaserwave.setValue("pulse_width_uom",laserwave.getString("pulse_width_uom"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("pulse_rep_rate") !=0):  
                newlaserwave.setValue("pulse_rep_rate",laserwave.getFloat("pulse_rep_rate"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if isBlank(laserwave.getString("pulse_rep_rate_uom") == False):  
                newlaserwave.setValue("pulse_rep_rate_uom",laserwave.getString("pulse_rep_rate_uom"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("pulse_energy") !=0):  
                newlaserwave.setValue("pulse_energy",laserwave.getFloat("pulse_energy"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if isBlank(laserwave.getString("pulse_energy_uom") == False):  
                newlaserwave.setValue("pulse_energy_uom",laserwave.getString("pulse_energy_uom"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("max_power") !=0):  
                newlaserwave.setValue("max_power",laserwave.getFloat("max_power"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if isBlank(laserwave.getString("max_power_uom") == False):  
                newlaserwave.setValue("max_power_uom",laserwave.getString("max_power_uom"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)                                
                
            if (laserwave.getFloat("exposuredur") !=0):  
                newlaserwave.setValue("exposuredur",laserwave.getFloat("exposuredur"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)                  
            if (laserwave.getFloat("mpe") !=0):  
                newlaserwave.setValue("mpe",laserwave.getFloat("mpe"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)                  
            if isBlank(laserwave.getString("mpe_uom") == False):  
                newlaserwave.setValue("mpe_uom",laserwave.getString("mpe_uom"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("od") !=0):  
                newlaserwave.setValue("od",laserwave.getFloat("od"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)                                              
            if (laserwave.getFloat("nohd") !=0):  
                newlaserwave.setValue("nohd",laserwave.getFloat("nohd"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if (laserwave.getFloat("skin_mpe") !=0):  
                newlaserwave.setValue("skin_mpe",laserwave.getFloat("skin_mpe"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
            if isBlank(laserwave.getString("skin_mpe_uom") == False):  
                newlaserwave.setValue("skin_mpe_uom",laserwave.getString("skin_mpe_uom"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)                                          
                                              
                                
                           
            
      
newlaserwaveSet.save()        



