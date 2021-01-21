from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap

def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams",errparm)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
    
def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

if (onadd==True):
    owner=mbo.getOwner()
    mbo.setValue("assetnum", owner.getString("assetnum"),  MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 

if ((mbo.getName()== "LBL_LASERHIST")):
    if (onadd==True or onupdate==True or ondelete==True):
        if (owner.getString("status") !='INACTIVE'):
              setError("lbl_laserhistorynotallowed","lbl_laser","")