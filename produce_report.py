import subprocess
import yaml
import argparse
import datetime
import re
import os
import sys
from json2html import *
import json

fileName = None

class report_produce():
	def fromatJsonFile(self):
		global fileName
		with open('sample.json') as f:
			output = ''
			for line in f.readlines():
				output += line.replace('\n', ',')
			
			print(output)
			f.close()
	 
		file = open('sample.json', 'w')
		fileName = file.name
		file.write('[' + output + ']')
		file.flush()
		file.close()
		
	def openJsonFile(self):
		with open('sample.json') as f:
			output = ''
			for line in f.readlines():
				output += line
		f.close()
		return output
	
	def getFileName(self):
		return fileName
		
	def writeHtmlToFile(self, fileName, html):
		myfile = open(fileName.replace('.json', '.html'), 'w+')
		myfile.write(html)
		myfile.flush()
		myfile.close()

def main():
	report = report_produce()
	report.fromatJsonFile()
	print(report.openJsonFile())
	jsonFile = report.openJsonFile()
	infoFromJson = json.loads(jsonFile)
	jsonhtml = json2html.convert(json = infoFromJson)
	print(jsonhtml)
	report.writeHtmlToFile(report.getFileName(), jsonhtml)
main()
