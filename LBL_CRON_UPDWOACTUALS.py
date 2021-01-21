####################################################################
# Purpose: Script for updating actuals in work order table 
#          from labtrans and tooltrans
#
# Author : Pankaj Bhide
#
# Date    : Sept 18 2018
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

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

print "PRB about to start the code"
mxServer = MXServer.getMXServer()
runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")

conKey = mxServer.getSystemUserInfo().getConnectionKey()
con = mxServer.getDBManager().getConnection(conKey)


strUpdateStat1 =" update workorder a " 
strUpdateStat1 +="  set a.actlabcost=(select sum(c.linecost)      from labtrans  c where c.siteid='FAC' and c.refwo=a.wonum), " 
strUpdateStat1 +="  a.actlabhrs=(select sum(d.regularhrs)         from labtrans  d where d.siteid='FAC' and d.refwo=a.wonum), "
strUpdateStat1 +="  a.ACTINTLABCOST=(select sum(c.linecost)       from labtrans  c where c.siteid='FAC' and c.refwo=a.wonum), " 
strUpdateStat1 +="  a.ACTINTLABHRS=(select sum(d.regularhrs)      from labtrans  d where d.siteid='FAC' and d.refwo=a.wonum)" 
strUpdateStat1 +="  where a.orgid='LBNL' and a.siteid='FAC' and a.wonum in " 
strUpdateStat1 +="  ( select distinct y.refwo from labtrans y   where y.siteid='FAC' and y.transdate between (sysdate-50) and sysdate and y.lt1 is not null)"


stmtUpdateStat1=con.prepareStatement(strUpdateStat1)
stmtUpdateStat1.executeUpdate()

try:
    stmtUpdateStat1.close()
    con.commit()

except:
    con.rollback()

strUpdateStat1 ="  update workorder a " 
strUpdateStat1 +="  set a.acttoolcost=(select sum(b.linecost) from tooltrans b where b.siteid='FAC' and b.refwo=a.wonum) "
strUpdateStat1 +="  where a.orgid='LBNL' and a.siteid='FAC' and a.wonum in "
strUpdateStat1 +=" (select distinct x.refwo from tooltrans x where x.siteid='FAC' and x.transdate between (sysdate-50) and sysdate and x.tt1 is not null)" 

stmtUpdateStat1=con.prepareStatement(strUpdateStat1)
stmtUpdateStat1.executeUpdate()

try:
    stmtUpdateStat1.close()
    con.commit()

except:
    con.rollback()

 # At the end of the program release the db connection to the pool
mxServer.getDBManager().freeConnection(conKey) 
con=None

