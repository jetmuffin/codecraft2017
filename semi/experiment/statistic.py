import re
import sys
import term
from optimum import *
from graph import *
from terminaltables import AsciiTable


def report(graph, solutions):
	solution = solutions['solution']
	customer_solution_len = 0

	table_data = [
		[
			term.format('server', term.bold), 
			term.format('level', term.bold),
			term.format('is_customer', term.bold),
			term.format('request', term.bold),
			term.format('degree', term.bold),
			term.format('cap / cost', term.bold),
		]
	]

	for s in solution:
		if(graph.nodes[s[0]].request > 0):
			customer_solution_len = customer_solution_len + 1

		table_data.append([
			s[0], 
			s[1], 
			"yes" if graph.nodes[s[0]].request > 0 else "no",
			"%d (%d)" % (graph.nodes[s[0]].request, graph.request_level(graph.nodes[s[0]].request)) if graph.nodes[s[0]].request > 0 else 0,
			"%d / %d" % (len(graph.nodes[s[0]].edges), graph.max_degree),
			"%f (%d / %d)" % (float(graph.nodes[s[0]].cap_div_cost)/float(graph.max_cap_div_cost), graph.nodes[s[0]].cap_div_cost, graph.max_cap_div_cost)
		])
	table = AsciiTable(table_data)


	term.writeLine('Statistical report for ' + term.format(solutions['name'], term.green))
	term.writeLine('The optimum is ' + term.format(solutions['optimum'], term.red, term.bold))
	term.writeLine('Customer server number: ' + term.format("%f ( %d / %d )" % \
		(float(customer_solution_len)/ float(len(solution)), customer_solution_len, len(solution)), term.red, term.bold))
	term.writeLine(table.table)

def main():
	if len(sys.argv) < 2:
		print "Usage: python statistic.py <case_file>"
		sys.exit(1)

	graph = read_graph(sys.argv[1])

	case_file = parse_case(sys.argv[1])
	solutions = read_optimum(case_file)

	report(graph, solutions)


if __name__ == '__main__':
	main()