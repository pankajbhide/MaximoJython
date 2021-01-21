# Purpose: Object level (save) on TOOLTRANS
#          Sets the value of linecost from lbl_linecost
#          Useful for inserting record from Datastage
#
# Author : Pankaj Bhide
#
# Date    : May 8, 2018
#
# Revision
# History :
#
######################################################

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


def setError(errkey,errgroup, errparm):
    ctx = HashMap()
    ctx.put("paramErrorkey",errkey)
    ctx.put("paramErrorgroup",errgroup)
    ctx.put("paramParams","")
    service.invokeScript("LBL_LIB_SHOWERRORMSG",ctx)


logger = mbo.getMboLogger()


if (mbo.getDouble("lbl_linecost") !=0) :
    mbo.setValue("linecost", mbo.getDouble("lbl_linecost"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("toolqty", 1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("toolrate", mbo.getDouble("lbl_linecost"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)








