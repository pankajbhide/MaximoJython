from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap



if (jIResource_type == "CRAFT" and ondelete == False):

    thisSet=mbo.getThisMboSet()
    intCount=thisSet.count()
    

    if (onadd==True):
        intCount=intCount-1
        

    for i in xrange(intCount):

        thisRow = thisSet.getMbo(i)
        

        if (thisRow.getString("resource_type") + thisRow.getString("craft") == "CRAFT" + jICraft):
              thisSet = None
              boolError=True
              ctx = HashMap()
              ctx.put("paramErrorkey","lbl_duplicatecraft")
              ctx.put("paramErrorgroup","lbl_wkthruops")
              ctx.put("paramParams","")
              service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx) 
          
              break