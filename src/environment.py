class Environment:
	def __init__(self):
		self.hashmap = {}

	def put(self, lvalue, rvalue):
		self.hashmap[lvalue] = rvalue

	def get(self, lvalue):
		return self.hashmap[lvalue]
