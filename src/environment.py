class Environment:
	def __init__(self, parent=None):
		self.hashmap = {}
		self.parent = parent # this is for lexical scoping of variable

	def putAt(self, lvalue, rvalue, index):
		# print('putat ', '"lvalue" ',lvalue, '"rvalue"', rvalue, index)
		if (index == 0):
			self.put(lvalue, rvalue)
		else:
			self.parent.putAt(lvalue, rvalue, index-1)
	def put(self, lvalue, rvalue):
		self.hashmap[lvalue] = rvalue

	def getAt(self, lvalue, index):
		# print('getat index', index)
		if (index == 0):
			return self.get(lvalue)
		else:
			return self.parent.getAt(lvalue, index-1)
	def get(self, lvalue):
		# print('get', lvalue)
		try:
			ret_val = self.hashmap[lvalue]
			# print('hashmap', self.hashmap)
			return ret_val
		except KeyError: # if not found in current environment search the parent environment for the needed variable
			if (self.parent != None):
				return self.parent.get(lvalue)
			else: # raise exception if the global environment doesn't have the needed variable
				raise Exception(f'undefined variable {lvalue}')


	def putIfExists(self, lvalue, rvalue):
		if (lvalue in self.hashmap.keys()):
			self.put(lvalue, rvalue) # put the value in current scope 
		elif (self.parent != None):
			self.parent.putIfExists(lvalue, rvalue) # if the value is not found in current scope put it recursively in parent scope
		else:
			raise Exception(f"undefined variable '{lvalue}'")# raise exception if the global scope doesn't contain the variable

	def __str__(self):
		return f"{str(self.parent)} -> {str(self.hashmap)}"