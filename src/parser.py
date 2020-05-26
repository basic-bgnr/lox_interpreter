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

class UnaryExpression:
	def __init__(self, operator, right):
		self.right =right
		self.operator = operator

	def linkVisitor(self, visitor):
		return visitor.visitUnaryExpression(self)

class GroupingExpression:
	def __init__(self, expression):
		self.expression = expression 

	def linkVisitor(self, visitor):
		return visitor.visitGroupingExpression(self)

class LiteralExpression:
	def __init__(self, value):
		self.value = value

	def linkVisitor(self, visitor):
		return visitor.visitLiteralExpression(self)


class ASTPrinter(ExpressionVisitor):

	def print(self, expr):
		return expr.linkVisitor(self)

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
		return str(literal_expression.value)

	def parenthesize(self, operator, *expressions):
		
		recursive_values =  ''.join([expression.linkVisitor(self) for expression in expressions])
		return f"({operator} {recursive_values})"

def test():
	from lexer import TokenType, Token

	new_expr = BinaryExpression(
		            UnaryExpression(Token(TokenType.MINUS), 
		            				LiteralExpression(123)),
		            Token(TokenType.STAR),

		            GroupingExpression(LiteralExpression(45.67))
		            )
	# new_expr = LiteralExpression(234)
	print(ASTPrinter().print(new_expr))

