#!/usr/bin/env python3.7

import os
import sys
import logging
import re
import subprocess
from shutil import which
from datetime import date

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

brokerlog_path = "logs/broker.log"
report_path = "logs/REPORT.log"

OUT = ""

OUT += "=============================================\n"
OUT += "===       Simulation Report Summary       ===\n"
OUT += "=============================================\n"
OUT += "\n\n"

def process_dot(line):
	global OUT
	OUT += "\n\n\n"
	part = line.partition("DOT: ")

	res = ""
	if which("graph-easy"):
		proc = subprocess.run(["graph-easy"], stdout=subprocess.PIPE, input=part[2], encoding='ascii')
		res = proc.stdout
	else:
		res = "Install Perl script `sudo cpanm Graph::Easy` to parse Dot format"
	
	timestamp = part[0].split(' ')[1]
	OUT += "Topology at " + timestamp + ":\n\n"
	OUT += res + "\n\n\n"

def process_fabric_cfg(line):
	global OUT
	part = line.partition("FABRIC_CONFIG: ")
	OUT += part[2]


with open(brokerlog_path, "r") as file:
	for line in file:
		if "FABRIC_CONFIG" in line:
			process_fabric_cfg(line)

		if ": FABRIC_EV:" in line: # results from executing Fabric event
			OUT += "Fabric event response:\n"
			OUT += "    " + line
		
		if "Scheduling plugin fabric" in line:
			part = line.split(' ')
			OUT += f"Scheduling fabric event at: {part[1]}\n"
		
		if "Calling at" in line:
			part = line.partition("Calling at ")
			OUT += "   " + part[2]

		if "DOT" in line: # topology in DOT format
			process_dot(line)

with open(report_path, 'w') as report_file:
	report_file.write(OUT)
