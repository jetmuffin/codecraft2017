import sys
import os
import subprocess
import time
import re
import term
from tqdm import tqdm
from optimum import *
from terminaltables import AsciiTable


def read_case():
	cases = []
	with open('case_list') as f:
		while True:
			line = f.readline()
			if not line or len(line) == 0:
				break
			cases.append(line.rstrip())
	return cases

def run(program_path, test_case_dir, test_case):
	test_case_path = os.path.realpath(os.path.join(test_case_dir, test_case))
	optimum = 0
	solution = []

	p = subprocess.Popen([program_path, test_case_path], shell=False, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)

	last_t = None
	with tqdm(total=55, desc=parse_case(test_case)) as tbar:
		while True:  
			line = p.stdout.readline()  
			if not line:  
				break  

			t = re.findall(r'time\(.*\)', line) 
			if len(t) > 0:
				t = int(float(t[0].replace('time(', '').replace(')', '')))
				if t != last_t:
					tbar.update(1)
					last_t = t

			else:
				if 'global minimum:' in line:
					optimum = int(line.split()[2])
				if 'server list:' in line:
					solution = ' '.join(line.split()[2:])

	return optimum, solution
	

def report(result, optimum):
	total_diff = 0
	table_data = [
		[
			term.format('case', term.bold), 
			term.format('answer', term.bold),
			term.format('optimum', term.bold),
			term.format('error', term.bold),
		]
	]

	for test_case, solution in result.iteritems():
		table_data.append([
			test_case,
			result[test_case][0],
			optimum[test_case]['optimum'],
			optimum[test_case]['optimum'] - result[test_case][0],
		])

		total_diff += optimum[test_case]['optimum'] - result[test_case][0]

	table = AsciiTable(table_data)
	term.writeLine('Test result:')
	term.writeLine('Average error:' + term.format(float(total_diff)/float(len(result)), term.red, term.bold))
	term.writeLine(table.table)


def main():
	if len(sys.argv) < 3:
		print "Usage: python test.py <cpp_program_path> <test_case_dir>"
		sys.exit(1)

	optimum = read_optimum()
	cases = read_case()
	result = {}

	term.writeLine('Running test for program: ' + term.format(sys.argv[1], term.bold))
	for c in cases:
		answer, solution = run(sys.argv[1], sys.argv[2], c)
		result[parse_case(c)] = (answer, solution)

	report(result, optimum)


if __name__ == '__main__':
	main()