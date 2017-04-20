class Node:
	def __init__(self, id, cost):
		self.id = id
		self.cost = cost
		self.edges = []
		self.request = None
		self.cap_div_cost = 0

	def __str__(self):
		return "id(%d) cost(%d) request(%d)" % (self.id, self.cost, self.request if self.request else 0)


class Edge:
	def __init__(self, source, target, cap, cost):
		self.source = source
		self.target = target
		self.cap = cap
		self.cost = cost

	def __str__(self):
		return "from(%d) to(%d) cap(%d) cost(%d)" % (self.source, self.target, self.cap, self.cost)


class Graph:
	def __init__(self):
		self.nodes = []	
		self.edges = []
		self.levels = []
		self._statistic = False

	@property
	def max_degree(self):
		if not self._statistic:
			self.statistic()

		return self._max_degree
	
	@property
	def max_cap_div_cost(self):
		if not self._statistic:
			self.statistic()

		return self._max_cap_div_cost

	def statistic(self):
		self._statistic = True

		_max_degree = -1
		_max_cap_div_cost = -1

		for n in self.nodes:
			_max_degree = max(_max_degree, len(n.edges))

			for e in n.edges:
				n.cap_div_cost += float(e.cap) / float(e.cost) 
			_max_cap_div_cost = max(_max_cap_div_cost, n.cap_div_cost)

		

		setattr(self, '_max_degree', _max_degree)
		setattr(self, '_max_cap_div_cost', _max_cap_div_cost)

	def request_level(self, request):
		for i in range(len(self.levels)):
			if self.levels[i][0] > request:
				return i

	def __str__(self):
		ret = "nodes: \n"
		ret += "\n".join([n.__str__() for n in self.nodes])

		ret += "\nedges: \n"
		ret += "\n".join([e.__str__() for e in self.edges])

		return ret

def read_graph(graph_file):
	with open(graph_file) as f:
		graph = Graph()	

		line = f.readline()
		vec_num, edge_num, customer_num = map(int, line.split())
		
		f.readline()
		while True:
			line = f.readline()
			if line == '\r\n':
				break
			level = map(int, line.split())
			graph.levels.append((level[1], level[2]))

		for i in range(vec_num):
			line = f.readline()
			_, cost = map(int, line.split())
			graph.nodes.append(Node(i, cost))

		f.readline()
		for i in range(edge_num):
			line = f.readline()
			args = map(int, line.split())
			edge = Edge(args[0], args[1], args[2], args[3])
			graph.edges.append(edge)
			graph.nodes[edge.source].edges.append(edge)
			graph.nodes[edge.target].edges.append(edge)

		f.readline()
		for i in range(customer_num):
			line = f.readline()
			args = map(int, line.split())
			graph.nodes[args[1]].request = args[2]

		return graph