#!/usr/bin/env python
#
#   Author: Gaetano Carlucci, Cisco CX
#   Python Version: 3
#
#   This software is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied

import json
from Utils.Session import Session
import re
import csv

# Returns a dict with all EPG deployed in the fabric
def get_all_endpoint(my_fabric, api_name):
    output = []
    data_json = json.loads(my_fabric.apic_json_get(api_name))
    for end_point_in_fabric in data_json['imdata']:
        for k, v in end_point_in_fabric['fvIp'].items():
            for j, attribute in v.items():
                if j == 'dn':
                    if re.search('/tn-(.*?)/ap-(.*?)/epg-(.*)', attribute):
                        tenant_name = (re.search('/tn-(.*?)/ap-(.*?)/epg-(.*)', attribute)).group(1)
                        app_name = (re.search('/tn-(.*?)/ap-(.*?)/epg-(.*)', attribute)).group(2)
                        epg_name = (re.search('/tn-(.*?)/ap-(.*?)/epg-(.*)', attribute)).group(3)
                        epg_dn = attribute
                        output.append([tenant_name, app_name, epg_name, epg_dn])
    return output

def main():
    with open('Utils/credentials.json') as json_file:
        data = json.load(json_file)

    my_fabric = Session(data['apic_ip_address'], data["apic_port"],
                        data['apic_admin_user'], data['apic_admin_password'])

    cookie = my_fabric.get_cookie()
    my_fabric.set_cookie(cookie)

    end_point_list = get_all_endpoint(my_fabric, 'fvIp')

    #take the first epg from the firt end point from the list ang get dn
    pattern = r'/cep-[^/]*|/ip-\[.*?\]'
    epg_dn = re.sub(pattern, '', end_point_list[0][-1])
    payload = {
        "fvAEPg": {
            "attributes": {
                "dn": epg_dn,
                "shutdown": "true"
            },
            "children": []
        }
    }

    my_fabric.apic_json_post(epg_dn, payload)

    # Open a file for writing
    with open('endpoints.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # Write each row of data to the CSV file
        for row in end_point_list:
            writer.writerow(row)

    print("Data has been written to 'endpoints.csv'.")


if __name__ == "__main__":
    main()
