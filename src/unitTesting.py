from ASTPrinter import ASTPrinter
from parser import Parser, BinaryExpression, UnaryExpression, GroupingExpression, LiteralExpression, StatementExecutor
from lexer import TokenType, Token, Scanner
from environment import Environment
from resolver import Resolver


def test_printer():
    new_expr = BinaryExpression(
                    UnaryExpression(Token(TokenType.MINUS), 
                                    LiteralExpression(123)),
                    Token(TokenType.STAR),

                    GroupingExpression(LiteralExpression(45.67))
                    )
    # new_expr = LiteralExpression(234)
    print(ASTPrinter().print(new_expr))

def test_lexer(source_code='2+2*2;'):

    scanner = Scanner(source_code)
    scanner.scanTokens()
    for tkn in scanner.token_list:
        print(tkn.toString())

    parser = Parser(scanner.token_list)
    parser.parse()

    print(ASTPrinter().print(parser.AST))


def test_parser(source_code='2+2*2; print (2 + (3*3+3);'):
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


def test_if_block_statement(source_code='''if true { 
    print true; 
    } else {
    print false; 
    }; '''):

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


def test_while_block_statement(source_code='''var i = 0;
    while i<3 { 
        print i;
        i = i + 1;
    };'''):

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


def test_reassignment_statement(source_code='''var i = 110;
    print i;
    i /= 10;
    print i;'''):

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

def test_function_statement(source_code='''fun add(a, b) {
    var a = 2;
    print a;
    };
    
    fun random(){};'''):

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


def test_function_call_expression(source_code='''fun count(n) {
    if n != 0 {
    count(n-1);
    };
    };
    count(4);
    '''):

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
    print('-------')
    env = Environment()
    for AST in parser.AST:
        StatementExecutor(env).execute(AST)



def test_anon_function(source_code='''var a =  |n| { 
  if n<=2 { 
    return 1; 
  };
  return this(n-1) + this(n-2); 
};

'''):

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
    print('-------')
    env = Environment()
    for AST in parser.AST:
        StatementExecutor(env).execute(AST)


def test_resolver(source_code='''
    var a = "global";
    {
      fun showA() {
        print a;
      };

      showA();
      var a = "block";
      showA();
    };'''):

    scanner = Scanner(source_code)
    scanner.scanTokens()
    # print(scanner.toString())


    parser = Parser(scanner.token_list)
    parser.parse()
    # print(parser.AST)
    # print(ASTPrinter().print(parser.AST[0]))
    # print(ASTPrinter().print(parser.AST[1]))
    # print('------')
    # for AST in parser.AST:
    #     print(ASTPrinter().print(AST))
    # print('-------')
    
    resolver = Resolver()
    resolver.resolveAll(parser.AST)

    env = Environment()
    for AST in parser.AST:
        StatementExecutor(env, resolver).execute(AST)

def test_resolver_loop(source_code='''
    var counter = 0;
    while counter <= 10 {
    print counter;
    counter += 1;
    };
    '''):

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
    print('-------')
    
    resolver = Resolver()
    resolver.resolveAll(parser.AST)

    env = Environment()
    for AST in parser.AST:
        StatementExecutor(env, resolver).execute(AST)



def test_class_declaration(source_code='''class Simple{
        var a = 23;
        var b = 100;
        fun Simple(){

        };
    };
    var s = Simple();
    var c = Simple();

    print "inside program";
    print c;
    '''):

    scanner = Scanner(source_code)
    scanner.scanTokens()
    # print(scanner.toString())


    parser = Parser(scanner.token_list)
    parser.parse()
    
    for AST in parser.AST:
        print(ASTPrinter().print(AST))
    print('-------')
    
    resolver = Resolver()
    resolver.resolveAll(parser.AST)

    env = Environment()
    for AST in parser.AST:
        StatementExecutor(env, resolver).execute(AST)

