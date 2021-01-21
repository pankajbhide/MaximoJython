from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.util import HashMap



## Validate uniqueness for planning team/sequence
if (jIResource_type == "PLANNING_TEAM" and ondelete == False):

    thisSet=mbo.getThisMboSet()
    intCount=thisSet.count()
    if (onadd==True):
        intCount=intCount-1

    for i in xrange(intCount):

        thisRow = thisSet.getMbo(i)

        if (thisRow.getString("resource_type") + str(thisRow.getInt("sequence")) == "PLANNING_TEAM" + str(jISequence)):
              thisSet = None
              boolError=True
              ctx = HashMap()
              ctx.put("paramErrorkey","lbl_duplicatewkthruseq")
              ctx.put("paramErrorgroup","lbl_wkthruops")
              ctx.put("paramParams","")
              service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
              
            
              break
          
## Validate uniqueness for craft/sequence
if (jIResource_type == "CRAFT" and ondelete == False):

    thisSet=mbo.getThisMboSet()
    intCount=thisSet.count()
    if (onadd==True):
        intCount=intCount-1

    for i in xrange(intCount):

        thisRow = thisSet.getMbo(i)

        if (thisRow.getString("resource_type") + str(thisRow.getInt("sequence")) == "CRAFT" + str(jISequence)):
              thisSet = None
              boolError=True
              ctx = HashMap()
              ctx.put("paramErrorkey","lbl_duplicatewkthruseq")
              ctx.put("paramErrorgroup","lbl_wkthruops")
              ctx.put("paramParams","")
              service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)
              
            
              break