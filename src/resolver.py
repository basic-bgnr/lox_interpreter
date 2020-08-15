
#the following class acts like a mini interpreter and perform static analysis of the plox code 
#as with general optimization compiler, after generating the AST, static analysis are performed
#in the form of pass(many passes are also possible) with specific function.
#For the first pass of optimization, the code below provides solution for lexical resolution of
#variables
#scope stack are only used for local scope, global scope is managed by statementExecutor class 
from collections import defaultdict
from lexer import TokenType
from ASTPrinter import ASTPrinter
from parser import LiteralExpression
class Resolver: 
    def __init__(self):
        self.scope_stack = [{}] 
        self.variable_location = {} #key pair, variable: stack_depth
        


    def peekStack(self):
        return self.scope_stack[-1]

    def isStackEmpty(self):
        return len(self.scope_stack) == 0

    def resolve(self, statement):
        # print('entering  ', ASTPrinter().print(statement))
        statement.linkVisitor(self)

    def resolveAll(self, statements):
        for statement in statements:
            self.resolve(statement)

    def beginScope(self):
        #scope_stack # placeholder for variable defined within a scope, true = present, false = absent, default=absent
        self.scope_stack.append({})

    def endScope(self):
        return self.scope_stack.pop()


    def define(self, name):
        self.peekStack()[name] = True

    def visitGetExpression(self, get_expression):
        self.resolve(get_expression.obj) # this just transverses the get_expression

    def visitClassStatement(self, class_statement):
        #first define it so that we can use it within itself
        self.define(class_statement.class_identifier_expression.expr.literal)
        self.resolve(class_statement.class_identifier_expression)
        

    def visitBlockStatement(self, block_statement):
        # print('entering block')
        # print(f'------------ ')
        # print(self.scope_stack)
        # print('----------->')
        self.beginScope()
        for statement in block_statement.statements:
            self.resolve(statement)
        self.endScope()
        # print(f'------------ ')
        # print(self.scope_stack)
        # print('----------->')
        # print('exiting block')

    def visitReturnStatement(self, return_statement):
        self.resolve(return_statement.expr) 
        
    def visitFunctionStatement(self, function_statement):
        # print('entering function')
        self.define(function_statement.function_identifier_expression.expr.literal)
        self.resolve(function_statement.function_identifier_expression)
        self.beginScope()
        # print(function_statement.params_list)
        for param in function_statement.params_list:
            self.define(param.expr.literal)
            self.resolve(param)
            
        self.resolve(function_statement.block_statement)
        self.endScope()
        # print('exiting function')

        
    def visitWhileStatement(self, while_statement):
        self.resolve(while_statement.expression)
        self.resolve(while_statement.block_statement) 

    def visitIfStatement(self, if_statement):
        self.resolve(if_statement.expression)
        self.resolve(if_statement.if_block_statement)
        if (else_block := if_statement.else_block_statement):
            self.resolve(else_block)
       
    def visitAssignmentStatement(self, assignment_statement):
        self.resolve(assignment_statement.rvalue)
        
        self.define(assignment_statement.lvalue.expr.literal)
        self.resolve(assignment_statement.lvalue) # this is called to store recently defined variable in the 
        #variable_location 
        
        
        # print('entering assignment ', self.scope_stack)
        
    def visitReassignmentStatement(self, reassignment_statement):
        self.resolve(reassignment_statement.rvalue)
        self.resolve(reassignment_statement.lvalue)
             
    def visitPrintStatement(self, print_statement):
        self.resolve(print_statement.expr)

    def visitExprStatement(self, expression_statement):
        self.resolve(expression_statement.expr) 

    def visitCallableExpression(self, callable_expression):
        self.resolve(callable_expression.caller_expr)
        for arg in callable_expression.args:
            self.resolve(arg)

    def visitBinaryExpression(self, binary_expression):
        # to do(completed): clean up the following conditional check about `lexeme` and replacement with `operator == TokenType.[PLUS, MINUS.....] directly
        self.resolve(binary_expression.left)
        self.resolve(binary_expression.right)


    def visitUnaryExpression(self, unary_expression):
        expr = unary_expression.right
        self.resolve(expr)

    def visitLiteralExpression(self, variable_expression):#variable_expression := literal_expression [number, string, identifier, true, false]
        if (variable_expression.expr.tipe == TokenType.IDENTIFIER):
            for (depth, stack_frame) in enumerate(self.scope_stack[-1::-1]):
                #we're concerned only with Identifier, literal number, boolean and string are not evaluated
                
                if (variable_expression.expr.literal in stack_frame.keys()):
                    self.variable_location[variable_expression] = depth #record the location of the variable in stack
                    return
            
                # raise Exception(f'undeclared variable used at {variable_expression.expr.line}')
            # raise Exception(f'undeclared variable used at {variable_expression.expr.line} {(variable_expression.expr.toString())}')

            #if none of the above match then the variable expression must be from global environment
            #runtime error is raised if the expression is not found

