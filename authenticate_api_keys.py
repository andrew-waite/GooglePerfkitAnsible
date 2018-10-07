import subprocess
import yaml
import argparse
import datetime
import re
import os
import sys

class api_key_reader():

	def __init__(self):
		self.config = self.import_yaml()

	def import_yaml(self):
		my_path = os.path.abspath(os.path.dirname(__file__))
		path = os.path.join(my_path, 'passwords/keys.yml')
		print(path)
		with open(path, 'r') as stream:
			try:
				return yaml.load(stream)
			except yaml.YAMLError as exc:
				print(exc)

	def runAuthCommands(self):
		#Digital Ocean configure
		try:
			if self.config['digital_ocean_key'] is None: # The variable
				print('The key is empty skipping')
		except NameError:
			print ("The digital ocean key is not set. Skipping this step...")
		else:
			command = 'doctl auth init -t ' + self.config['digital_ocean_key']
			result = subprocess.call(command, shell=True)

		#AWS configure
		try:
			if self.config['aws_keys']['aws_access_key_id'] is None: # The variable
				print('The key is empty skipping')
		except NameError:
			print ("The aws key is not set. Skipping this step...")
		else:
			command0 = 'aws configure set aws_access_key_id ' + self.config['aws_key']['aws_access_key_id']
			command1 = 'aws configure set aws_secret_access_key ' + self.config['aws_key']['aws_secret_access_key']
			command2 = 'aws configure set default.region ' + self.config['aws_key']['default_region']

			subprocess.call(command0, shell=True)
			subprocess.call(command1, shell=True)
			subprocess.call(command2, shell=True)

		#Azure configure
		try:
			if self.config['azure_keys']['username'] is None: # The variable
				print('The key is empty skipping')
		except NameError:
			print ("The Azure username is not set. Skipping this step...")
		else:
			command = 'azure login -u ' + self.config['azure_keys']['username'] + ' -p ' + self.config['azure_keys']['password']
			subprocess.call(command, shell=True)
			subprocess.call('azure config mode arm', shell=True)
			subprocess.call('azure provider register Microsoft.Compute', shell=True)
			subprocess.call('azure provider register Microsoft.Network', shell=True)

def main():
	perfkitRun = api_key_reader()
	perfkitRun.runAuthCommands()

main()
