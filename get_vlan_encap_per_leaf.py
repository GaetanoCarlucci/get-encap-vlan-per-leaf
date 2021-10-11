#!/usr/bin/env python
#
#   Author: Gaetano Carlucci, Cisco CX
#   Python Version: 3
#
#   This software is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied

import json
from Utils.Session import Session
from Utils import excel_lib
import re

# parsed the column in order to get a more user friendly output 
def parse_column(column_for_excel_raw, node_names):
    output = []
    column = ['VLAN','node_id', 'host_name', 'tenant_name','ap_name','epg_name']
    for row in column_for_excel_raw:
        new_row = {}
        ap_name = ''
        for k, v in row.items():
            if k == 'epgDn':
                if re.search('/epg-(.*)', v):
                    epg_name = (re.search('/epg-(.*)', v)).group(1)
                    new_row['epg_name'] = epg_name
                if re.search('/tn-(.*?)/', v):
                    tenant_name = (re.search('/tn-(.*?)/', v)).group(1)
                    new_row['tenant_name'] = tenant_name
                if re.search('/ap-(.*?)/', v):
                    ap_name = (re.search('/ap-(.*?)/', v)).group(1)
                    new_row['ap_name'] = ap_name
            if k == 'dn':
                 if re.search('/node-(.*?)/', v):
                    node_id = (re.search('/node-(.*?)/', v)).group(1)
                    new_row['node_id'] = node_id
                    new_row['host_name'] = node_names[node_id]
            if k == 'encap':
                new_row['VLAN'] = v
        if ap_name == '' :
            new_row['ap_name'] = row['epgDn']
            new_row['epg_name'] = row['epgDn']
        output.append(new_row)
    return [output,column]

#Return a list of dict with correspond to each row of the excel sheet not parsed
def get_vlan_encap(my_fabric, api_name, column):
    output = []
    data_json = json.loads(my_fabric.apic_json_get(api_name))
    for vlan in data_json['imdata']:
        for k, v in vlan.items():
            row = {}
            for j, attribute in v.items():
                for i in column:
                   row[i] = attribute[i]
                output.append(row)
    return output

# Returns a dict with Node id as key and host name as value
def get_node_name(my_fabric, api_name):
    output = {}
    data_json = json.loads(my_fabric.apic_json_get(api_name))
    for fabric_node in data_json['imdata']:
        for k, v in fabric_node['fabricNode'].items():
            for j, attribute in v.items():
                if j == 'dn':
                    if re.search('/node-(.*)', attribute):
                        node_id = (re.search('/node-(.*)', attribute)).group(1)
                if j == 'name':
                    name = attribute
            output[node_id] = name
    return output

# Returns a dict with Node id as key and host name as value
def get_interfaces(my_fabric, api_name):
    output = {}
    data_json = json.loads(my_fabric.apic_json_get(api_name))
    for interfaces in data_json['imdata']:
        print(interfaces)
    return output
 
def main():
    with open('Utils/credentials.json') as json_file:
        data = json.load(json_file)
    my_fabric = Session(data['apic_ip_address'], data["apic_port"],
                        data['apic_admin_user'], data['apic_admin_password'])
    cookie = my_fabric.get_cookie()
    my_fabric.set_cookie(cookie)

    excel = excel_lib.Excel('./', "Vlan_Encap6")
    
    column_raw = ["encap", "epgDn", "dn"]
    column_for_excel_raw = get_vlan_encap(my_fabric, 'vlanCktEp', column_raw)
    node_names = get_node_name(my_fabric, 'fabricNode')
    interfaces = get_interfaces(my_fabric, 'fvIfConn') 

    column_for_excel = parse_column(column_for_excel_raw, node_names)

    excel.create_sheet("Vlan_Encap", column_for_excel[1])
    excel.fill_sheet(column_for_excel[0], "Vlan_Encap")

    print("Vlan_Encap.xlsx successfully created")

if __name__ == "__main__":
    main()