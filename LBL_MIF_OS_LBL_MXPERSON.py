#######################################################
# Purpose: Script for intercepting the inbound traffic
#          for performing extra business processing
#
# Author : Pankaj Bhide
#
# Date    : Nov 18 2017
#
# Revision
# History : 
#
######################################################

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

########################################
# Skip the processing of business rules 
########################################
def mboRules(ctx):
    
    # Bypass transaction if an in-activated employee is already in-activated in MAXIMO
    struc=ctx.getData() # Get data structure from the incoming message
    strLblStatusInMessage=struc.getCurrentData("LBL_STATUS") # Status from incoming message
    
    if (strLblStatusInMessage=='I'):  # Inactive
        
        strPersonid=struc.getCurrentData("PERSONID") # Get employee id
        
        # Now look up the existing value of the status for that employee in MAXIMO
        personSet = MXServer.getMXServer().getMboSet("PERSON", ctx.getUserInfo())       
        strWhere = "personid='" + strPersonid+ "'"                 
        personSet.setUserWhere(strWhere)
        if (personSet.isEmpty()==False):  # employee found in MAXIMO
            strLblStatusInMaximo=personSet.getMbo(0).getString("lbl_status")
            if (strLblStatusInMaximo==strLblStatusInMessage):
                personSet=None # Free up to induce garbage collection
                ctx.skipTxn()  # Skip transaction 
                 
        personSet=None # Free up to induce garbage collection

        
def beforeMboData(ctx):
    
    struc=ctx.getData() # Get data structure from the incoming message          
    # Generate error if supervisor of the employee is same as that employee
        
    if (struc.getCurrentData("PERSONID")==struc.getCurrentData("SUPERVISOR")):
        errorgroup = "iface"
        errorkey ="SKIP_TRANSACTION"        
        
################################################################
# Implement custom logic available after the business object is 
# created/update and values are set in MBO by MIF               
################################################################ 
def preSaveRules(ctx):
    struc=ctx.getData() # Get data structure from the incoming message
    
    # If employee division is FA, then sync data into
    # labor related tables.
    
    if (struc.getCurrentData("LBL_ORG_LEVEL_1")=="FA"):
        # Now look up the existing value of the status for that labor in MAXIMO
        laborSet = MXServer.getMXServer().getMboSet("LABOR", ctx.getUserInfo())       
        strWhere = "laborcode='" + struc.getCurrentData("PERSONID")+ "'"                 
        laborSet.setUserWhere(strWhere)
        
        if (laborSet.isEmpty()==False):  # labor found in MAXIMO
            
            laborSet.getMbo(0).setValue("la3",struc.getCurrentData("lbl_status"))
            laborSet.getMbo(0).setValue("worklocation",struc.getCurrentData("location"))
            laborSet.save()
        else: # record not found, insert
            
            newlabor=laborSet.add()
            #newlabor.setValue("orgid","LBNL")
            newlabor.setValue("worksite","FAC")
            newlabor.setValue("laborcode",struc.getCurrentData("PERSONID"))
            newlabor.setValue("personid",struc.getCurrentData("PERSONID"))
            newlabor.setValue("la3",struc.getCurrentData("lbl_status"))
            newlabor.setValue("worklocation",struc.getCurrentData("location"))
            #newlabor.setValue("status","ACTIVE")
            newlabor.setValue("LBSDATAFROMWO",0)
            newlabor.setValue("AVAILFACTOR",1)
            laborSet.save()
            
        laborSet=None # Free up to induce garbage collection

                      
            
            
        
                   

    
    
            
        
            
        
    
    