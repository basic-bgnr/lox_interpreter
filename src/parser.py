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
class ReturnException(Exception):
    def __init__(self, ret_value, message="return value of function"):
        self.message = message
        self.ret_value = ret_value 
        super().__init__(self.message)
#########################native function call ##################

class CallableFunction:
    def __init__(self):
        pass
    def register(self, name, environment):
        pass
    def arity(self):
        pass 
    def call(self, args, resolver=None):
        pass
    

class NativeTimer(CallableFunction):
    
    def __init__(self):
        import time
        self.func = time.time_ns
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, args, resolver=None):
        return self.func()


class Exit(CallableFunction):
    
    def __init__(self):
        import sys
        self.func = sys.exit
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 1
        
    def call(self, *args, resolver=None):
        #head scratcher, arguments for sys.exit function must be of type int, i was using floats
        return self.func(int(args[0] if args else 0))

class Str(CallableFunction):
    def __init__(self):
        self.func = str
        self.name = ''

    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)
    def arity(self):
        return 1

    def call(self, args, resolver=None):
        return self.func(args[0] if args else "")


class Random(CallableFunction):
    
    def __init__(self):
        import random
        self.func = random.random
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, args, resolver=None):
        return self.func()

class Array(CallableFunction):
    
    def __init__(self):
        import random
        self.func = list
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        return self.func(args)

class InsertAt(CallableFunction):
    
    def __init__(self):
        import random
        self.func = None
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        arg_one = args[0] #array object
        arg_two = int(args[1]) #index
        arg_three = args[2] # new object
        arg_one[arg_two] = arg_three
        # return self.func(args)

class DeleteAt(CallableFunction):
    
    def __init__(self):
        import random
        self.func = None
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        arg_one = args[0] #array object
        arg_two = int(args[1]) #index
        del arg_one[arg_two]
        # return self.func(args)

class At(CallableFunction):
    
    def __init__(self):
        import random
        self.func = None
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        arg_one = args[0] #array object
        arg_two = int(args[1]) #index
        return arg_one[arg_two]

class Len(CallableFunction):
    
    def __init__(self):
        import random
        self.func = len
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        return self.func(args[0])
########################################################
######################lox_fuction#######################
class LoxFunction(CallableFunction):
    # params_list is list of tokens
    def __init__(self, function_statement):
        self.function_statement = function_statement
        #token.literal is variable name
        
        # print(f'inside lox function -> {self.environment.hashmap}, {executor.environment.hashmap}')

    def call(self, args, resolver):
         
        call_environment = Environment(self.environment)

        for param, arg in zip(self.function_statement.params_list, args):
            try:
                index = resolver.variable_location[param]
                call_environment.putAt(param.expr.literal, arg, index)
            except KeyError:
                call_environment.put(param.expr.literal, arg)

            


        
        ##### make self available in call environment, referring to itself
        # print('call ', TokenType.THIS.value, self)
        call_environment.put(TokenType.THIS.value, self)
        
        #####


        # print(f'inside lox call function -> {self.environment.hashmap}, {self.executor.environment.hashmap}')
        #creates a new execution context
        executor = StatementExecutor(call_environment, resolver)
        
        try:
            executor.execute(self.function_statement.block_statement)
        except ReturnException as e:
            return e.ret_value

        # print(closure_environment)

    def register(self, environment):
        self.environment = environment
        self.environment.put(self.function_statement.function_identifier_expression.expr.literal, self,)

    def arity(self):
        pass 

########################################################
class FunctionStatement:
    def __init__(self, function_identifier_expression, params_list, block_statement):
        self.function_identifier_expression = function_identifier_expression
        self.params_list = params_list #list of token
        self.block_statement = block_statement #BlockStatement

        self.name = "<function>"

    def linkVisitor(self, visitor):
        return visitor.visitFunctionStatement(self)

class ReturnStatement:
    def __init__(self, expr):
        self.expr = expr
        self.name = f"<return>"

    def linkVisitor(self, visitor):
        return visitor.visitReturnStatement(self)

class WhileStatement:
    def __init__(self, expression, block_statement):
        self.expression = expression
        self.block_statement = block_statement
        self.name = f"<while>"

    def linkVisitor(self, visitor):
        return visitor.visitWhileStatement(self)

class IfStatement:
    def __init__(self, expression, if_block_statement, else_block_statement=None):
        self.expression = expression
        self.if_block_statement = if_block_statement
        self.else_block_statement = else_block_statement

        self.name1 = f"<if>"
        self.name2 = f"<else>"

    def linkVisitor(self, visitor):
        return visitor.visitIfStatement(self)

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

from environment import Environment
class StatementExecutor:
    def __init__(self, environment, resolver):
        self.environment = environment
        self.resolver = resolver

    def execute(self, statement):
        statement.linkVisitor(self)

    def visitReturnStatement(self, return_statement):
        calculator = Calculator(self.environment, self.resolver)
        ret_value = calculator.calculate(return_statement.expr)
        raise ReturnException(ret_value)

    def visitFunctionStatement(self, function_statement):
        lox_function = LoxFunction(function_statement)
        lox_function.register(self.environment) #function is registered one time only when executing the AST


    def visitWhileStatement(self, while_statement):
        calculator= Calculator(self.environment, self.resolver)
        while (cond := calculator.calculate(while_statement.expression)):
            # print(ASTPrinter().print(while_statement.expression))
            self.execute(while_statement.block_statement)
            # input()

    def visitIfStatement(self, if_statement):
        calculator = Calculator(self.environment, self.resolver)

        if (calculator.calculate(if_statement.expression)):
            self.execute(if_statement.if_block_statement)
        elif(if_statement.else_block_statement):
            # print('inside else block {}')
            self.execute(if_statement.else_block_statement)

    def visitBlockStatement(self, block_statement):
        block_executor = StatementExecutor(Environment(parent=self.environment), self.resolver)
        for statement in block_statement.statements:
            block_executor.execute(statement)

    def visitAssignmentStatement(self, statement):
        calc = Calculator(self.environment, self.resolver)
        lvalue = statement.lvalue.expr.literal #get the name of the varible #this
        rvalue = calc.calculate(statement.rvalue)
        # print("-->  ", self.resolver.variable_location)
        # print(statement.lvalue)
        try:
            index = self.resolver.variable_location[statement.lvalue]
            self.environment.putAt(lvalue, rvalue, index)
        except KeyError:
            self.environment.put(lvalue, rvalue)

        

    def visitReassignmentStatement(self, statement):
        calc = Calculator(self.environment, self.resolver)
        lvalue = statement.lvalue.expr.literal #get the name of the varible # this 
        rvalue = calc.calculate(statement.rvalue)
        # self.environment.putIfExists(lvalue, rvalue)
        try:
            index = self.resolver.variable_location[statement.lvalue]
            self.environment.putAt(lvalue, rvalue, index)
        except KeyError:
            self.environment.put(lvalue, rvalue)
        
        #print(f'inside statement executor statements {statement.rvalue}   {statement.lvalue}')
        #print(f'inside statement executor {lvalue} -> {rvalue}')


    def visitPrintStatement(self, statement):
        print_object = Calculator(self.environment, self.resolver).calculate(statement.expr)
        # print(type(print_object), " len ", len(print_object))
        print(print_object)

    def visitExprStatement(self, statement):
        Calculator(self.environment, self.resolver).calculate(statement.expr)

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
    #   return f'({self.operator.lexeme} {self.left.print()} {self.right.print()})'

class UnaryExpression:
    def __init__(self, operator, right):
        self.right =right
        self.operator = operator

    def linkVisitor(self, visitor):
        return visitor.visitUnaryExpression(self)

    # def print(self):
    #   return f'({self.operator.lexeme} {self.right.print()})'
class FunctionExpression:
    def __init__(self, caller_expr, args):
        self.caller_expr = caller_expr
        self.args = args

    def linkVisitor(self, visitor):
        return visitor.visitFunctionExpression(self)

class GroupingExpression:
    def __init__(self, expression):
        self.expression = expression 

    def linkVisitor(self, visitor):
        return visitor.visitGroupingExpression(self)

    # def print(self):
    #   return f'({self.expression.print()})'

class LiteralExpression:
    def __init__(self, expr):
        self.expr = expr
        self.value = expr.literal #this is just for number, string only 

    def linkVisitor(self, visitor):
        return visitor.visitLiteralExpression(self)

    # def print(self):
    #   return str(self.value)
from ASTPrinter import ASTPrinter
class Calculator(ExpressionVisitor):
    def __init__(self, environment, resolver):
        self.environment = environment
        self.resolver = resolver

    def calculate(self, expr):
        return expr.linkVisitor(self)

    def visitFunctionExpression(self, function_expression):
        caller_expr = self.calculate(function_expression.caller_expr)
        # print("function expr ", caller_expr, " ", type(caller_expr), " ", isinstance(caller_expr, CallableFunction))
        if (isinstance(caller_expr, CallableFunction)):
            ret = caller_expr.call(*[self.calculate(arg) for arg in function_expression.args], resolver=self.resolver)
            return ret

        raise Exception('non function called')

    def visitBinaryExpression(self, binary_expression):
        # to do(completed): clean up the following conditional check about `lexeme` and replacement with `operator == TokenType.[PLUS, MINUS.....] directly
        left_expr = self.calculate(binary_expression.left)
        operator = binary_expression.operator
        right_expr = self.calculate(binary_expression.right)

        #print(f'inside calculator BinaryExpression {left_expr} and {right_expr}')

        if (operator.tipe == TokenType.AND):
            return left_expr and right_expr
        if (operator.tipe == TokenType.OR):
            return left_expr or right_expr


        if (operator.tipe == TokenType.PLUS):
            return left_expr + right_expr
        if (operator.tipe == TokenType.MINUS):
            return left_expr - right_expr
        if (operator.tipe == TokenType.STAR):
            return left_expr * right_expr
        if (operator.tipe == TokenType.SLASH):
            return left_expr / right_expr


        if (operator.tipe == TokenType.EQUAL_EQUAL):
            return left_expr == right_expr
        if (operator.tipe == TokenType.BANG_EQUAL):
            return left_expr != right_expr
        if (operator.tipe == TokenType.GREATER):
            return left_expr > right_expr
        if (operator.tipe == TokenType.GREATER_EQUAL):
            return left_expr >= right_expr
        if (operator.tipe == TokenType.LESS):
            return left_expr < right_expr
        if (operator.tipe == TokenType.LESS_EQUAL):
            return left_expr <= right_expr

    def visitUnaryExpression(self, unary_expression):
        operator = unary_expression.operator
        expr     = self.calculate(unary_expression.right)
        if (operator.tipe == TokenType.PLUS):
            return expr
        if (operator.tipe == TokenType.MINUS):
            return - expr 
        if (operator.tipe == TokenType.BANG):
            return not expr

    def visitLiteralExpression(self, literal_expression):
        if (literal_expression.expr.tipe == TokenType.TRUE):
            return True
        elif (literal_expression.expr.tipe == TokenType.FALSE):
            return False
        #to do : add case for identifier variable, function call ...etc
        elif (literal_expression.expr.tipe in [TokenType.IDENTIFIER, TokenType.THIS] ):
            # return self.environment.get(literal_expression.expr.literal)
            # print("->>> ", ASTPrinter().print(literal_expression))
            try:
                index = self.resolver.variable_location[literal_expression]
                return self.environment.getAt(literal_expression.expr.literal, index)
            except KeyError:
                return self.environment.get(literal_expression.expr.literal)

        return literal_expression.value




from lexer import TokenType, Scanner, Token
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
        self.setCurrentAST(AST)
        while (self.peek().tipe != TokenType.EOF):
            #this is executed every loop so as to prevent indirection to other intermediate AST list 
            statement = self.parseStatement()
            if (self.peek().tipe == TokenType.SEMICOLON):
                self.advance()#consume the semicolon
                AST.append(statement)
            else:
                raise Exception(f'statement is not terminated by semicolon at line {self.peek().line}')
        return AST 

    def parseStatement(self):
        #variable statement
        #print statement 
        #expression statement, reassignment statement
        #block statement
        #if statement

        if (variable_statement := self.variableStatement()):
            return variable_statement

        # important if you're looking for anon function 
        if (block_statement := self.blockStatement()):
            return block_statement

        if (if_statement := self.ifStatement()):
            return if_statement

        if (print_statement := self.printStatement()):
            return print_statement

        if (while_statement := self.whileStatement()):
            return while_statement

        if(return_statement := self.returnStatement()):
            return return_statement

        if (function_statement := self.functionStatement()):
            return function_statement

        if (expression_statement := self.expressionStatement()):
            return expression_statement

        raise Exception(f'Invalid statement at line {self.peek().line}')


    def functionStatement(self):
        #the following conditional checks if it's normal function statement or anon function expression
        #if identifier is provided after `fun` its function statement 
        if(self.peek().tipe == TokenType.FUN and self.peekNext().tipe == TokenType.IDENTIFIER):
            function_token = self.advance() # consume the fun token 
            function_identifier_expression = LiteralExpression(self.advance())
            left_paren = self.advance()
            params_list = []
            if (self.peek().tipe == TokenType.IDENTIFIER): #handles case of zero argument
                arg = self.advance()
                params_list.append(LiteralExpression(arg))

            while(self.peek().tipe != TokenType.RIGHT_PAREN):
                if (self.peek().tipe == TokenType.EOF):
                    raise Exception(f"parenthesis is not terminated by matching parenthesis at line # {left_paren.line}")
                
                if(self.peek().tipe == TokenType.COMMA):
                    self.advance() # consume comma
                    if (self.peek().tipe == TokenType.IDENTIFIER):
                        arg = self.advance()
                        params_list.append(LiteralExpression(arg))
                    else:
                        raise Exception('function parameter must be identifier')
                else:
                    raise Exception(f"function argument must be separated by comma at line # {self.peek().line}")

            self.advance()# consume right paren

            block_statement = self.blockStatement()

            return FunctionStatement(function_identifier_expression, params_list, block_statement)


    def variableStatement(self):
        #variable statement
        if (self.peek().tipe == TokenType.VAR):
            self.advance() # consume the var keyword
            #var must be initialized with value mandatorily
            lvalue = self.parseExpr() #self.advance()
            # print(f'variableStatement -> {ASTPrinter().print(lvalue)}')
            if (self.peek().tipe == TokenType.EQUAL):
                self.advance() # consume the equal sign
                rvalue = self.parseExpr()
                # print(f'variableStatement -> {ASTPrinter().print(rvalue)}')
                assignment_statement = AssignmentStatement(lvalue, rvalue)
                return assignment_statement
            else:
                raise Exception('var keyword must be followed by identifier, equals sign and a mandatory rvalue')

    def returnStatement(self):
        if (self.peek().tipe == TokenType.RETURN):
            return_keyword = self.advance()
            if (ret_expr := self.parseExpr()):
                return ReturnStatement(ret_expr)

    def blockStatement(self):
        #anon function requiremnt, whenever you enter a block get a reference to parent AST and at the end 
        #setthe current AST to this parent ast

        parent_ast = self.getCurrentAST()
        #block statement
        if(self.peek().tipe == TokenType.LEFT_BRACE):
            left_brace = self.advance() # consume the left brace
            statements = []
            
            self.setCurrentAST(statements)#useful for anon function 

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
            #setting current AST to be the parent ast  
            self.setCurrentAST(parent_ast)
            return BlockStatement(statements)

    def printStatement(self):
        # print statement
        if (self.peek().tipe == TokenType.PRINT): 
            p_statement = self.advance()#not actually required, we can discard this value
            expr = self.parseExpr()
            # print('expr ', expr, expr.value)
            return PrintStatement(expr)
        # the following handles expression statement as well as reassignment statement

    def expressionStatement(self):
        lvalue = self.parseExpr()
        if (self.peek().tipe in [TokenType.EQUAL, TokenType.MINUS_EQUAL, TokenType.PLUS_EQUAL, TokenType.STAR_EQUAL, TokenType.SLASH_EQUAL]): # this is reassignment statement
            if (lvalue.expr.tipe == TokenType.IDENTIFIER): #check if the lvalue is assignable variable
                operator = self.advance() # consume the sign
                rvalue = self.parseExpr()
                if (operator.tipe == TokenType.EQUAL):
                    return ReassignmentStatement(lvalue, rvalue)
                ### the following procedure replaces the double token with their equivalent single token operator and at the 
                ### end carry out syntactic operation of binaryExpression and return it as
                if (operator.tipe == TokenType.PLUS_EQUAL):
                    operator.tipe = TokenType.PLUS 

                if (operator.tipe == TokenType.MINUS_EQUAL):
                    operator.tipe = TokenType.MINUS 

                if (operator.tipe == TokenType.STAR_EQUAL):
                    operator.tipe = TokenType.STAR

                if (operator.tipe == TokenType.SLASH_EQUAL):
                    operator.tipe = TokenType.SLASH

                syntactic_expression  = BinaryExpression(lvalue, operator, rvalue)
                return ReassignmentStatement(lvalue, syntactic_expression)
            else:
                raise Exception("non assignable target")
        else: #if there is no equlity sign then it must be expression statement 
            return ExprStatement(lvalue)

    def ifStatement(self):
        if (self.peek().tipe == TokenType.IF):
            self.advance() #consume the 'if' token
            expression = self.parseExpr()
            if (if_block_statement := self.blockStatement()):
                if (self.peek().tipe == TokenType.ELSE):
                    self.advance() # consume the 'else' token
                    if else_block_statement := self.blockStatement():
                        return IfStatement(expression, if_block_statement, else_block_statement)
                    else:
                        raise Exception(f"else statement must be followed by matching braces at line {self.peek().line}")
                else:
                    return IfStatement(expression, if_block_statement)
            else:
                raise Exception(f"if statement must be followed by matching braces at line {self.peek().line}")

    def whileStatement(self):
        if (self.peek().tipe == TokenType.WHILE):
            self.advance() # consume the `while` token
            expression = self.parseExpr()
            if (block_statement := self.blockStatement()):
                return WhileStatement(expression, block_statement)
            else:
                raise Exception(f"while statement must be followed by matching braces at line {self.peek().line}")

    def parseExpr(self):
        return self.logicalExpr()

    def logicalExpr(self):
        left_expr = self.comparisonExpr()
        if (self.peek().tipe in [TokenType.AND, TokenType.OR]):
            operator = self.advance() #return `and` or `or`
            right_expr = self.logicalExpr()
            return BinaryExpression(left_expr, operator, right_expr)
        return left_expr

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
        
        return self.functionExpr()

    def functionExpr(self):
        #################################
        def argument_list():
            args = []
            if (arg:= self.parseExpr()):
                args.append(arg)
            while(self.peek().tipe != TokenType.RIGHT_PAREN):
                if (self.peek().tipe == TokenType.EOF):
                    raise Exception(f"no matching parenthesis at line {left_paren.line}")
                if (self.peek().tipe == TokenType.COMMA):
                    self.advance()#consume the comma
                    arg = self.parseExpr()
                    args.append(arg)
            self.advance() # consume the right parenthesis
            return args
        ##################################
        caller_expr = self.literalExpr()
        while (True): 
            if (self.peek().tipe == TokenType.LEFT_PAREN):
                left_paren = self.advance()
                args = argument_list()
                caller_expr = FunctionExpression(caller_expr, args)
            else:
                break
        

        return caller_expr
    ############the folllowing function is defined in order to facilitate AST manipulation for anon function 
    def getCurrentAST(self):
        return self.current_AST

    def setCurrentAST(self, current_AST):
        self.current_AST = current_AST
    ######################################################


    def literalExpr(self): # this needs to add support for bracketed expr or(group expression) as they have the same precedence as the literal number
        if (anon_function  := self.anonFunctionExpr()):
            return anon_function
        if (self.peek().tipe in [TokenType.STRING, TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.TRUE, TokenType.FALSE, TokenType.THIS]):
            literal_expr = self.advance()
            # print('literalExpr ', literal_expr.literal)
            return LiteralExpression(literal_expr)
        elif (self.peek().tipe == TokenType.LEFT_PAREN):
            self.advance() # consume the '(' token
            group_expr = self.parseExpr()
            if (self.peek().tipe == TokenType.RIGHT_PAREN):
                self.advance() # consume the ')' token
                return group_expr
            else:
                Exception(f'error no matching parenthesis found at {self.peek().line}') #exception needs to be raised here

    def anonFunctionExpr(self): # anon function declaration expression
        # To do: needs to check user program for error in the following code 
        if(self.peek().tipe == TokenType.WALL):
            function_token = self.advance() # consume the wall token 
            #this is an anonymous function declaration
            function_identifier_token = Token(TokenType.IDENTIFIER, lexeme='', literal='', line=function_token.line)
            function_identifier_token.literal = f"@{hash(function_identifier_token)}" # generate unique id for anonyous function
            function_identifier_expression = LiteralExpression(function_identifier_token)
            
            params_list = []
            if (self.peek().tipe == TokenType.IDENTIFIER): #handles case of zero argument
                arg = self.advance()
                params_list.append(LiteralExpression(arg))

            while(self.peek().tipe != TokenType.WALL):
                if (self.peek().tipe == TokenType.EOF):
                    raise Exception(f"parenthesis is not terminated by matching parenthesis at line # {left_paren.line}")
                
                if(self.peek().tipe == TokenType.COMMA):
                    self.advance() # consume comma
                    if (self.peek().tipe == TokenType.IDENTIFIER):
                        arg = self.advance()
                        params_list.append(LiteralExpression(arg))
                    else:
                        raise Exception('function parameter must be identifier')
                else:
                    raise Exception(f"function argument must be separated by comma at line # {self.peek().line}")

            self.advance()# consume right paren

            block_statement = self.blockStatement()

            # self.AST.append(FunctionStatement(function_identifier_token, params_list, block_statement))
            #side effect
            function_statement = FunctionStatement(function_identifier_expression, params_list, block_statement)
            self.getCurrentAST().append(function_statement)
            #end side effect

            return function_identifier_expression


    def advance(self):
        self.current += 1
        return self.token_list[self.current - 1]

    def reverse(self):
        return self.token_list[self.current - 1]

    def peek(self):
        return self.token_list[self.current] if not self.isAtEnd() else TokenType.EOF

    def peekNext(self):
        return self.token_list[self.current+1] if not self.isAtEndWhere(n=self.current + 1) else TokenType.EOF


    def peekAndMatch(self, match_token):
        if (self.peek() == match_with_token):
            self.advance()
            return True
        return False

    def peekAndMatchMultiple(self, *match_tokens):
        return any(map(self.peekAndMatch, match_tokens))

    def isAtEnd(self):
        return self.current >= len(self.token_list)#check the type of the end item

    #temporary helper functoin to facilitate peekNext() function
    def isAtEndWhere(self, n):
        return n >= len(self.token_list)