# Get Vlan Encap Per Leaf


This tool collects the Vlan Encap used on each leaf shows them in an excel files.

## Getting Started

### Prerequisites

* Python 3 (create your venv)

```
 python3 -m venv venv
```
* Activate your venv

```
 source venv/bin/activate
```

### Installing
1. Run pip command to install required libraries.

```
> pip install -r requirements.txt
```

## Usage

Insert the login data in the file `Utils/credentials.json`:

Example:
```
{
"apic_ip_address": "X.X.X.X",
"apic_port": "443",
"apic_admin_user": "admin",
"apic_admin_password": "xxxxxxxx"
}
```

then run the script using a *python3* interpreter:

```
$python3 get-encap-vlan-per-leaf.py
```

it will create the xlsx file `Vlan_Encap_Per_Leaf.xlsx` that contains a sheet with the list of encap vlan used on each leaf:


<img src="excel.png" width="400" />

and it will also provide a `Vlan_Encap.csv` file with the date in comma-separated values format.


## CSV Fields Explanation

### VLAN
- **Description**: The external VLAN encapsulation identifier used by the corresponding EPG, in the format `vlan-<number>`. This is a unique label for the VLAN.
- **Example**: `vlan-876`

### node_id
- **Description**: An identifier for the specific node (or switch) within the ACI fabric. 
- **Example**: `101`

### oob_addr
- **Description**: The out-of-band IP address for the node. This is used for management and administrative tasks outside of the data traffic.
- **Example**: `10.51.89.5/25`

### host_name
- **Description**: The hostname of the switch or node in the ACI fabric. This is a label assigned to the hardware device for easier identification.
- **Example**: `POD1-LEAF1`

### tenant_name
- **Description**: The name of the tenant within the ACI fabric. In ACI, tenants represent isolated virtualized environments or groups.
- **Example**: `Pippo-Tenant`

### ap_name
- **Description**: The name of the Application Profile. This is a container for EPGs (End Point Groups) and is used to group related application components.
- **Example**: `CLIENT_AP`

### epg_name
- **Description**: The name of the End Point Group. EPGs represent a set of endpoints (devices, servers, etc.) that share common policies and configurations.
- **Example**: `CLIENT_EPG3`

### bd_name
- **Description**: The name of the Bridge Domain. Bridge Domains represent Layer 2 broadcast domains and are used to define the scope of Layer 2 traffic.
- **Example**: `CLIENT_BD`

### vrf
- **Description**: The name of the Virtual Routing and Forwarding instance. VRFs are used to create isolated Layer 3 routing tables.
- **Example**: `DEFAULT_VRF`

### subnet_ip
- **Description**: The subnet IP address and subnet mask associated with the Bridge Domain. This defines the IP range used by the BD for Layer 3 routing.
- **Example**: `10.116.141.1/24`



## Authors

* **Gaetano Carlucci** 
