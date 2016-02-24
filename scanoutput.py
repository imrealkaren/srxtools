# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:05:35 2016

@author: xf05id1
"""
from databroker import DataBroker as db, get_table, get_images, get_events
import time

def textout(scan=-1, header=[], userheader={}, column=[], usercolumn = {}, usercolumnname = [], output = True, filename_add = ''):
    '''
    scan: can be scan_id (integer) or uid (string). defaul = -1 (last scan run)
          default = -1
    header: a list of items that exist in the event data to be put into the header
    userheader: a dictionary defined by user to put into the hdeader
    column: a list of items that exist in the event data to be put into the column data
    output: print all header fileds. if output = False, only print the ones that were able to be written
            default = True
    
    '''   
    scanh= db[scan]
    print(scanh.start)
    events=list(get_events(scanh))

 
   #convert time stamp to localtime
    #timestamp=scanhh.start['time']
    #scantime=time.localtime(timestamp)   
    
    filedir='/nfs/xf05id1/userdata/2016cycle2/300265_inhouse/'
    
    if filename_add is not '':    
        filename='scan_'+ str(scanh.start['scan_id'])+'_'+filename_add
    else:
        filename='scan_'+ str(scanh.start['scan_id']) 


    f = open(filedir+filename, 'w')

    staticheader = '# XDI/1.0 MX/2.0\n' \
              +'# Beamline.name: '+scanh.start.beamline_id+'\n'  \
              +'# Facility.name: NSLS-II\n'  \
              +'# Facility.ring_current:' + str(events[0]['data']['ring_current'])+'\n' \
              +'# Scan.start.uid: '+scanh.start.uid+'\n'  \
              +'# Scan.start.time: '+str(scanh.start.time)+'\n'  \
              +'# Scan.start.ctime: '+time.ctime(scanh.start.time)+'\n'  \
              +'# Mono.name: Si 111\n'  \
              #+'# bpm.cam.exposure_time: '+str(events[0].descriptor.configuration['bpmAD']['data']['bpmAD_cam_acquire_time'])+'\n'  \
              #+'# Undulator.elevation: '+str(scanh.start.undulator_setup['elevation'])+'\n'  \
              #+'# Undulator.tilt: '+str(scanh.start.undulator_setup['tilt'])+'\n'  \
              #+'# Undulator.taper: '+str(scanh.start.undulator_setup['taper'])+'\n'              

    f.write(staticheader)

    for item in header:
        if item in events[0].data.keys():
            f.write('# '+item+': '+str(events[0]['data'][item])+'\n')
            if output is True:
                print(item+' is written')
        else: 
            print(item+' is not in the scan')
           
    for key in userheader:
        f.write('# '+key+': '+str(userheader[key])+'\n')
        if output is True:
            print(key+' is written')                   

    for idx, item in enumerate(column): 
        if item in events[0].data.keys():        
            f.write('# Column.'+str(idx+1)+': '+item+'\n')


    f.write('# ') 
    for item in column: 
        if item in events[0].data.keys():        
            f.write(str(item)+'\t')

    for item in usercolumnname: 
        f.write(item+'\t')
            
    f.write('\n')
    
    idx = 0
    for event in events:
        for item in column: 
            if item in events[0].data.keys():        
                f.write(str(event['data'][item])+'\t')
        for item in usercolumnname:
            f.write(str(usercolumn[item][idx])+'\t')

        idx = idx + 1
        f.write('\n')
        
    f.close()