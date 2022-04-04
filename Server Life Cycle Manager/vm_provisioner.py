# Import the needed credential and management objects from the libraries.
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
import os
import json

print(f"Provisioning a virtual machine...some operations might take a minute or two.")

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()
group_flag = False
network_flag = False
vm_flag = False
# Retrieve subscription ID from environment variable.
f = open('../subscription_config.json')
subs = json.load(f)
subscription_id = subs["id"]


# Step 1: Provision a resource group

# Obtain the management object for resources, using the credentials from the CLI login.
resource_client = ResourceManagementClient(credential, subscription_id)

# Constants we need in multiple places: the resource group name and the region
# in which we provision resources. You can change these values however you want.
file = open('../network_resource_config.json')
v_net = json.load(file)

RESOURCE_GROUP_NAME = v_net["RESOURCE_GROUP_NAME"]           #"IAS_AZURE_GROUP_TEST"
LOCATION =  v_net["LOCATION"]                                #"centralindia"


for item in resource_client.resource_groups.list():
    if item.name == RESOURCE_GROUP_NAME:
        group_flag = True

# Provision the resource group.
if group_flag == False:
    rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
        {
            "location": LOCATION
        }
    )
    print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")
else:
    print(f"Resource group {LOCATION} already present in the {LOCATION} region")
# For details on the previous code, see Example: Provision a resource group
# at https://docs.microsoft.com/azure/developer/python/azure-sdk-example-resource-group


# Step 2: provision a virtual network

# A virtual machine requires a network interface client (NIC). A NIC requires
# a virtual network and subnet along with an IP address. Therefore we must provision
# these downstream components first, then provision the NIC, after which we
# can provision the VM.

# Network and IP address names
VNET_NAME = v_net["VNET_NAME"]                      #"IAS_AZURE_VNET_TEST"
SUBNET_NAME = v_net["SUBNET_NAME"]                  #"IAS_AZURE_SUBNET_TEST"
IP_NAME = v_net["IP_NAME"]                          #"IAS_AZURE_IP_TEST"
IP_CONFIG_NAME = v_net["IP_CONFIG_NAME"]            #"IAS_AZURE_IPCONFIG_TEST"
NIC_NAME =  v_net["NIC_NAME"]                       #"IAS_AZURE_NIC_TEST"

# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)

for item in network_client.virtual_networks.list(RESOURCE_GROUP_NAME):
    if item.name == VNET_NAME:
        network_flag = True

# Provision the virtual network and wait for completion
if network_flag == False:
    poller = network_client.virtual_networks.begin_create_or_update(RESOURCE_GROUP_NAME,
        VNET_NAME,
        {
            "location": LOCATION,
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            }
        }
    )
    vnet_result = poller.result()
    print(f"Provisioned virtual network {vnet_result.name} with address prefixes {vnet_result.address_space.address_prefixes}")

    # Step 3: Provision the subnet and wait for completion
    poller = network_client.subnets.begin_create_or_update(RESOURCE_GROUP_NAME, 
        VNET_NAME, SUBNET_NAME,
        { "address_prefix": "10.0.0.0/24" }
    )
    subnet_result = poller.result()

    print(f"Provisioned virtual subnet {subnet_result.name} with address prefix {subnet_result.address_prefix}")

    # Step 4: Provision an IP address and wait for completion
    poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME,
        IP_NAME,
        {
            "location": LOCATION,
            "sku": { "name": "Standard" },
            "public_ip_allocation_method": "Static",
            "public_ip_address_version" : "IPV4"
        }
    )

    ip_address_result = poller.result()
   
    
    print(f"Provisioned public IP address {ip_address_result.name} with address {ip_address_result.ip_address}")

    # Step 5: Provision the network interface client
    poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME,
        NIC_NAME, 
        {
            "location": LOCATION,
            "ip_configurations": [ {
                "name": IP_CONFIG_NAME,
                "subnet": { "id": subnet_result.id },
                "public_ip_address": {"id": ip_address_result.id }
            }]
        }
    )

    nic_result = poller.result()

    ip_address_details = {
        "resource_group_name" : RESOURCE_GROUP_NAME,
        "vnet_name" : VNET_NAME,
        "subnet_name)" : SUBNET_NAME, 
        "ip_name" : ip_address_result.name,
        "ip_cofig_name" : IP_CONFIG_NAME,
        "ip_address" : ip_address_result.ip_address,
        "location": LOCATION,
        "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
        },
        "ip_configurations": [ {
                "name": IP_CONFIG_NAME,
                "subnet": { "id": subnet_result.id },
                "public_ip_address": {"id": ip_address_result.id }
            }],
        "nic_name" : nic_result.name,
        "nic_id" : nic_result.id
    }
    json_object = json.dumps(ip_address_details, indent = 4)
    with open("../configuration_details.json", "w") as outfile:
        outfile.write(json_object)
    print(f"Provisioned network interface client {nic_result.name}")
else:
    print("Subnet Already present")


# Step 6: Provision the virtual machine
f1 = open('./vm_provisioning_config.json')
f2 = open('../vm_user_config.json')
vm_s = json.load(f1)
vm_user = json.load(f2)

provisioned_vm = []
# Obtain the management object for virtual machines
compute_client = ComputeManagementClient(credential, subscription_id)
for item in compute_client.virtual_machines.list(RESOURCE_GROUP_NAME):
    for key in vm_s:
        if item.name == vm_s[key]["VM_NAME"]:
            vm_flag = True

f3 = open('../configuration_details.json')
config_details = json.load(f3)

if vm_flag == False:
    for key in vm_s:
        print(f"Provisioning virtual machine "+ str(vm_s[key]["VM_NAME"]) +"; this operation might take a few minutes.")

        # Provision the VM specifying only minimal arguments, which defaults to an Ubuntu 18.04 VM
        # on a Standard DS1 v2 plan with a public IP address and a default virtual network/subnet.

        poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, vm_s[key]["VM_NAME"],
            {
                "location": LOCATION,
                "storage_profile": {
                    "image_reference": {
                        "publisher": 'Canonical',
                        "offer": vm_s[key]["offer"],        #"UbuntuServer",
                        "sku": vm_s[key]["sku"],            #"16.04.0-LTS",
                        "version": "latest"
                    }
                },
                "hardware_profile": {
                    "vm_size": "Standard_DS1_v2"
                },
                "os_profile": {
                    "computer_name": vm_s[key]["VM_NAME"],
                    "admin_username": vm_user["username"],
                    "admin_password": vm_user["password"]
                },
                "network_profile": {
                    "network_interfaces": [{
                        "id": config_details["nic_id"],
                    }]
                }        
            }
        )

        vm_result = poller.result()
        provisioned_vm.append(vm_result)

    print(f"Provisioned virtual machines : {provisioned_vm}")

else:
    print("VM already present")