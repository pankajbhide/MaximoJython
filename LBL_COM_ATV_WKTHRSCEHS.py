from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap


## Validate uniqueness for EHS Support 
if (jIResource_type == "EHS_SUPPORT" and ondelete == False):

    thisSet=mbo.getThisMboSet()
    intCount=thisSet.count()
    if (onadd==True):
        intCount=intCount-1

    for i in xrange(intCount):

        thisRow = thisSet.getMbo(i)

        if (thisRow.getString("resource_type") + thisRow.getString("ehs_support") == "EHS_SUPPORT" + jIEhs_support):
              thisSet = None
              boolError=True
              ctx = HashMap()
              ctx.put("paramErrorkey","lbl_duplicateehssupport")
              ctx.put("paramErrorgroup","lbl_wkthruops")
              ctx.put("paramParams","")
              service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
                                         
              break