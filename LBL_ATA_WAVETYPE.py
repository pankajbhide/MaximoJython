##################################################### 
# Purpose: Script to mark field read-only.
#
# Author : Pankaj Bhide
#
# Date    : Apr 28, 2016
#
# Revision
# History : 
#
######################################################

from psdi.server import MXServer

if (ondelete == False):
    
    
    if (mbo.getString("wavetype")=='CW'):
        jIOPulse_rep_rate_readonly=True
        jIOPulse_rep_rate_uom_readonly=True
        jIOPulse_width_readonly=True
        jIOPulse_width_uom_readonly=True
        jIOPulse_energy_readonly=True
        jIOPulse_energy_UOM_readonly=True
    else:
        jIOPulse_rep_rate_readonly=False
        jIOPulse_rep_rate_uom_readonly=False
        jIOPulse_width_readonly=False
        jIOPulse_width_uom_readonly=False
        jIOPulse_energy_readonly=False
        jIOPulse_energy_UOM_readonly=False
     