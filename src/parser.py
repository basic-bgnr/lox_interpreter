#####################what Visitor Pattern actually is ? #########
#In my understanding, the visitor pattern is primarily to 
#1. reduce code smell, separating classes (multiple) that represent only data and no methods
#   by creating another class (VisitorClass) which gets linked to the data class.
#   The visitor class contains methods that utilizes the data of the data class.
#   The primary benefit is that the data classes are not modified in any way and 
#   all the code that utilizes every data classes are collectively found on single Class i.e the visitor class
#2. The added benefit is that every data class uses `polymorphic` function `linkVisitor` to connect with the visitor class
#   Since the method is polymorphic every data class can call the function with the same parameter i.e the visitor
#   The visitor then can call specific function which manipulates the data of concerned dataclass. for eg.
#   The BinaryExpression, UnaryExpression, GroupingExpression and LiteralExpresssion all have polymorphic function `linkVisitor`
#   At the same time the Visitor Class (i.e ExpressionVisitor) has specific function related to every data class (visitBinaryExpression,
#   visitUnaryExpression,visitGroupingExpression,visitLiteralExpression). All implementation detail can be seen consolidated in a single
#   class.
#3. Apart from this, this pattern also prevent typechecking of every data class manually(when calling a function)  
#   what this pattern does is that at coding time create specific implementation of the data manipulation method and calls that 
#   specific method from the polymorphic method `linkVisitor`, this function for each data class has specific function call
#################################################################
class BlockStatement:
	def __init__(self, statements): 
		self.statements = statements
		self.name = f"<Block>"

	def linkVisitor(self, visitor):
		return visitor.visitBlockStatement(self)

class AssignmentStatement:
	#lvalue : simple identifier token. (todo, make lvalue an expression)
	#rvalue : expression
	def __init__(self, lvalue, rvalue):
		self.lvalue = lvalue
		self.rvalue = rvalue 
		self.name = f"<Assignment>"

	def linkVisitor(self, visitor):
		return visitor.visitAssignmentStatement(self)

class ReassignmentStatement:
	#lvalue : assignable variable
	#rvalue : expression
	def __init__(self, lvalue, rvalue):
		self.lvalue = lvalue
		self.rvalue = rvalue 
		self.name = f"<Reassignment>"

	def linkVisitor(self, visitor):
		return visitor.visitReassignmentStatement(self)

class PrintStatement:
	def __init__(self, expr):
		self.expr = expr
		self.name = f"<{TokenType.PRINT.value}>"

	def linkVisitor(self, visitor):
		return visitor.visitPrintStatement(self)


class ExprStatement:
	def __init__(self, expr):
		self.expr = expr
		self.name = f"<Expression>"


	def linkVisitor(self, visitor):
		return visitor.visitExprStatement(self)

class StatementExecutor:
	def __init__(self, environment):
		self.environment = environment

	def execute(self, statement):
		statement.linkVisitor(self)

	def visitBlockStatement(self, block_statement):
		block_executor = StatementExecutor(Environment(parent=self.environment))
		for statement in block_statement.statements:
			block_executor.execute(statement)

	def visitAssignmentStatement(self, statement):
		calc = Calculator(self.environment)
		lvalue = statement.lvalue.literal #get the name of the varible
		rvalue = calc.calculate(statement.rvalue)
		self.environment.put(lvalue, rvalue)

	def visitReassignmentStatement(self, statement):
		calc = Calculator(self.environment)
		lvalue = statement.lvalue.literal #get the name of the varible
		rvalue = calc.calculate(statement.rvalue)
		self.environment.putIfExists(lvalue, rvalue)


	def visitPrintStatement(self, statement):
		print(Calculator(self.environment).calculate(statement.expr))

	def visitExprStatement(self, statement):
		Calculator(self.environment).calculate(statement.expr)

#Implementation of Visitor Pattern for code simplification 
class ExpressionVisitor:
	def __init__(self):
		pass
	def visitBinaryExpression(self, binary_expression):
		pass
	def visitUnaryExpression(self, unary_expression):
		pass
	def visitGroupingExpression(self, grouping_expression):
		pass
	def visitLiteralExpression(sefl, literal_expression):
		pass

class BinaryExpression:
	#here [left, right] -> _Expresssion
	#operator -> Token class defined in lexer.py which has 4 properties: token_type, lexeme, literal, value
	def __init__(self, left, operator, right):
		self.left = left
		self.right = right
		self.operator = operator

	def linkVisitor(self, visitor):
		return visitor.visitBinaryExpression(self)

	# def print(self):
	# 	return f'({self.operator.lexeme} {self.left.print()} {self.right.print()})'

class UnaryExpression:
	def __init__(self, operator, right):
		self.right =right
		self.operator = operator

	def linkVisitor(self, visitor):
		return visitor.visitUnaryExpression(self)

	# def print(self):
	# 	return f'({self.operator.lexeme} {self.right.print()})'

class GroupingExpression:
	def __init__(self, expression):
		self.expression = expression 

	def linkVisitor(self, visitor):
		return visitor.visitGroupingExpression(self)

	# def print(self):
	# 	return f'({self.expression.print()})'

class LiteralExpression:
	def __init__(self, expr):
		self.expr = expr
		self.value = expr.literal #this is just for number, string only 

	def linkVisitor(self, visitor):
		return visitor.visitLiteralExpression(self)

	# def print(self):
	# 	return str(self.value)
class Calculator(ExpressionVisitor):
	def __init__(self, environment):
		self.environment = environment

	def calculate(self, expr):
		return expr.linkVisitor(self)

	def visitBinaryExpression(self, binary_expression):
		left_expr = self.calculate(binary_expression.left)
		operator = binary_expression.operator
		right_expr = self.calculate(binary_expression.right)


		if (operator.lexeme == TokenType.PLUS.value):
			return left_expr + right_expr
		if (operator.lexeme == TokenType.MINUS.value):
			return left_expr - right_expr
		if (operator.lexeme == TokenType.STAR.value):
			return left_expr * right_expr
		if (operator.lexeme == TokenType.SLASH.value):
			return left_expr / right_expr


		if (operator.lexeme == TokenType.EQUAL_EQUAL.value):
			return left_expr == right_expr
		if (operator.lexeme == TokenType.BANG_EQUAL.value):
			return left_expr != right_expr
		if (operator.lexeme == TokenType.GREATER.value):
			return left_expr > right_expr
		if (operator.lexeme == TokenType.GREATER_EQUAL.value):
			return left_expr >= right_expr
		if (operator.lexeme == TokenType.LESS.value):
			return left_expr < right_expr
		if (operator.lexeme == TokenType.LESS_EQUAL.value):
			return left_expr <= right_expr

	def visitUnaryExpression(self, unary_expression):
		operator = unary_expression.operator
		expr     = self.calculate(unary_expression.right)
		if (operator.lexeme == TokenType.PLUS.value):
			return expr
		if (operator.lexeme == TokenType.MINUS.value):
			return - expr 
		if (operator.lexeme == TokenType.BANG.value):
		    return not expr

	def visitLiteralExpression(self, literal_expression):
		if (literal_expression.expr.tipe == TokenType.TRUE):
			return True
		elif (literal_expression.expr.tipe == TokenType.FALSE):
			return False
		#to do : add case for identifier variable, function call ...etc
		elif (literal_expression.expr.tipe == TokenType.IDENTIFIER):
			return self.environment.get(literal_expression.expr.literal)

		return literal_expression.value

class ASTPrinter:
	#statement are enclosed in <>
	def print(self, entity):
		return entity.linkVisitor(self)

	def visitBlockStatement(self, block_statement):
		ret_val = block_statement.name + "{\n"
		for statement in block_statement.statements:
			ret_val += self.print(statement) + '\n'
		ret_val += '}'
		return ret_val

	def visitAssignmentStatement(self, statement):
		#below statement.lvalue.literal is used since statement.lvalue.lexeme contains entire alphanumeric characters
		ret_val = f"{statement.name} {statement.lvalue.literal}, {self.print(statement.rvalue)}"
		return ret_val

	def visitReassignmentStatement(self, statement):
		return self.visitAssignmentStatement(statement)

	def visitPrintStatement(self, statement): 
		# print('AST')
		ret_val  = f"{statement.name} {self.print(statement.expr)}"
		# print(ret_val)
		return ret_val

	def visitExprStatement(self, statement):
		return f"{statement.name} {self.print(statement.expr)}"

	def visitBinaryExpression(self, binary_expression):
		return self.parenthesize(binary_expression.operator.lexeme,
								binary_expression.left,
								binary_expression.right)

	def visitGroupingExpression(self, grouping_expression):
		return self.parenthesize('group',
								grouping_expression.expression)

	def visitUnaryExpression(self, unary_expression):
		return self.parenthesize(unary_expression.operator.lexeme,
								unary_expression.right)

	def visitLiteralExpression(self, literal_expression):
		if (literal_expression.expr.tipe in [TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER]):
			return str(literal_expression.value)
		return literal_expression.expr.lexeme


	def parenthesize(self, operator, *expressions):
		recursive_values =  ' '.join([expression.linkVisitor(self) for expression in expressions])
		return f"({operator} {recursive_values})"

from lexer import TokenType, Scanner
class Parser:
	def __init__(self, token_list):
		self.token_list = token_list
		self.current = 0
		self.interpreter = None
		self.AST = [] # list of statements 

	def parse(self):
		self.AST = self.parseProgram()

	def parseProgram(self): #returns list statements
		AST = []
		while (self.peek().tipe != TokenType.EOF):
			statement = self.parseStatement()
			if (self.peek().tipe == TokenType.SEMICOLON):
				self.advance()#consume the semicolon
				AST.append(statement)
			else:
				raise Exception('statement is not terminated by semicolon', statement)
		return AST 

	def parseStatement(self):
		#variable statement
		#print statement 
		#expression statement, reassignment statement
		#block statement

		#variable statement
		if (self.peek().tipe == TokenType.VAR):
			self.advance() # consume the var keyword
			#var must be initialized with value mandatorily
			lvalue = self.advance()
			if (self.peek().tipe == TokenType.EQUAL):
				self.advance() # consume the equal sign
				rvalue = self.parseExpr()
				assignment_statement = AssignmentStatement(lvalue, rvalue)
				return assignment_statement
			else:
				raise Exception('var keyword must be followed by identifier, equals sign and a mandatory rvalue')

		#block statement
		if(self.peek().tipe == TokenType.LEFT_BRACE):
			left_brace = self.advance() # consume the left brace
			statements = []
			while (self.peek().tipe != TokenType.RIGHT_BRACE):
				if (self.peek().tipe == TokenType.EOF):
					raise Exception(f'Block statement not terminated by matching brace at line {left_brace.line}')
				
				statement = self.parseStatement()
				#look for ; in the next token
				if (self.peek().tipe == TokenType.SEMICOLON):
					self.advance() # consumet the semicolon
					statements.append(statement)
				else:
					raise Exception(f'->statement not terminated at line {self.peek().line}')

			self.advance() # consume the right brace
			return BlockStatement(statements)
			

		# print statement
		if (self.peek().tipe == TokenType.PRINT): 
		    p_statement = self.advance()#not actually required, we can discard this value
		    expr = self.parseExpr()
		    # print('expr ', expr, expr.value)
		    return PrintStatement(expr)
		# the following handles expression statement as well as reassignment statement
		else:
			lvalue = self.parseExpr()
			if (self.peek().tipe == TokenType.EQUAL): # this is reassignment statement
			    if (lvalue.expr.tipe == TokenType.IDENTIFIER): #check if the lvalue is assignable variable
			         self.advance() # consume the equal sign
			         rvalue = self.parseExpr()
			         return ReassignmentStatement(lvalue.expr, rvalue) # lvalue.expr because self.parseExpr() return LiteralExpresion whose expr property contains the actual token
			    else:
			    	raise Exception("non assignable target")
			else: #if there is no equlity sign then it must be expression statement 
			    return ExprStatement(lvalue)

	def parseExpr(self):
		return self.comparisonExpr()

	def comparisonExpr(self):
		left_expr = self.additionExpr()

		if  (self.peek().tipe in [TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL,
			                      TokenType.GREATER, TokenType.GREATER_EQUAL,
			                      TokenType.LESS, TokenType.LESS_EQUAL]):
		    operator = self.advance() #consume the operator and move forward
		    right_expr = self.comparisonExpr()
		    return BinaryExpression(left_expr, operator, right_expr)
		return left_expr

	def additionExpr(self):
		left_expr = self.multiplicationExpr()

		if(self.peek().tipe in [TokenType.PLUS, TokenType.MINUS]):
			operator = self.advance()
			right_expr = self.additionExpr()
			return BinaryExpression(left_expr, operator, right_expr)
		
		return left_expr

		
	def multiplicationExpr(self):
		left_expr = self.unitaryExpr()
		if (self.peek().tipe in [TokenType.STAR, TokenType.SLASH]):
			operator = self.advance() #consume the operator
			right_expr = self.multiplicationExpr()
			return BinaryExpression(left_expr, operator, right_expr)
		return left_expr


	def unitaryExpr(self):
		if (self.peek().tipe in [TokenType.BANG, TokenType.MINUS, TokenType.PLUS]):
			operator = self.advance() # advance the operator
			return UnaryExpression(operator, self.literalExpr())
		
		return self.literalExpr()

	def literalExpr(self): # this needs to add support for bracketed expr or(group expression) as they have the same precedence as the literal number
	    if (self.peek().tipe in [TokenType.STRING, TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.TRUE, TokenType.FALSE]):
	    	literal_expr = self.advance()
	    	return LiteralExpression(literal_expr)
	    elif (self.peek().tipe == TokenType.LEFT_PAREN):
	    	self.advance() # consume the '(' token
	    	group_expr = self.parseExpr()
	    	if (self.peek().tipe == TokenType.RIGHT_PAREN):
	    		self.advance() # consume the ')' token
	    		return group_expr
	    	else:
	    		print('error no matching parenthesis found') #exception needs to be raised here

	def advance(self):
		self.current += 1
		return self.token_list[self.current - 1]

	def reverse(self):
		return self.token_list[self.current - 1]

	def peek(self):
		return self.token_list[self.current] if not self.isAtEnd() else TokenType.EOF

	def peekAndMatch(self, match_token):
		if (self.peek() == match_with_token):
			self.advance()
			return True
		return False

	def peekAndMatchMultiple(self, *match_tokens):
		return any(map(self.peekAndMatch, match_tokens))

	def isAtEnd(self):
		return self.current >= len(self.token_list)#check the type of the end item



def test_printer():
	from lexer import TokenType, Token

	new_expr = BinaryExpression(
		            UnaryExpression(Token(TokenType.MINUS), 
		            				LiteralExpression(123)),
		            Token(TokenType.STAR),

		            GroupingExpression(LiteralExpression(45.67))
		            )
	# new_expr = LiteralExpression(234)
	print(ASTPrinter().print(new_expr))

def test_lexer(source_code='2+2*2'):

	scanner = Scanner(source_code)
	scanner.scanTokens()
	for tkn in scanner.token_list:
		print(tkn.toString())

	parser = Parser(scanner.token_list)
	parser.parse()

	print(ASTPrinter().print(parser.AST))


def test_parser(source_code='2+2*2; print (2 + (3*3+3)'):
	scanner = Scanner(source_code)
	scanner.scanTokens()
	# print(scanner.toString())


	parser = Parser(scanner.token_list)
	parser.parse()
	# print(parser.AST)
	# print(ASTPrinter().print(parser.AST[0]))
	# print(ASTPrinter().print(parser.AST[1]))
	for AST in parser.AST:
		print(ASTPrinter().print(AST))

	print('------')
	for AST in parser.AST:
		StatementExecutor().execute(AST)
	print('------')

from environment import Environment
def test_parser_assignment_statement(source_code='var a = 23; a = 10; print a;'):
	scanner = Scanner(source_code)
	scanner.scanTokens()
	# print(scanner.toString())


	parser = Parser(scanner.token_list)
	parser.parse()
	# print(parser.AST)
	# print(ASTPrinter().print(parser.AST[0]))
	# print(ASTPrinter().print(parser.AST[1]))
	print('------')
	for AST in parser.AST:
		print(ASTPrinter().print(AST))

	print('------')
	env = Environment()
	for AST in parser.AST:
		StatementExecutor(env).execute(AST)

	
def test_parser_block_statement(source_code='{ a = 10; print a; };'):
	scanner = Scanner(source_code)
	scanner.scanTokens()
	# print(scanner.toString())


	parser = Parser(scanner.token_list)
	parser.parse()
	# print(parser.AST)
	# print(ASTPrinter().print(parser.AST[0]))
	# print(ASTPrinter().print(parser.AST[1]))
	print('------')
	for AST in parser.AST:
		print(ASTPrinter().print(AST))

	print('------')
	env = Environment()
	for AST in parser.AST:
		StatementExecutor(env).execute(AST)