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

def filter_epg_with_contract(my_fabric, class_name):
    epg_output = []
    egp_json = json.loads(my_fabric.apic_json_get(class_name))
    for contract in egp_json['imdata']:
        for k, v in contract[class_name].items():
            if re.search('/brc-(.*?)/[dia]', v['dn']):
                contract_name = (re.search('/brc-(.*?)/[dia]', v['dn'])).group(1)
                epg_output.append((v['epgDn'], contract_name))
    return epg_output

def extract_data(epg_list, role):
    tenant = ""
    epg = ""
    app = ""
    output = []
    for i in epg_list:
        epg_dn = i[0]
        contract_name = i[1]
        if re.search('tn-(.*)/ap-', epg_dn):
            tenant = (re.search('tn-(.*)/ap-', epg_dn)).group(1)
            app = (re.search('ap-(.*)/epg-', epg_dn)).group(1)
            epg = (re.search('/epg-(.*)', epg_dn)).group(1)
        if re.search('tn-(.*)/ctx-', epg_dn):
            tenant = (re.search('tn-(.*)/ctx-', epg_dn)).group(1)
            app = 'vZany'
            epg = "any " + (re.search('ctx-(.*)/', epg_dn)).group(1)
        if re.search('tn-(.*)/mg', epg_dn):
            tenant = (re.search('tn-(.*)/mg', epg_dn)).group(1)
            app = (re.search('mgmtp-(.*)/', epg_dn)).group(1)
            epg = (re.search('/inb-(.*)', epg_dn)).group(1)
        if re.search('tn-(.*)/out-', epg_dn):
            tenant = (re.search('tn-(.*)/out', epg_dn)).group(1)
            app = (re.search('/out-(.*)/instP-', epg_dn)).group(1)
            epg = (re.search('/instP-(.*)', epg_dn)).group(1)

        output.append({"Contract_name": contract_name, "Tenant": tenant,
                       "APP Profile": app, "EPG": epg, "Role": role})
    return output

def get_contract_relationship(my_fabric):
    provider_epg_list = filter_epg_with_contract(my_fabric, 'vzProvDef')
    consumer_epg_list = filter_epg_with_contract(my_fabric, 'vzConsDef')
    output = extract_data(provider_epg_list, "Provider")
    output = output + extract_data(consumer_epg_list, "Consumer")
    return output

def main():
    with open('Utils/credentials.json') as json_file:
        data = json.load(json_file)
    my_fabric = Session(data['apic_ip_address'], data["apic_port"],
                        data['apic_admin_user'], data['apic_admin_password'])
    cookie = my_fabric.get_cookie()
    my_fabric.set_cookie(cookie)
    excel = excel_lib.Excel('./', "Contract_Relationship")
    excel.create_sheet("Contract_Relationship", ["Contract_name", "Tenant",
                                                 "APP Profile", "EPG", "Role"])
    data = get_contract_relationship(my_fabric)
    excel.fill_sheet(data, "Contract_Relationship")
    print("Contracts_Relationships.xlsx successfully created")

if __name__ == "__main__":
    main()
