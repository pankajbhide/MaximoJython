#######################################################################
# Purpose: Script for attribute level launch (validate)
#         LBL_WOWCDCONDITION.ANSWER
# Author : Pankaj Bhide
#
# Date    : August 25 , 2015
#
# Revision
# History : 
#
######################################################

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from java.util import HashMap


def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams",errparm)
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)


logger = mbo.getMboLogger()

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


if (jIOrgid=="LBNL" and jISiteid=="FAC"):
    

   # Presently Facilities decided not having any sub condition. Therefore
   # this code does not check for duplicate yes in sub condition. However
   # if they decide utilizing sub condition, then, in  a sub condition
   # there must be only one row with YES answer.
   
   if (jIAnswer.lower()=="yes" and jISubconditionnum != 0):
        thisSet=mbo.getThisMboSet()
        intCount=thisSet.count()
        for i in xrange(intCount):

            thisRow = thisSet.getMbo(i)

            if (thisRow.getString("answer").lower()=="yes"):
                if (jIConditionnum == thisRow.getString("conditionnum")):                        
                  if (jISubconditionnum != thisRow.getString("LBL_WCDSUBCONDID")):
                    thisSet = None
                    boolError=True
                    setError("lbl_dupansyes","lbl_wowcdcondition"," ")
                    break
              