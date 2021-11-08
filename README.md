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


## Authors

* **Gaetano Carlucci** 
