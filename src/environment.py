class Environment:
	def __init__(self):
		self.hashmap = {}

	def put(self, lvalue, rvalue):
		self.hashmap[lvalue] = rvalue

	def get(self, lvalue):
		return self.hashmap[lvalue]

	def putIfExists(self, lvalue, rvalue):
		if lvalue in self.hashmap.keys():
			self.put(lvalue, rvalue)
		else:
			raise Exception(f"undefined variable '{lvalue}'")
