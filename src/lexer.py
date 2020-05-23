def test(source_code = '{{(+)}}'):
	scanner = Scanner(source_code)
	scanner.scanTokens()
	print(scanner.toString())

class Scanner:
	def __init__(self, source_code):
		self.source_code = source_code
		self.token_list = []
		self.start = 0
		self.current = 0
		self.line   = 1

	# def getTokenizedList(self):
	# 	self.scanTokens()
	# 	return self.token_list

	def scanTokens(self):
		while(not self.isAtEnd()):
			self.start = self.current

			self.scanToken()

		#just for clarity
		#below line is indicative of the end of the souce_code
		self.addToken(TokenType.EOF)

	def isAtEnd(self):
		return self.current >= len(self.source_code)

	def scanToken(self):
		lexeme = self.advance()
		if (lexeme == TokenType.LEFT_PAREN.value):
		 	self.addToken(TokenType.LEFT_PAREN)

		elif (lexeme == TokenType.RIGHT_PAREN.value):
			self.addToken(TokenType.RIGHT_PAREN)

		elif (lexeme == TokenType.LEFT_BRACE.value):
			self.addToken(TokenType.LEFT_BRACE)

		elif (lexeme ==TokenType.RIGHT_BRACE.value):
			self.addToken(TokenType.RIGHT_BRACE)

		elif (lexeme == TokenType.COMMA.value):
			self.addToken(TokenType.COMMA)

		elif (lexeme == TokenType.DOT.value):
			self.addToken(TokenType.DOT)

		elif (lexeme == TokenType.MINUS.value):
			self.addToken(TokenType.MINUS)

		elif (lexeme == TokenType.PLUS.value):
			self.addToken(TokenType.PLUS)

		elif (lexeme == TokenType.SEMICOLON.value):
			self.addToken(TokenType.SEMICOLON)

		elif (lexeme == TokenType.STAR.value):
			self.addToken(TokenType.STAR)

		elif (lexeme == TokenType.COMMENT.value):
			#this is a comment and must be consumed till the end of line 
			while True:
				if (self.peek() not in [TokenType.NEW_LINE.value, TokenType.EOF.value]): #check for the newline or endoffile
					self.advance() #consume everything in between and loop till \n or \0
				else:
					break #if newline or eof found in self.peek()
				

		elif (lexeme in [TokenType.CARRIAGE_RETURN.value, TokenType.SPACE.value, TokenType.TAB.value]): #ignore any of the case of return feed, space and tab
			pass # do nothing and let it be consumed in the next cycle of scantokens function

		elif (lexeme == TokenType.NEW_LINE.value):
			self.line += 1


		#two character lexemes, here peek_and_match consumes the current token and forward if matched
		elif (lexeme == TokenType.BANG):
			self.addToken(TokenType.BANG_EQUAL) if self.peek_and_match(TokenType.EQUAL) else self.addToken(TokenType.BANG)

		elif (lexeme == TokenType.EQUAL):
			self.addToken(TokenType.EQUAL_EQUAL) if self.peek_and_match(TokenType.EQUAL) else self.addToken(TokenType.EQUAL)

		elif (lexeme == TokenType.LESS.value):
			self.addToken(TokenType.LESS_EQUAL) if self.peek_and_match(TokenType.EQUAL) else self.addToken(TokenType.LESS)

		elif (lexeme == TokenType.GREATER.value):
			self.addToken(TokenType.GREATER_EQUAL) if self.peek_and_match(TokenType.EQUAL) else self.addToken(TokenType.GREATER)

		else:
			#self.had_error
			#report the error to the interpreter but do not stop the parsing
			#determine other souce of error
			pass

	def peek_and_match(self, expected_lexeme):
		next_lexeme = self.peek()#peek the next value
		if (next_lexeme == expected_lexeme):
			self.advance()#consume the next value
			return True
		else:
			return False

	def peek(self):
		return TokenType.EOF.value if self.isAtEnd() else self.source_code[self.current]

	def advance(self):
		self.current += 1 
		# the reason why we add first and subtract later is to use the substring fuction in the addtoken function 
		# which require the end to +1'ed to get the full token
		# additionally also allows us to peek the next value without mutating or impuring the start and current variable
		return self.source_code[self.current-1]

	def addToken(self, token, literal=None):
		#the following code return multicharacter lexeme, that's why start and current is required
		#lexeme = self.source_code[self.start:self.current] if literal else literal #non printable character should have None as printable literal 
		lexeme = self.source_code[self.start:self.current]
		self.token_list.append(
			Token(token, 
				  lexeme,# the string corresponding to the token, it is necessary only for identifier other are redundant
				  literal, 
				  self.line)
			)

	def toString(self):
		return '  '.join(map(lambda x: x.toString(), self.token_list))


class Token:
	def __init__(self, tipe, lexeme, literal, line):
		self.tipe = tipe
		self.lexeme = lexeme
		self.literal = literal
		self.line = line

	def toString(self):
		return f'<{self.tipe} {self.lexeme} {self.literal} "{self.line}"''>'

from enum import Enum, auto
class TokenType(Enum):                                   
  ##Single-character tokens.                      
  LEFT_PAREN = '('
  RIGHT_PAREN = ')'
  LEFT_BRACE  = '{'
  RIGHT_BRACE = '}'
  COMMA =','
  DOT  = '.'
  MINUS = '-'
  PLUS = '+'
  SEMICOLON = ';'
  SLASH ='/'
  STAR = '*'
  NEW_LINE = '\n'

  #token to ignore
  TAB = '\t'
  SPACE = ' '
  CARRIAGE_RETURN = '\r'
  COMMENT = '#'


  ##One or two character tokens.                  
  BANG = '!'
  BANG_EQUAL = '!='                                
  EQUAL = '='
  EQUAL_EQUAL = '=='                              
  GREATER = '.'
  GREATER_EQUAL = '>='                          
  LESS = '<'
  LESS_EQUAL = '>='                                

  ##Literals.                                     
  IDENTIFIER  = auto()
  STRING = auto()
  NUMBER = auto()             

  ##Keywords.                                     
  AND = 'and'
  CLASS = 'class'
  ELSE = 'else'
  FALSE = 'false'
  FUN = 'fun'
  FOR = 'for'
  IF = 'if'
  NIL = 'nil'
  OR  = 'or'
  PRINT = 'print'
  RETURN = 'return'
  SUPER = 'super'
  THIS = 'this'
  TRUE = 'true'
  VAR = 'var'
  WHILE = 'while'

  EOF = '\0'