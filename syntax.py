from lexi import Lexical

class Syntax:
  def __init__(self, input):
    self.input = input
    self.lexer = Lexical(input)
    self.pos = 0
    self.line = 1 # First line
    self.column = 1 # First letter
    self.current = self.input[0] if input else None # Takes the first character of the input if one exists

  def next(self):
    self.pos += 1
    self.column += 1

    if self.pos >= len(self.input):
      self.current = None
    else:
      self.current = self.input[self.pos]
      if self.current == '\n':
        self.line += 1
        self.column = 0

# Functions for each syntax rule
  def Rat25S(self):
    print("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")

  def optFunctionDefinitions(self):
    print("<Opt Function Definitions> -> <Function Definitions> | <Empty>")

    self.functionDefinitions()
    self.empty()

  def functionDefinitions(self):
    print("<Function Definitions -> <Function> | <Function> <Function Definitions>")

    self.function()
    self.functionDefinitions()

  def function(self):
    print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")

  def optParameterList(self):
    print("<Opt Parameter List> -> <Parameter List> | <Empty>")

    self.parameterList()
    self.empty()

  def parameterList(self):
    print("<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>")

  def parameter(self):
    print("<Parameter> -> <IDs> <Qualifier>")

  def qualifier(self):
    print("<Qualifier> -> integer | boolean | real")

  def body(self):
    print("<Body> -> { <Statement List> }")

  def optDeclarationList(self):
    print("<Opt Declaration List> -> <Declaration List> | <Empty>")

  def declarationList(self):
    print("<Declaration List> -> <Declaration> ; | <Declaration> ; <Declaration List>")

  def declaration(self):
    print("<Declaration> -> <Qualifier><IDs>")

    self.qualifier()
    self.ids()

  def ids(self):
    print("<IDs> -> <Identifier> | <Identifier>, <IDs>")

  def statementList(self):
    print("<Statement List> -> <Statement> | <Statement> <Statement List>")

  def statement(self):
    print("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")


    self.compound()
    self.assign()
    # if current lexeme is "if"
    self._if()
    # if current lexeme is "return"
    self._return()
    # if current lexeme is "print"
    self._print()
    # if current lexeme is "scan"
    self.scan()
    # if current lexeme is "while"
    self._while()
    # else:

  def compound(self):
    print("<Compound> -> { <Statement List> }")

  def assign(self):
    print("<Assign> -> <Identifier> -> <Expression>")


  def _if(self):
    print("<If> -> if(<Condition>)<Statement> <If Prime>")

  def ifPrime(self):
    print("<If Prime> -> endif | else <Statement> endif")

  def _return(self):
    print("<Return> -> return <Return Prime>")

  def returnPrime(self):
    print("<Return Prime> -> ; | <Expression> ;")

  def _print(self):
    print("<Print> ::= print ( <Expression>);")

  def scan(self):
    print("<Scan> -> scan(<IDs>);")

  def _while(self):
    print("<While> -> while ( <Condition> ) <Statement> endwhile")
    self.condition()
    self.statement()

  def condition(self):
    print("<Condition> -> <Expression> <Relop> <Expression>")
    self.expression()
    self.relop()
    self.expression()

  def relop(self):
    print("<Relop> -> == | != | > | < | <= | =>")

  def expression(self):
    print("<Expression> -> <Term> <Expression Prime>")
    self.term()
    self.expressionPrime()

  def expressionPrime(self):
    print("Expression Prime -> +<Term><Expression Prime> | -<Term><Expression Prime> | empty")
    self.term()
    self.expressionPrime()
    self.empty()

  def term(self):
    print("<Term> -> <Factor><Term Prime>")

    self.factor()
    self.termPrime()

  def termPrime(self):
    print("<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime> | empty")

    self.empty()


  def factor(self):
    print("<Factor> ::= - <Primary> | <Primary>")

  def primary(self):
    print("<Primary> -> <Identifier> <Primary Prime> | <Integer> | ( <Expression> ) | <Real> | true | false ")

  def primaryPrime(self):
    print("<Primary Prime> -> ( <IDs> ) | empty")

  def empty(self):
    print("<Empty> -> epsilon")

  # Error function
  def syntax_error(expected):
    raise SyntaxError(f"Syntax Error at line {line_num}: Expected {expected}, got {token_value} ({token_type})")

# def newToken():
#   current_token = lexi.getToken()
#   if current_token == expected_type:
#       nextToken()
#   else:
#       syntax_error



# Create three test files
filenames = ["test1.txt", "test2.txt", "test3.txt"]

for filename in filenames:
  try:
    with open(filename, 'r') as file:
      data = file.read()

  except FileNotFoundError:
    print(f"File {filename} not found")
