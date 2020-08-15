from parser import CallableExpression, LoxInstance

class NativeTimer(CallableExpression):
    
    def __init__(self):
        import time
        self.func = time.time_ns
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        return self.func()


class Exit(CallableExpression):
    
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

class Str(CallableExpression):
    def __init__(self):
        self.func = str
        self.name = ''

    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)
    def arity(self):
        return 1

    def call(self, *args, resolver=None):
        return self.func(args[0] if args else "")


class Random(CallableExpression):
    
    def __init__(self):
        import random
        self.func = random.random
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        return self.func()

class ReadFile(CallableExpression):
    
    def __init__(self):
        self.func = open
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        # print('reading file')
        arg_one = args[0] #file location
        with open(arg_one, 'r') as read_file:
            content =  read_file.readlines()
        return content
        # return self.func(args)

class WriteFile(CallableExpression):
    
    def __init__(self):
        self.func = open
        self.name = ''
        
    def register(self, name, environment):
        self.name = name
        environment.put(self.name, self)

    def arity(self):
        return 0
        
    def call(self, *args, resolver=None):
        arg_one = args[0] #file location
        arg_two = args[1] #file content
        with self.func(arg_one, 'w') as write_file:
            write_file.write(arg_two)


#####################native lox ArrayList class#############
class ArrayListClass(CallableExpression):
    def __init__(self, class_statement=None):
        self.class_statement = class_statement

    def call(self, *args, resolver=None):
        return ArrayListInstance()
        #return f"{self.class_statement.class_identifier_expression.expr.literal} class string value only"
# 
    def register(self, name, environment):
        self.environment = environment
        self.environment.put(name, self)

    def arity(self):
        pass 

class ArrayListInstance(LoxInstance):
   
    def __init__(self):
        self.lox_class = None
        self.args = None
        self.environment = None

        self.internal_array = list()
        # a = ArrayListInstance.Push(self.internal_array)
        self.methods_properties = {'push': ArrayListInstance.Push(self.internal_array),
                                   'pop': ArrayListInstance.Pop(self.internal_array),
                                   'len': ArrayListInstance.Len(self.internal_array),
                                   'at': ArrayListInstance.At(self.internal_array),
                                   'insertAt': ArrayListInstance.InsertAt(self.internal_array),
                                   'deleteAt': ArrayListInstance.DeleteAt(self.internal_array)}

    def getMethodsProperties(self, prop):
        #prop: simple string value ## wrong 
        #prop: must be token to print line # when there's error
        # print('prop -> ', prop.toString())
        try:
            ret_value = self.methods_properties[prop.literal]
            return ret_value
        except KeyError:
            raise Exception(f"no property named {prop.literal} in instance of {self.lox_class.class_statement.class_identifier_expression.expr.literal} at line {prop.line}")

    def setMethodsProperties(self, lvalue, rvalue):
        self.methods_properties[lvalue] = rvalue

    def __str__(self):
        return str(self.internal_array)

    ###########helper class ################
    class Push(CallableExpression):
    
        def __init__(self, internal_array):
            self.func = None
            self.name = ''
            self.internal_array = internal_array
            
        def register(self, name, environment):
            self.name = name
            environment.put(self.name, self)

        def arity(self):
            return 0
            
        def call(self, *args, resolver=None):
            arg_one = args[0] # item to push
           

            # print(arg_one)
            self.internal_array.append(arg_one)

    class Pop(CallableExpression):
    
        def __init__(self, internal_array):
            self.func = None
            self.name = ''
            self.internal_array = internal_array
            
        def register(self, name, environment):
            self.name = name
            environment.put(self.name, self)

        def arity(self):
            return 0
            
        def call(self, *args, resolver=None):
            return self.internal_array.pop()
            # return self.func(args)

    class Len(CallableExpression):
    
        def __init__(self, internal_array):
            self.func = len
            self.name = ''
            self.internal_array = internal_array
            
        def register(self, name, environment):
            self.name = name
            environment.put(self.name, self)

        def arity(self):
            return 0
            
        def call(self, *args, resolver=None):
            return len(self.internal_array)

    class At(CallableExpression):
    
        def __init__(self, internal_array):
            self.func = None
            self.name = ''
            self.internal_array = internal_array
            
        def register(self, name, environment):
            self.name = name
            environment.put(self.name, self)

        def arity(self):
            return 0
            
        def call(self, *args, resolver=None):
            index = int(args[0])
            return self.internal_array[index]

    class InsertAt(CallableExpression):
    
        def __init__(self, internal_array):
            self.func = None
            self.name = ''
            self.internal_array = internal_array
            
        def register(self, name, environment):
            self.name = name
            environment.put(self.name, self)

        def arity(self):
            return 0
            
        def call(self, *args, resolver=None):
            index = int(args[0]) #index
            obj = args[1] # new object
            self.internal_array[index] = obj
            # return self.func(args)

    class DeleteAt(CallableExpression):
        
        def __init__(self, internal_array):
            self.func = None
            self.name = ''
            self.internal_array = internal_array
            
        def register(self, name, environment):
            self.name = name
            environment.put(self.name, self)

        def arity(self):
            return 0
            
        def call(self, *args, resolver=None):
            index = int(args[0]) #index
            del self.internal_array[index]
            # return self.func(args)
    ##########################################
