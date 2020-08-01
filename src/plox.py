import sys
from lexer import Scanner
from parser import Parser, Calculator, StatementExecutor, NativeTimer, Exit, Str, Random
from ASTPrinter import ASTPrinter
from environment import Environment
from resolver import Resolver
class Lox:
	def __init__(self):
		self.had_error = False
		self.environment = Environment()
		self.resolver = Resolver()

		self.prompt_signature = '#|>>'
		### initialize native function####
		timer = NativeTimer()
		timer.register('timer', self.environment)

		ext = Exit()
		ext.register('exit', self.environment)

		string = Str()
		string.register('str', self.environment) 

		random = Random()
		random.register('random', self.environment)
		##################################
	
	@staticmethod
	def main():
		if len(sys.argv) > 2:
			if (sys.argv[2] == '-i'):
				Lox.runFileInteractive(sys.argv[1], Lox())
			else:
				print('''usage: 
					plox files [-i]
					-i: run files in interactive mode''')
			exit(64) #see open_bsd exit code (just for standardization)
		elif len(sys.argv) == 2:
			Lox.runFile(sys.argv[1], Lox())

		else:
			Lox.runPrompt(Lox())

	@staticmethod
	def runFileInteractive(path, lox_interpreter):
		Lox.runFile(path, lox_interpreter)
		Lox.runPrompt(lox_interpreter)

	@staticmethod
	def runFile(path, lox_interpreter):
		with open(path, mode='r') as content:
			source_code = content.read()
			lox_interpreter.run(source_code)
		### add interpreter in prompt mode after this. if necessary arguments are passed
	
	@staticmethod
	def runPrompt(lox_interpreter):
		while True:
			print(lox_interpreter.prompt_signature, end=' ')
			try:
				lox_interpreter.run(input())
			except Exception as e: 
				print(e)
	
	def run(self, source_code):
		#why this runs, its because of the lox interpreter environment, which remains in existence even after this function ends 
		scanner = Scanner(source_code)
		scanner.scanTokens()
		# print(scanner.toString())
		parser = Parser(scanner.token_list)
		parser.parse()
		#print(Calculator().calculate(parser.AST))
		self.resolver.resolveAll(parser.AST)
		

		interpreter = StatementExecutor(self.environment, self.resolver)
		for ast in parser.AST:
			interpreter.execute(ast)
			# print(ASTPrinter().print(ast))

	def error(self, line, err_msg):
		report(line, "", err_msg) 

	def report(self, line, where, err_msg):
		print(f'[Line {line}] of {where} following errors where reported\n{err_msg}')



#run the program by calling the static function main of the interpreter
Lox.main()