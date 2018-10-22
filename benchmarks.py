#!/usr/bin/env python

import subprocess
import yaml
import argparse
import datetime
import re
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--cloud_provider", help="Enter the cloud name here", required=True)
ARGS = parser.parse_args()

class googlePerfKit():

    def __init__(self):
        self.config = self.import_yaml()
        self.core_config = self.config['core_config']
        self.elastic_search = self.config['elasticsearch']
        self.cloud_config = self.config['cloud_config'][ARGS.cloud_provider]
        self.benchmarks = self.config['benchmarks']

    def import_yaml(self):

        with open('benchmarks.yml', 'r') as stream:
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

    def format_elastic_search(self):
        if(self.elastic_search['enabled'] == True):
            elasticSearchUrl = '--es_uri=' \
                                + self.elastic_search['url'] \
                                + ' --es_index=' \
                                + self.elastic_search['index_name'] \
                                + ' --es_type=' \
                                + self.elastic_search['type_name']
            return elasticSearchUrl
        else:
            return ''

    def build_base_command(self, benchmark, mode=None, workload=None, storage_type=None, storage_tier=None):

        command = './pkb.py ' \
                  + '--benchmarks=' + benchmark + ' ' \
                  + self.format_results_log(benchmark, mode, workload)

        if(self.format_elastic_search() != ''):
            command = command + ' ' + self.format_elastic_search()

        if mode:
            command = command + ' --' + mode + '=' + workload
        for option, value in self.cloud_config['options'].iteritems():
            command = command + (' --' + str(option) + '=' + str(value))
        return command

    def run_benchmarks_list(self, BENCHMARKGROUP):

        benchmarks = []
        for benchmarkName in self.benchmarks:
            benchmarks.append(self.build_base_command(benchmarkName))
        return benchmarks

    def run_benchmarks(self):

        env = os.environ.copy()
        for benchmark in self.benchmarks:
            for command in self.run_benchmarks_list(benchmark):
                metaCommand = command + ' --metadata="cloud_provider:' + ARGS.cloud_provider \
                        + ',machine_type:' + self.cloud_config['flavor_name'] \
                        + ',region:' + self.cloud_config['options']['zones'] + '"'
                print(metaCommand)
                result = subprocess.Popen(metaCommand, shell=True, stdout=subprocess.PIPE, cwd=self.core_config['perfkit_path'], env=env)
                print(result.stdout.read())
                self.write_log(result.stdout.read())

def main():
    perfkitRun = googlePerfKit()
    print(perfkitRun);
    print ("Started the run at : " + perfkitRun.get_date() + "on cloud: " + ARGS.cloud_provider)
    perfkitRun.run_benchmarks()
    print(perfkitRun.run_benchmarks());
    print ("Finished the run at : " + perfkitRun.get_date())

main()
