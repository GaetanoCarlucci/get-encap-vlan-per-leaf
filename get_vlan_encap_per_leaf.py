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

def get_vlan_encap(my_fabric, api_name, column):
    output = {}
    for i in column:
        print(i)
        output[i] = []
    data_json = json.loads(my_fabric.apic_json_get(api_name))
    for vlan in data_json['imdata']:
        for k, v in vlan.items():
            for j, attribute in v.items():
                for i in column:
                   output[i].append(attribute[i])
                   #print(attribute[i])
    return output
 

def main():
    with open('Utils/credentials.json') as json_file:
        data = json.load(json_file)
    my_fabric = Session(data['apic_ip_address'], data["apic_port"],
                        data['apic_admin_user'], data['apic_admin_password'])
    cookie = my_fabric.get_cookie()
    my_fabric.set_cookie(cookie)

    dashboard = []
    excel = excel_lib.Excel('./', "Vlan_Encap")
    column = ["encap", "epgDn", "dn", "name"]
    excel.create_sheet("Vlan_Encap", column)

    vlan_column_for_excel = get_vlan_encap(my_fabric, 'vlanCktEp', column)

    print(vlan_column_for_excel['encap'])
    excel.fill_sheet(vlan_column_for_excel, "Vlan_Encap")
    print("Vlan_Encap.xlsx successfully created")

if __name__ == "__main__":
    main()
