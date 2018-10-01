#!/usr/bin/env python

import subprocess
import yaml
import argparse
import datetime
import re
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--cloud_provider", help="Service provider to benchmark \
                    [UKCloud-OpenStack | UKCloud-vCloud | AWS-UK | AWS-US | Azure | Google]", required=True)
parser.add_argument("--config", help='Path to perfkit yaml config', required=True)
ARGS = parser.parse_args()

class ukcloudPerfkit():

    def __init__(self):
        self.config = self.import_yaml()
        self.core_config = self.config['core_config']
        self.common_config = self.config['common_config']
        self.cloud_config = self.config['cloud_config'][ARGS.cloud_provider]
        self.benchmarks = self.config['benchmarks']

    def import_yaml(self):
    
        with open(ARGS.config, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_date(self):

        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d-%H-%M")

    def write_log(self, data):
        
        file = open(self.core_config['log_path'] + 'perfkit-' + self.get_date() + '.log', "w+") 
        file.write(data)
        file.close() 

    def format_results_log(self, benchmark, mode, workload):

        logPath = '--json_path=' \
                  + self.core_config['json_path'] \
                  + ARGS.cloud_provider \
                  + '.' + self.cloud_config['flavor_name'] \
                  + '.' + benchmark
        if workload:
            logPath = logPath + '.' + workload
        logPath = logPath + '.' + self.get_date() + '.' + 'results.json'
        return logPath
    
    def build_base_command(self, benchmark, mode=None, workload=None, storage_type=None, storage_tier=None):
    
        command = './pkb.py ' \
                  + '--benchmarks=' + benchmark + ' ' \
                  + self.format_results_log(benchmark, mode, workload)
        if mode:
            command = command + ' --' + mode + '=' + workload 
        for option, value in self.common_config.iteritems():
            command = command + (' --' + str(option) + '=' + str(value))
        for option, value in self.cloud_config['options'].iteritems():
            command = command + (' --' + str(option) + '=' + str(value))
        return command

    def run_benchmark_group(self, BENCHMARKGROUP):
    
        benchmarks = []
        for benchmarkName, sub_tests in self.benchmarks[BENCHMARKGROUP].iteritems():
            if sub_tests:
                for mode in sub_tests:
                    for test in self.benchmarks[BENCHMARKGROUP][benchmarkName][mode]:
                        benchmarks.append(self.build_base_command(benchmarkName, mode, test))
            else:
                benchmarks.append(self.build_base_command(benchmarkName))
        return benchmarks
    
    def set_env(self):

        env = os.environ.copy()
        if self.cloud_config['environment']:
            file = open(self.cloud_config['environment'], 'r')
            for line in file:
                if re.match('^export.*', line):
                    var = re.sub('export ', '', line)
                    key, val = var.split('=')
                    val = re.sub('^"', '', val)
                    val = re.sub('"$', '', val)
                    val = re.sub("^'", '', val)
                    val = re.sub("'$", '', val)
                    env[key] = val.rstrip()
        return env

    def run_benchmarks(self):
        
        env = self.set_env()
        for benchmark in self.benchmarks:
            for command in self.run_benchmark_group(benchmark):
                if self.cloud_config['storage_tiers']:
                    for storage in self.cloud_config['storage_tiers']:
                        for param, value in storage.iteritems():
                            metaCommand = command + ' --' + param + '=' + value \
                                        + ' --metadata="cloud_provider:' + ARGS.cloud_provider \
                                        + ',region:' + self.cloud_config['options']['zones'] \
                                        + ',machine_type:' + self.cloud_config['flavor_name'] \
                                        + ',storage_type:' + value + '"'
                            print(metaCommand)
                            result = subprocess.Popen(metaCommand, shell=True, stdout=subprocess.PIPE, cwd=self.core_config['perfkit_path'], env=env)
                            print(result.stdout.read())
                            self.write_log(result.stdout.read())
                else:
                    metaCommand = command + ' --metadata="cloud_provider:' + ARGS.cloud_provider \
                                  + ',machine_type:' + self.cloud_config['flavor_name'] \
                                  + ',region:' + self.cloud_config['options']['zones'] + '"'
                    print(metaCommand)
                    result = subprocess.Popen(metaCommand, shell=True, stdout=subprocess.PIPE, cwd=self.core_config['perfkit_path'], env=env)
                    print(result.stdout.read())
                    self.write_log(result.stdout.read())
    
def main():
    perfkitRun = ukcloudPerfkit()
    print(perfkitRun);
    print ("Started the run at : "+perfkitRun.get_date())
    perfkitRun.run_benchmarks()
    print(perfkitRun.run_benchmarks());
    print ("Finished the run at : "+perfkitRun.get_date())

main()