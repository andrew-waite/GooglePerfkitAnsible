# GooglePerfkitAnsible
For automatically deploying google perfkit to servers in the cloud using asnible

To run playbook go to playbooks folder then run:

ansible-playbook main.yml

To set host to deploy to edit the hosts file in inventories folder

doctl auth init -t {apikey}

./pkb.py --benchmarks=ping --num_vms=1 --data_disk_size=20 --zones=sfo2 --cloud=DigitalOcean --openstack_volume_size=20 --machine_type=2g --ip_addresses=INTERNAL --openstack_network=net-2 --openstack_volume_type=TIER1 --metadata="cloud_provider:DigitalOcean,region:soft,machine_type:2g"

aws configure set a a us-eas a

aws configure list

Below command method doesnt support 2fa

azure login -u <username> -p <password>

This one does support 2fa 

azure login

test it is install properly

azure vm list


Finally, make sure Azure is in Resource Management mode and that your account is authorized to allocate VMs and networks from Azure:

$ azure config mode arm
$ azure provider register Microsoft.Compute
$ azure provider register Microsoft.Network
