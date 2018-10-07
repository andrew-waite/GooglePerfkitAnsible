#!/usr/bin/env python

import subprocess
import yaml
import argparse
import datetime
import re
import os
import sys

def import_yaml():
    with open('aaa.yml', 'r') as stream:
        try:
	        return yaml.load(stream)
        except yaml.YAMLError as exc:
        	print(exc)
def main():
	abc = import_yaml()
	print('a')
	
	for key in abc['a']:
		print(key)
	
main()