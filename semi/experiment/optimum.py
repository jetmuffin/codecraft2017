import re


def parse_case(str):
	index = str.find("case_example")
	return str[index + 13 :].replace("/", ".").replace(".txt", "")

	
def read_optimum(case_file):
	with open("optimum_solution") as f:
		optimum_solution = {}
		while True:
			line = f.readline()
			if not line:
				break
			splits = line.split()

			case = splits[0]
			answer = int(splits[1])
			servers = [tuple(map(int, re.findall(r'\d+', splits[i]))) for i in range(2, len(splits))]

			optimum_solution[case] = {
				'name': case_file,
				'optimum': answer,
				'solution': servers
			}

		if optimum_solution.has_key(case_file):
			return optimum_solution[case_file]
		else:
			return None