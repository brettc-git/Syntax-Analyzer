import sys
from lexi import Lexical

class Syntax:
  def __init__(self, input):
    self.input = input
    self.lexer = Lexical(input)
    self.tokens = self.lexer.parse() # Parse all tokens from input
    self.current_index = 0
    self.current = self.tokens[0] if input else None # Takes the first character of the input if one exists

  def match(self, exp_type, exp_lexeme = None):
    # Get the current token and expected type and the lexeme
    if self.current is None:
      self.syntax_error(f"Expected {exp_type}, but reached end of input")

    token_type, lexeme = self.current

    # Throw an error if the token type does not match the expected type
    if token_type != exp_type:
      self.syntax_error(f"Expected {exp_type}, but got {token_type}")

    # Throw an error if the lexeme does not match the expected lexeme
    if exp_lexeme is not None and lexeme != exp_lexeme:
      self.syntax_error(f"Expected {exp_lexeme}, but got {lexeme}")

    _current = self.current
    self.next()
    return _current

  def next(self):
    self.current_index += 1

    if self.current_index < len(self.tokens):
      self.current = self.tokens[self.current_index]
    else:
      # If there are no more tokens, return None
      self.current = None

  # Error function
  def syntax_error(self, expected):
    raise SyntaxError(f"Syntax Error: {expected}")

  # Parsing function
  def parse(self):
    self.Rat25S()

    # In the event that all of the input tokens have been parsed but there are still tokens left
    if self.current is not None:
      self.syntax_error("Unexpected tokens at end of input.")


# Functions for each syntax rule

  # Done
  def Rat25S(self):
    print("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")
    self.match("Separator", "$$")
    self.optFunctionDefinitions()
    self.match("Separator", "$$")
    self.optDeclarationList()
    self.match("Separator", "$$")
    self.statementList()
    self.match("Separator", "$$")

  # Done
  def optFunctionDefinitions(self):
    print("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    if self.current and self.current[1] == "function":
      self.functionDefinitions()
    else:
      self.empty()


  def functionDefinitions(self):
    print("<Function Definitions -> <Function> | <Function> <Function Definitions>")

    self.function()

    if self.current and self.current[1] == "function":
      self.functionDefinitions()

  def function(self):
    print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")

    self.match("Keyword", "function")
    self.match("Identifier")
    self.match("Separator", "(")
    self.optParameterList()
    self.match("Separator", ")")
    self.optDeclarationList()
    self.body()

  def optParameterList(self):
    print("<Opt Parameter List> -> <Parameter List> | <Empty>")
    if self.current and self.current[1] == "identifier":
      self.parameterList()
    else:
      self.empty()

  def parameterList(self):
    print("<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>")

    self.parameter()
    if self.current and self.current[1] == ",":
      self.match("Separator", ",")
      self.parameterList()

  # Done
  def parameter(self):
    print("<Parameter> -> <IDs> <Qualifier>")
    self.ids()
    self.qualifier()

  # CHECK
  def qualifier(self):
    print("<Qualifier> -> integer | boolean | real")
    if self.current is None:
      self.syntax_error("Unexpected end of input in <Qualifier>")

    token_type, lexeme = self.current
    if token_type == "Integer":
      self.match("Integer")
    elif token_type == "Boolean":
      self.match("Boolean")
    elif token_type == "Real":
      self.match("Real")
    else:
      self.syntax_error("Invalid Token")

  def body(self):
    print("<Body> -> { <Statement List> }")
    self.match("Separator", "{")
    self.statementList()
    self.match("Separator", "}")

  def optDeclarationList(self):
    print("<Opt Declaration List> -> <Declaration List> | <Empty>")
    if self.current and self.current[1] in ["integer", "boolean", "real"]:
      self.declarationList()
    else:
      self.empty()

  def declarationList(self):
    print("<Declaration List> -> <Declaration> ; | <Declaration> ; <Declaration List>")
    self.declaration()
    self.match("Separator", ";")
    if self.current and self.current[1] in ["integer", "real", "boolean"]:
      self.declarationList()


  def declaration(self):
    print("<Declaration> -> <Qualifier><IDs>")

    self.qualifier()
    self.ids()

  def ids(self):
    print("<IDs> -> <Identifier> | <Identifier>, <IDs>")
    self.match("Identifier")

    if self.current and self.current[1] == ",":
      self.match("Separator", ",")
      self.ids()

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

  # Done
  def compound(self):
    print("<Compound> -> { <Statement List> }")
    self.match("Separator", "{")
    self.statementList()
    self.match("Separator", "}")

  # Done
  def assign(self):
    print("<Assign> -> <Identifier> -> <Expression>")
    self.match("Identifier")
    self.match("Separator", "->")
    self.expression()

  # Done
  def _if(self):
    print("<If> -> if(<Condition>)<Statement> <If Prime>")
    self.match("Keyword", "if")
    self.match("Separator", "(")
    self.condition()
    self.match("Separator", ")")
    self.statement()
    self.ifPrime()

  def ifPrime(self):
    print("<If Prime> -> endif | else <Statement> endif")

    if self.current and self.current[1] == "endif":
      self.match("Keyword", "endif")
    else:
      self.match("Keyword", "else")
      self.statement()
      self.match("Keyword", "endif")

  # Done
  def _return(self):
    print("<Return> -> return <Return Prime>")
    self.match("Keyword", "return")
    self.returnPrime()

  # Done
  def returnPrime(self):
    print("<Return Prime> -> ; | <Expression> ;")
    if self.current and self.current[1] == ";":
      self.match("Separator", ";")
    else:
      self.expression()
      self.match("Separator", ";")

  def _print(self):
    print("<Print> -> print ( <Expression>) ;")
    self.match("Keyword", "print")
    self.match("Separator", "(")
    self.expression()
    self.match("Separator", ")")
    self.match("Separator", ";")

  # Done
  def scan(self):
    print("<Scan> -> scan(<IDs>);")
    self.match("Keyword", "scan")
    self.match("Separator", "(")
    self.ids()
    self.match("Separator", ")")
    self.match("Separator", ";")

  # Done
  def _while(self):
    print("<While> -> while ( <Condition> ) <Statement> endwhile")
    self.match("Keyword", "while")
    self.match("Separator", "(")
    self.condition()
    self.match("Separator", ")")
    self.statement()
    self.match("Keyword", "endwhile")

  # Done
  def condition(self):
    print("<Condition> -> <Expression> <Relop> <Expression>")
    self.expression()
    self.relop()
    self.expression()

  # Done
  def relop(self):
    print("<Relop> -> == | != | > | < | <= | =>")
    if self.current[1] in ["==", "!=" ,">", "<", "<=", ">="]:
      self.match("Operator")
    else:
      self.syntax_error("Relational operator expected.")


  # Done
  def expression(self):
    print("<Expression> -> <Term> <Expression Prime>")
    self.term()
    self.expressionPrime()

  # Done
  def expressionPrime(self):
    print("Expression Prime -> +<Term><Expression Prime> | -<Term><Expression Prime> | empty")
    if self.current and self.current[1] in ["+", "-"]:
      self.match("Operator")
      self.term()
      self.expressionPrime()
    else:
      self.empty()

  # Done
  def term(self):
    print("<Term> -> <Factor><Term Prime>")
    self.factor()
    self.termPrime()

  # Done
  def termPrime(self):
    print("<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime> | empty")
    if self.current and self.current[1] in ["*", "/"]:
      self.match("Operator")
      self.factor()
      self.termPrime()
    else:
      self.empty()


  # Done
  def factor(self):
    print("<Factor> -> - <Primary> | <Primary>")
    if self.current and self.current[1] == "-":
      self.match("Operator")
      self.primary()
    else:
      self.primary()

  # Done
  def primary(self):
    print("<Primary> -> <Identifier> <Primary Prime> | <Integer> | ( <Expression> ) | <Real> | true | false ")
    if self.current is None:
      self.syntax_error("Unexpected end of input in <Primary>")

    token_type, lexeme = self.current

    if token_type == "Identifier":
      self.match("Identifier")
      self.primaryPrime()
    elif token_type == "Integer":
      self.match("Integer")
    elif token_type == "Separator" and lexeme == "(":
      self.match("Separator", "(")
      self.expression()
      self.match("Separator", ")")
    elif token_type == "Real":
      self.match("Real")
    elif token_type == "Keyword" and lexeme in ["true", "false"]:
      self.match("Keyword", lexeme)
    else:
      self.syntax_error("Invalid <Primary>")

  # Done
  def primaryPrime(self):

    print("<Primary Prime> -> ( <IDs> ) | empty")

    if self.current and self.current[1] == "(":
      self.match("Separator", "(")
      self.ids()
      self.match("Separator", ")")
    else:
      self.empty()

  # Done
  def empty(self):
    print("<Empty> -> epsilon")


# Actual usage of parser

# Read three test files
filenames = ["test1.txt", "test2.txt", "test3.txt"]

for name in filenames: # Go through each file
  try:
    with open(name, 'r') as file: # Open the file
      input_text = file.read() # Read the file

    parser = Syntax(input_text)
    try:
      parser.parse()
      print("Syntax Analyzer successfully parsed the file: ", name)
    except SyntaxError as e:
      print(f"Error parsing {name}: {e}")
  except FileNotFoundError:
    print(f"File {name} not found")

result = ""
with open("output.txt", 'w') as file:
  file.write(result)