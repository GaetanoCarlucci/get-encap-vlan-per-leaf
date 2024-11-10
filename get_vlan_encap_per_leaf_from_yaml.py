#!/usr/bin/env python
#
#   Author: Gaetano Carlucci, Cisco CX
#   Python Version: 3
#
#   This software is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied

import os
import yaml
from Utils import excel_lib

#extract from data model: tenant, vrf, bd, subnet
def extract_bd_data_from_yaml_files(directory):
    list_of_dicts = []

    # Iterate through all files in the directory that start with "tenant"
    for filename in os.listdir(directory):
        if filename.startswith('tenant') and filename.endswith('.yaml'):
            file_path = os.path.join(directory, filename)
            
            # Load YAML data from file
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            
            # Extract values from application profiles and populate dictionaries
            for tenant in data['apic']['tenants']:
                tenant_name = tenant['name']
                if 'bridge_domains' not in tenant:
                    continue
                for bd in tenant['bridge_domains']:
                    bd_name = bd['name']
                    if 'vrf' not in bd:
                        vrf_name = None
                    else:
                       vrf_name = bd['vrf']
                    if 'subnets' not in bd:
                        subnets = ''
                    else:
                        subnets = ''
                        for subnet in bd['subnets']:
                           subnets = subnets + ' ' + subnet['ip']

                    # Create dictionary with extracted values
                    dict_entry = {
                        'tenant_name': tenant_name,
                        'bd_name': bd_name,
                        'vrf': vrf_name,
                        'subnet_ip': subnets
                    }
                    
                    # Add dictionary to list
                    list_of_dicts.append(dict_entry)
    return list_of_dicts


def extract_node_data_from_yaml_files(directory):
    list_of_dicts = []

      # Iterate through all files in the directory that start with "tenant"
    for filename in os.listdir(directory):
        if filename.startswith('node_') and filename.endswith('.yaml'):
            file_path = os.path.join(directory, filename)
            
            # Load YAML data from file
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            

            if 'node_policies' in data['apic']:
                node_policies = data['apic']['node_policies']
                
                for node in node_policies.get('nodes', []):
                    node_id = node.get('id', None)
                    name = node.get('name', None)
                    oob_address = node.get('oob_address', None)
                    
                    # Create dictionary with extracted values
                    dict_entry = {
                        'node_id': node_id,
                        'name': name,
                        'oob_address': oob_address
                    }
                    
                    # Add dictionary to list
                    list_of_dicts.append(dict_entry)
            
    return list_of_dicts


#extract from data model: tenant, vlan, application_profilem, epg_name, node_id and combines it with other list provided as input
def extract_epg_data_from_yaml_files(directory, node_list, bd_list):
    list_of_dicts = []

    # Iterate through all files in the directory that start with "tenant"
    for filename in os.listdir(directory):
        if filename.startswith('tenant') and filename.endswith('.yaml'):
            file_path = os.path.join(directory, filename)
            
            # Load YAML data from file
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            
            # Extract values from application profiles and populate dictionaries
            for tenant in data['apic']['tenants']:
                tenant_name = tenant['name']
                if 'application_profiles' not in tenant:
                    continue
                for ap in tenant['application_profiles']:
                    ap_name = ap['name']
                    if 'endpoint_groups' not in ap:
                        continue
                    for epg in ap['endpoint_groups']:
                        epg_name = epg['name']
                        bd_name = epg.get('bridge_domain', None)
                        if 'physical_domains' not in epg: 
                            continue 
                        phy_domains = ''
                        for domain in epg['physical_domains']:
                            phy_domains = phy_domains + ' ' + domain
                        if 'static_ports' not in epg:
                            continue
                        for port in epg['static_ports']:
                            vlan = port.get('vlan', None)
                            #if a vpc port can be attached to 2 nodes
                            node_ids = [port.get('node_id', None), port.get('node2_id', None)]
                            oob_addr = None  
                            host_name = None 
                            subnet_ip = None
                            vrf_name = None
                            p = port.get('port', None)

                            if 'channel' in port:
                                p = port['channel']
                            else:
                                if 'port' in port:
                                    p = port['port']
                                else:
                                    p = ''

                            for node_id in node_ids:
                                if not node_id:
                                    continue
                                for node in node_list:
                                    if node_id == node["node_id"]:
                                        oob_addr = node['oob_address']
                                        host_name = node['name']
                            
                                for bd in bd_list:
                                    if tenant_name == bd['tenant_name'] and bd_name == bd['bd_name']:
                                        vrf_name = bd['vrf']
                                        subnet_ip = bd['subnet_ip']

                                # Create dictionary with extracted values
                                dict_entry = {
                                    'VLAN': vlan,
                                    'node_id': node_id,
                                    'oob_addr': oob_addr,
                                    'host_name': host_name,
                                    'tenant_name': tenant_name,
                                    'ap_name': ap_name,
                                    'epg_name': epg_name,
                                    'bd_name': bd_name,
                                    'vrf': vrf_name,
                                    'subnet_ip': subnet_ip,
                                    'port': p,
                                    'domain': phy_domains
                                }
                                    
                                    # Add dictionary to list
                                list_of_dicts.append(dict_entry)

                #add also l3out with svi
                if 'l3outs' not in tenant:
                    continue
                for l3out in tenant['l3outs']:
                    l3out_name = l3out['name']
                    if 'vrf' not in l3out:
                        continue
                    if 'domain' not in l3out:
                        continue
                    domain = l3out['domain']
                    vrf_name = l3out['vrf']
                    if 'node_profiles' not in l3out:
                        continue
                    for np in l3out['node_profiles']:
                        if 'interface_profiles' not in np:
                            continue
                        for ip in np['interface_profiles']:
                            if 'interfaces' not in ip:
                                continue

                            for interface in ip['interfaces']:
                                if 'svi' not in interface:
                                    continue

                                if 'node2_id' in interface:
                                    node_ids =  [interface['node_id'], interface['node2_id']]
                                else:
                                    node_ids = [interface['node_id']]
                                
                                if 'channel' in interface:
                                    channel = interface['channel']
                                else:
                                    if 'port' in interface:
                                        channel = interface['port']
                                    else:
                                        channel = ''
                                
                                for node_id in node_ids:  

                                    int_p = ''

                                    if 'ip' in interface:
                                        int_p = interface['ip']
                                    if 'ip_shared' in interface:
                                        int_p = interface['ip_shared']

                                    dict_entry = {
                                        'VLAN': interface['vlan'],
                                        'node_id': node_id,
                                        'oob_addr': '',
                                        'host_name': 'external epg',
                                        'tenant_name': tenant_name,
                                        'ap_name': l3out_name,
                                        'epg_name': 'external epg',
                                        'bd_name': 'svi',
                                        'vrf': vrf_name,
                                        'subnet_ip': int_p,
                                        'port': channel,
                                        'domain': domain
                                    }

                                    # Add dictionary to list
                                    list_of_dicts.append(dict_entry)

    return list_of_dicts




def main():
    # Example usage
    directory_path = 'dir_path'
    node_list = extract_node_data_from_yaml_files(directory_path)
    bd_list = extract_bd_data_from_yaml_files(directory_path)
    output = extract_epg_data_from_yaml_files(directory_path, node_list, bd_list)

    excel = excel_lib.Excel('./', "Vlan_Encap_" + directory_path)

    column = ['VLAN', 'node_id', 'oob_addr', 'host_name', 'tenant_name', 'ap_name', 'epg_name', 'bd_name', 'vrf', 'subnet_ip', 'port', 'domain']
    excel.create_sheet("Vlan_Encap", column)
    excel.fill_sheet(output, "Vlan_Encap")

    print("Vlan_Encap.xlsx successfully created")

    excel.convert_to_csv("Vlan_Encap", "Vlan_Encap.csv")


if __name__ == "__main__":
    main()
