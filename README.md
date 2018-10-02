# GooglePerfkitAnsible
For automatically deploying google perfkit to servers in the cloud using asnible

To run playbook go to playbooks folder then run:

ansible-playbook main.yml

To set host to deploy to edit the hosts file in inventories folder


./pkb.py --benchmarks=ping_benchmark --json_path=/opt/results/DigitalOcean.4gb.ping_benchmark.2018-10-01-12-31.results.json --num_vms=2 --aerospike_storage_type=disk --data_disk_size=20 --zones=sfo2 --machine_type=4gb --cloud=DigitalOcean --metadata="cloud_provider:DigitalOcean,machine_type:4gb,region:sfo2"
