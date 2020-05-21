import sys 

class Lox:
	def __init__(self):
		self.had_error = False
	
	@staticmethod
	def main():
		if len(sys.argv) > 2:
			print('usage: plox files')
			exit(64) #see open_bsd exit code (just for standardization)
		elif len(sys.argv) == 2:
			Lox.runFile(sys.argv[1])

		else:
			Lox.runPrompt()

	@staticmethod
	def runFile(path):
		source_code = ''
		with open(path, mode='r') as content:
			source_code = content.read()

		lox_interpreter = Lox()
		lox_interpreter.run(source_code)

	@staticmethod
	def runPrompt():
		lox_interpreter = Lox()
		while True:
			print('>>', end=' ')
			lox_interpreter.run(input())
	
	def run(self, program):
		for token in program:
			print(token, end='')
		print()

	
	def error(self, line, err_msg):
		report(line, "", err_msg) 

	def report(self, line, where, err_msg):
		print(f'[Line {line}] of {where} following errors where reported\n{err_msg}')



#run the program by calling the static function main of the interpreter
Lox.main()
