################################################################################
# Purpose: Script for object level before save launch point on lbl_json_reports
#          (send email)
#
# Author : Pankaj Bhide
#
# Date    : May 25 2019
#
# Revision
# History :
#
###########################################################################
from psdi.server import MXServer
from com.ibm.json.java import JSONObject, JSONArray
from org.python.core.util import StringUtil
from com.ibm.tivoli.maximo.oslc import OslcUtils
from com.ibm.tivoli.maximo.oslc.provider.OslcRequest import *
from psdi.mbo  import   MboConstants
from psdi.mbo import SqlFormat


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def getPropertyvalue(strProperty):
    mxServer = MXServer.getMXServer()
    runAsUserInfo1 = mxServer.getUserInfo("IT-BS-MXINTADM")
    strPropertyValue=None
    maxpropvalueSet = MXServer.getMXServer().getMboSet("maxpropvalue", runAsUserInfo1)
    maxpropvalueSet.setUserWhere("propname='" + strProperty +"'")
    if (not maxpropvalueSet.isEmpty()):
                strPropertyValue=maxpropvalueSet.getMbo(0).getString("propvalue")
    maxpropvalueSet=None      
    return strPropertyValue


    
strEmailFrom=""
strEmailTo=""
strEmailSubject=""
strReportType=""
strReportTitle=""
strReportBody=""
strReportFooter=""

strEmailFrom=mbo.getString("email_from")
strEmailTo=mbo.getString("email_to")
strEmailSubject=mbo.getString("email_subject")
strReportType=mbo.getString("report_type")
strReportTitle=mbo.getString("report_title")
strReportBody=mbo.getString("report_body")
strReportFooter=mbo.getString("report_footer")

strDisclaimer  = '[Please note that the report is generated from the TEST data. It does not represent the data from the production database.]'


strEmailText ='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
strEmailText = strEmailText  + '<html>'
strEmailText = strEmailText  + '<head>'
strEmailText = strEmailText  + '<title>' + strEmailSubject  + '</title></head><body>'         
strEmailText = strEmailText  + '<TABLE align="left" border="0" width="auto"> '

if (strReportType =="1"):
    strEmailText = strEmailText  + '<TR><TD align="center" VALIGN="TOP"><FONT face="Arial"size="4"><STRONG>' + strReportTitle + '</STRONG></FONT></TD></TR>'
if (strReportType =="2"):
    strEmailText = strEmailText  + '<TR><TD align="left" VALIGN="TOP"><FONT face="Arial"size="4">' + strReportTitle + '</FONT></TD></TR>'

strEmailText = strEmailText  + '<TR><TD>'
strEmailText = strEmailText  + '<TABLE cellspacing="1" cellpadding="1" width="auto" align="left" border="2"> '

if (strReportType =="1"):
    
    reqData = OslcUtils.bytesToJSONArray(StringUtil.toBytes(strReportBody))
    row_count=0
    
    for i in range(len(reqData)):
    
        obj=reqData[i]
        row_count =row_count + 1
        
        
        if (i==0):
                     
            obj["_data"]["col1_hdr"] ="" if ( not "col1_hdr" in obj["_data"])  else obj["_data"]["col1_hdr"] 
            obj["_data"]["col2_hdr"] ="" if ( not "col2_hdr" in obj["_data"])  else obj["_data"]["col2_hdr"]
            obj["_data"]["col3_hdr"] ="" if ( not "col3_hdr" in obj["_data"])  else obj["_data"]["col3_hdr"] 
            obj["_data"]["col4_hdr"] ="" if ( not "col4_hdr" in obj["_data"])  else obj["_data"]["col4_hdr"]
            obj["_data"]["col5_hdr"] ="" if ( not "col5_hdr" in obj["_data"])  else obj["_data"]["col5_hdr"] 
            obj["_data"]["col6_hdr"] ="" if ( not "col6_hdr" in obj["_data"])  else obj["_data"]["col6_hdr"]
            obj["_data"]["col7_hdr"] ="" if ( not "col7_hdr" in obj["_data"])  else obj["_data"]["col7_hdr"] 
            obj["_data"]["col8_hdr"] ="" if ( not "col8_hdr" in obj["_data"])  else obj["_data"]["col8_hdr"]
            obj["_data"]["col9_hdr"] ="" if ( not "col9_hdr" in obj["_data"])  else obj["_data"]["col9_hdr"] 
            obj["_data"]["col10_hdr"] ="" if ( not "col10_hdr" in obj["_data"])  else obj["_data"]["col10_hdr"]
            obj["_data"]["col11_hdr"] ="" if ( not "col11_hdr" in obj["_data"])  else obj["_data"]["col11_hdr"] 
            obj["_data"]["col12_hdr"] ="" if ( not "col12_hdr" in obj["_data"])  else obj["_data"]["col12_hdr"]
            obj["_data"]["col13_hdr"] ="" if ( not "col13_hdr" in obj["_data"])  else obj["_data"]["col13_hdr"] 
            obj["_data"]["col14_hdr"] ="" if ( not "col14_hdr" in obj["_data"])  else obj["_data"]["col14_hdr"]
            obj["_data"]["col15_hdr"] ="" if ( not "col15_hdr" in obj["_data"])  else obj["_data"]["col15_hdr"] 
            obj["_data"]["col16_hdr"] ="" if ( not "col16_hdr" in obj["_data"])  else obj["_data"]["col16_hdr"]
            obj["_data"]["col17_hdr"] ="" if ( not "col17_hdr" in obj["_data"])  else obj["_data"]["col17_hdr"] 
            obj["_data"]["col18_hdr"] ="" if ( not "col18_hdr" in obj["_data"])  else obj["_data"]["col18_hdr"]
            obj["_data"]["col19_hdr"] ="" if ( not "col19_hdr" in obj["_data"])  else obj["_data"]["col19_hdr"] 
            obj["_data"]["col20_hdr"] ="" if ( not "col20_hdr" in obj["_data"])  else obj["_data"]["col20_hdr"]
                     
            col1_hdr=obj["_data"]["col1_hdr"]                  
            col2_hdr=obj["_data"]["col2_hdr"]                  
            col3_hdr=obj["_data"]["col3_hdr"]                   
            col4_hdr=obj["_data"]["col4_hdr"]                  
            col5_hdr=obj["_data"]["col5_hdr"]
            col6_hdr=obj["_data"]["col6_hdr"]
            col7_hdr=obj["_data"]["col7_hdr"]                   
            col8_hdr=obj["_data"]["col8_hdr"]                   
            col9_hdr=obj["_data"]["col9_hdr"]                   
            col10_hdr=obj["_data"]["col10_hdr"]                    
            col11_hdr=obj["_data"]["col11_hdr"]                    
            col12_hdr=obj["_data"]["col12_hdr"]                    
            col13_hdr=obj["_data"]["col13_hdr"]                    
            col14_hdr=obj["_data"]["col14_hdr"]                
            col15_hdr=obj["_data"]["col15_hdr"]         
            col16_hdr=obj["_data"]["col16_hdr"]                
            col17_hdr=obj["_data"]["col17_hdr"]       
            col18_hdr=obj["_data"]["col18_hdr"]                
            col19_hdr=obj["_data"]["col19_hdr"]          
            col20_hdr=obj["_data"]["col20_hdr"]
             
         
            if (strReportType =="1"):
                 
                if (isBlank(col1_hdr)==False):
                    strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col1_hdr + '</FONT></TD>'
                if (isBlank(col2_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col2_hdr + '</FONT></TD>'
                if (isBlank(col3_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col3_hdr + '</FONT></TD>'
                if (isBlank(col4_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col4_hdr + '</FONT></TD>'
                if (isBlank(col5_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col5_hdr + '</FONT></TD>'
                if (isBlank(col6_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col6_hdr + '</FONT></TD>'
                if (isBlank(col7_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col7_hdr + '</FONT></TD>'
                if (isBlank(col8_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col8_hdr + '</FONT></TD>'
                if (isBlank(col9_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col9_hdr + '</FONT></TD>'
                if (isBlank(col10_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col10_hdr + '</FONT></TD>'
                if (isBlank(col11_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col11_hdr + '</FONT></TD>'
                if (isBlank(col12_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col12_hdr + '</FONT></TD>'
                if (isBlank(col13_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col13_hdr + '</FONT></TD>'
                if (isBlank(col14_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col14_hdr + '</FONT></TD>'
                if (isBlank(col15_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col15_hdr + '</FONT></TD>'
                if (isBlank(col16_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col16_hdr + '</FONT></TD>'
                if (isBlank(col17_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col17_hdr + '</FONT></TD>'
                if (isBlank(col18_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col18_hdr + '</FONT></TD>'
                if (isBlank(col19_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col19_hdr + '</FONT></TD>'
                if (isBlank(col20_hdr)==False):
                    strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col20_hdr + '</FONT></TD>'
                strEmailText = strEmailText  +'</TR>'
            
        obj["_data"]["col1_val"] ="" if ( not "col1_val" in obj["_data"])  else obj["_data"]["col1_val"] 
        obj["_data"]["col2_val"] ="" if ( not "col2_val" in obj["_data"])  else obj["_data"]["col2_val"]
        obj["_data"]["col3_val"] ="" if ( not "col3_val" in obj["_data"])  else obj["_data"]["col3_val"] 
        obj["_data"]["col4_val"] ="" if ( not "col4_val" in obj["_data"])  else obj["_data"]["col4_val"]
        obj["_data"]["col5_val"] ="" if ( not "col5_val" in obj["_data"])  else obj["_data"]["col5_val"] 
        obj["_data"]["col6_val"] ="" if ( not "col6_val" in obj["_data"])  else obj["_data"]["col6_val"]
        obj["_data"]["col7_val"] ="" if ( not "col7_val" in obj["_data"])  else obj["_data"]["col7_val"] 
        obj["_data"]["col8_val"] ="" if ( not "col8_val" in obj["_data"])  else obj["_data"]["col8_val"]
        obj["_data"]["col9_val"] ="" if ( not "col9_val" in obj["_data"])  else obj["_data"]["col9_val"] 
        obj["_data"]["col10_val"] ="" if ( not "col10_val" in obj["_data"])  else obj["_data"]["col10_val"]
        obj["_data"]["col11_val"] ="" if ( not "col11_val" in obj["_data"])  else obj["_data"]["col11_val"] 
        obj["_data"]["col12_val"] ="" if ( not "col12_val" in obj["_data"])  else obj["_data"]["col12_val"]
        obj["_data"]["col13_val"] ="" if ( not "col13_val" in obj["_data"])  else obj["_data"]["col13_val"] 
        obj["_data"]["col14_val"] ="" if ( not "col14_val" in obj["_data"])  else obj["_data"]["col14_val"]
        obj["_data"]["col15_val"] ="" if ( not "col15_val" in obj["_data"])  else obj["_data"]["col15_val"] 
        obj["_data"]["col16_val"] ="" if ( not "col16_val" in obj["_data"])  else obj["_data"]["col16_val"]
        obj["_data"]["col17_val"] ="" if ( not "col17_val" in obj["_data"])  else obj["_data"]["col17_val"] 
        obj["_data"]["col18_val"] ="" if ( not "col18_val" in obj["_data"])  else obj["_data"]["col18_val"]
        obj["_data"]["col19_val"] ="" if ( not "col19_val" in obj["_data"])  else obj["_data"]["col19_val"] 
        obj["_data"]["col20_val"] ="" if ( not "col20_val" in obj["_data"])  else obj["_data"]["col20_val"]
            
                     
        col1_val=obj["_data"]["col1_val"]
        col2_val=obj["_data"]["col2_val"]
        col3_val=obj["_data"]["col3_val"]
        col4_val=obj["_data"]["col4_val"]
        col5_val=obj["_data"]["col5_val"]
        col6_val=obj["_data"]["col6_val"]
        col7_val=obj["_data"]["col7_val"]
        col8_val=obj["_data"]["col8_val"]
        col9_val=obj["_data"]["col9_val"]
        col10_val=obj["_data"]["col10_val"]
        col11_val=obj["_data"]["col11_val"]
        col12_val=obj["_data"]["col12_val"]
        col13_val=obj["_data"]["col13_val"]
        col14_val=obj["_data"]["col14_val"]
        col15_val=obj["_data"]["col15_val"]
        col16_val=obj["_data"]["col16_val"]
        col17_val=obj["_data"]["col17_val"]
        col18_val=obj["_data"]["col18_val"]
        col19_val=obj["_data"]["col19_val"]
        col20_val=obj["_data"]["col20_val"]    
        
                                   
        if (isBlank(col1_val)==False):
            strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col1_val + '</FONT></TD>'
        if (isBlank(col2_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col2_val + '</FONT></TD>'
        if (isBlank(col3_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col3_val + '</FONT></TD>'
        if (isBlank(col4_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col4_val + '</FONT></TD>'
        if (isBlank(col5_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col5_val + '</FONT></TD>'
        if (isBlank(col6_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col6_val + '</FONT></TD>'
        if (isBlank(col7_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col7_val + '</FONT></TD>'
        if (isBlank(col8_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col8_val + '</FONT></TD>'
        if (isBlank(col9_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col9_val + '</FONT></TD>'
        if (isBlank(col10_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col10_val + '</FONT></TD>'
        if (isBlank(col11_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col11_val + '</FONT></TD>'
        if (isBlank(col12_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col12_val + '</FONT></TD>'
        if (isBlank(col13_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col13_val + '</FONT></TD>'
        if (isBlank(col14_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col14_val + '</FONT></TD>'
        if (isBlank(col15_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col15_val + '</FONT></TD>'
        if (isBlank(col16_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col16_val + '</FONT></TD>'
        if (isBlank(col17_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col17_val + '</FONT></TD>'
        if (isBlank(col18_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col18_val + '</FONT></TD>'
        if (isBlank(col19_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col19_val + '</FONT></TD>'
        if (isBlank(col20_val)==False):
            strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col20_val + '</FONT></TD>'
               
        strEmailText = strEmailText  +'</TR>'

    
if (strReportType =="2"):   # Two-columns report 
    
    obj=OslcUtils.bytesToJSONObject(StringUtil.toBytes(strReportBody))
    row_count=1
         
         
    obj["_data"]["col1_hdr"] ="" if ( not "col1_hdr" in obj["_data"])  else obj["_data"]["col1_hdr"] 
    obj["_data"]["col2_hdr"] ="" if ( not "col2_hdr" in obj["_data"])  else obj["_data"]["col2_hdr"]
    obj["_data"]["col3_hdr"] ="" if ( not "col3_hdr" in obj["_data"])  else obj["_data"]["col3_hdr"] 
    obj["_data"]["col4_hdr"] ="" if ( not "col4_hdr" in obj["_data"])  else obj["_data"]["col4_hdr"]
    obj["_data"]["col5_hdr"] ="" if ( not "col5_hdr" in obj["_data"])  else obj["_data"]["col5_hdr"] 
    obj["_data"]["col6_hdr"] ="" if ( not "col6_hdr" in obj["_data"])  else obj["_data"]["col6_hdr"]
    obj["_data"]["col7_hdr"] ="" if ( not "col7_hdr" in obj["_data"])  else obj["_data"]["col7_hdr"] 
    obj["_data"]["col8_hdr"] ="" if ( not "col8_hdr" in obj["_data"])  else obj["_data"]["col8_hdr"]
    obj["_data"]["col9_hdr"] ="" if ( not "col9_hdr" in obj["_data"])  else obj["_data"]["col9_hdr"] 
    obj["_data"]["col10_hdr"] ="" if ( not "col10_hdr" in obj["_data"])  else obj["_data"]["col10_hdr"]
    obj["_data"]["col11_hdr"] ="" if ( not "col11_hdr" in obj["_data"])  else obj["_data"]["col11_hdr"] 
    obj["_data"]["col12_hdr"] ="" if ( not "col12_hdr" in obj["_data"])  else obj["_data"]["col12_hdr"]
    obj["_data"]["col13_hdr"] ="" if ( not "col13_hdr" in obj["_data"])  else obj["_data"]["col13_hdr"] 
    obj["_data"]["col14_hdr"] ="" if ( not "col14_hdr" in obj["_data"])  else obj["_data"]["col14_hdr"]
    obj["_data"]["col15_hdr"] ="" if ( not "col15_hdr" in obj["_data"])  else obj["_data"]["col15_hdr"] 
    obj["_data"]["col16_hdr"] ="" if ( not "col16_hdr" in obj["_data"])  else obj["_data"]["col16_hdr"]
    obj["_data"]["col17_hdr"] ="" if ( not "col17_hdr" in obj["_data"])  else obj["_data"]["col17_hdr"] 
    obj["_data"]["col18_hdr"] ="" if ( not "col18_hdr" in obj["_data"])  else obj["_data"]["col18_hdr"]
    obj["_data"]["col19_hdr"] ="" if ( not "col19_hdr" in obj["_data"])  else obj["_data"]["col19_hdr"] 
    obj["_data"]["col20_hdr"] ="" if ( not "col20_hdr" in obj["_data"])  else obj["_data"]["col20_hdr"]
    
    obj["_data"]["col1_val"] ="" if ( not "col1_val" in obj["_data"])  else obj["_data"]["col1_val"] 
    obj["_data"]["col2_val"] ="" if ( not "col2_val" in obj["_data"])  else obj["_data"]["col2_val"]
    obj["_data"]["col3_val"] ="" if ( not "col3_val" in obj["_data"])  else obj["_data"]["col3_val"] 
    obj["_data"]["col4_val"] ="" if ( not "col4_val" in obj["_data"])  else obj["_data"]["col4_val"]
    obj["_data"]["col5_val"] ="" if ( not "col5_val" in obj["_data"])  else obj["_data"]["col5_val"] 
    obj["_data"]["col6_val"] ="" if ( not "col6_val" in obj["_data"])  else obj["_data"]["col6_val"]
    obj["_data"]["col7_val"] ="" if ( not "col7_val" in obj["_data"])  else obj["_data"]["col7_val"] 
    obj["_data"]["col8_val"] ="" if ( not "col8_val" in obj["_data"])  else obj["_data"]["col8_val"]
    obj["_data"]["col9_val"] ="" if ( not "col9_val" in obj["_data"])  else obj["_data"]["col9_val"] 
    obj["_data"]["col10_val"] ="" if ( not "col10_val" in obj["_data"])  else obj["_data"]["col10_val"]
    obj["_data"]["col11_val"] ="" if ( not "col11_val" in obj["_data"])  else obj["_data"]["col11_val"] 
    obj["_data"]["col12_val"] ="" if ( not "col12_val" in obj["_data"])  else obj["_data"]["col12_val"]
    obj["_data"]["col13_val"] ="" if ( not "col13_val" in obj["_data"])  else obj["_data"]["col13_val"] 
    obj["_data"]["col14_val"] ="" if ( not "col14_val" in obj["_data"])  else obj["_data"]["col14_val"]
    obj["_data"]["col15_val"] ="" if ( not "col15_val" in obj["_data"])  else obj["_data"]["col15_val"] 
    obj["_data"]["col16_val"] ="" if ( not "col16_val" in obj["_data"])  else obj["_data"]["col16_val"]
    obj["_data"]["col17_val"] ="" if ( not "col17_val" in obj["_data"])  else obj["_data"]["col17_val"] 
    obj["_data"]["col18_val"] ="" if ( not "col18_val" in obj["_data"])  else obj["_data"]["col18_val"]
    obj["_data"]["col19_val"] ="" if ( not "col19_val" in obj["_data"])  else obj["_data"]["col19_val"] 
    obj["_data"]["col20_val"] ="" if ( not "col20_val" in obj["_data"])  else obj["_data"]["col20_val"]
    
    
    
    col1_hdr=obj["_data"]["col1_hdr"]                  
    col2_hdr=obj["_data"]["col2_hdr"]                  
    col3_hdr=obj["_data"]["col3_hdr"]                   
    col4_hdr=obj["_data"]["col4_hdr"]                  
    col5_hdr=obj["_data"]["col5_hdr"]
    col6_hdr=obj["_data"]["col6_hdr"]
    col7_hdr=obj["_data"]["col7_hdr"] 
    col8_hdr=obj["_data"]["col8_hdr"] 
    
    col9_hdr=obj["_data"]["col9_hdr"]                   
    col10_hdr=obj["_data"]["col10_hdr"]                    
    col11_hdr=obj["_data"]["col11_hdr"]                    
    col12_hdr=obj["_data"]["col12_hdr"]                    
    col13_hdr=obj["_data"]["col13_hdr"]                    
    col14_hdr=obj["_data"]["col14_hdr"]                
    col15_hdr=obj["_data"]["col15_hdr"]         
    col16_hdr=obj["_data"]["col16_hdr"]                
    col17_hdr=obj["_data"]["col17_hdr"]       
    col18_hdr=obj["_data"]["col18_hdr"]                
    col19_hdr=obj["_data"]["col19_hdr"]          
    col20_hdr=obj["_data"]["col20_hdr"]
    
    col1_val=obj["_data"]["col1_val"]
    col2_val=obj["_data"]["col2_val"]
    col3_val=obj["_data"]["col3_val"]
    col4_val=obj["_data"]["col4_val"]
    col5_val=obj["_data"]["col5_val"]
    col6_val=obj["_data"]["col6_val"]
    col7_val=obj["_data"]["col7_val"]
    col8_val=obj["_data"]["col8_val"]
    col9_val=obj["_data"]["col9_val"]
    col10_val=obj["_data"]["col10_val"]
    col11_val=obj["_data"]["col11_val"]
    col12_val=obj["_data"]["col12_val"]
    col13_val=obj["_data"]["col13_val"]
    col14_val=obj["_data"]["col14_val"]
    col15_val=obj["_data"]["col15_val"]
    col16_val=obj["_data"]["col16_val"]
    col17_val=obj["_data"]["col17_val"]
    col18_val=obj["_data"]["col18_val"]
    col19_val=obj["_data"]["col19_val"]
    col20_val=obj["_data"]["col20_val"]   
    
    if (isBlank(col1_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col1_hdr + '</FONT></TD>'
    if (isBlank(col1_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col1_val + '</FONT></TD></TR>'
    if (isBlank(col2_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col2_hdr + '</FONT></TD>'
    if (isBlank(col2_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col2_val + '</FONT></TD></TR>'
    if (isBlank(col3_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col3_hdr + '</FONT></TD>'
    if (isBlank(col3_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col3_val + '</FONT></TD></TR>'
    if (isBlank(col4_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col4_hdr + '</FONT></TD>'
    if (isBlank(col4_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col4_val + '</FONT></TD></TR>'
    if (isBlank(col5_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col5_hdr + '</FONT></TD>'
    if (isBlank(col5_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col5_val + '</FONT></TD></TR>'
    if (isBlank(col6_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col6_hdr + '</FONT></TD>'
    if (isBlank(col6_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col6_val + '</FONT></TD></TR>'
    if (isBlank(col7_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col7_hdr + '</FONT></TD>'
    if (isBlank(col7_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col7_val + '</FONT></TD></TR>'
    if (isBlank(col8_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col8_hdr + '</FONT></TD>'
    if (isBlank(col8_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col8_val + '</FONT></TD></TR>'
    if (isBlank(col9_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col9_hdr + '</FONT></TD>'
    if (isBlank(col9_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col9_val + '</FONT></TD></TR>'
    if (isBlank(col10_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col10_hdr + '</FONT></TD>'
    if (isBlank(col10_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col10_val + '</FONT></TD></TR>'
    if (isBlank(col11_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col11_hdr + '</FONT></TD>'
    if (isBlank(col11_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col11_val + '</FONT></TD></TR>'
    if (isBlank(col12_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col12_hdr + '</FONT></TD>'
    if (isBlank(col12_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col12_val + '</FONT></TD></TR>'
    if (isBlank(col13_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col13_hdr + '</FONT></TD>'
    if (isBlank(col13_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col13_val + '</FONT></TD></TR>'
    if (isBlank(col14_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col14_hdr + '</FONT></TD>'
    if (isBlank(col14_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col14_val + '</FONT></TD></TR>'
    if (isBlank(col15_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col15_hdr + '</FONT></TD>'
    if (isBlank(col15_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col15_val + '</FONT></TD></TR>'
    if (isBlank(col16_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col16_hdr + '</FONT></TD>'
    if (isBlank(col16_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col16_val + '</FONT></TD></TR>'
    if (isBlank(col17_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col17_hdr + '</FONT></TD>'
    if (isBlank(col17_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col17_val + '</FONT></TD></TR>'
    if (isBlank(col18_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col18_hdr + '</FONT></TD>'
    if (isBlank(col18_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col18_val + '</FONT></TD></TR>'
    if (isBlank(col19_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col19_hdr + '</FONT></TD>'
    if (isBlank(col19_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col19_val + '</FONT></TD></TR>'
    if (isBlank(col20_hdr)==False):
        strEmailText = strEmailText  + ' <TR> <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col20_hdr + '</FONT></TD>'
    if (isBlank(col20_val)==False):
        strEmailText = strEmailText  + ' <TD VALIGN="TOP"><FONT face="Arial"size="4">' + col20_val + '</FONT></TD></TR>'        


    
if (row_count > 0):

    strEmailText = strEmailText + '</TABLE> </TD></TR>'
    strEmailText = strEmailText +'<TR><TD>&nbsp;</TD></TR><TR><TD>&nbsp;</TD></TR>'
    
                   
    if (strReportFooter.upper() != "BLANK") :
        strEmailText = strEmailText  + '<TR><TD align="center" VALIGN="TOP"><FONT face="Arial"size="4">' + strReportFooter + '</FONT></TD></TR>'
        
    
    LblMaxvarsSet= MXServer.getMXServer().getMboSet("lbl_maxvars", mbo.getUserInfo())
    strWhere = " varname in " + "('APPLICATION_ENV','MAX_TESTUSERSEMAIL')"     
    LblMaxvarsSet.reset() # clears the contents of collection - mset refers to locations
    LblMaxvarsSet.setWhere(strWhere) # popu
    strApplicationEnv=""
    strTestEmailTo=""
    if (not LblMaxvarsSet.isEmpty()):
        intCount=LblMaxvarsSet.count()
        for i in xrange(intCount):
            if (LblMaxvarsSet.getMbo(i).getString("varname") == "APPLICATION_ENV"):
                strApplicationEnv=LblMaxvarsSet.getMbo(i).getString("varvalue")
            if (LblMaxvarsSet.getMbo(i).getString("varname") == "MAX_TESTUSERSEMAIL"):
                strTestEmailTo=LblMaxvarsSet.getMbo(i).getString("varvalue")
    LblMaxvarsSet=None
    
    if (strApplicationEnv !="PRODUCTION"):
        strEmailText = strEmailText  + '<TR><TD align="center" VALIGN="TOP"><FONT face="Arial"size="4"><STRONG><U>' + strDisclaimer +  '</U></STRONG></FONT></TD></TR>'
        strEmailSubject = '[TEST] ' +  strEmailSubject
        strEmailTo=strTestEmailTo
    
    strEmailText = strEmailText +  ' </TABLE>'
    strEmailText = strEmailText   + '</BODY></HTML> '
    
       
       
    LblWOSet = MXServer.getMXServer().getMboSet("workorder", mbo.getUserInfo())
    strWhere = " rownum=1 "     
    LblWOSet.reset() # clears the contents of collection - mset refers to locations
    LblWOSet.setWhere(strWhere) # popu
    wombo=LblWOSet.getMbo(0)
    strMailhost=getPropertyvalue("mail.smtp.host")
    wombo.LblSendMail(strMailhost,strEmailFrom , strEmailTo, "", strEmailSubject,  "HTML", strEmailText)
    LblWOSet=None