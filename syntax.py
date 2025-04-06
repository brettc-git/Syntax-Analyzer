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
      self.error(f"Expected {exp_type}, but reached end of input")

    token_type, lexeme = self.current

    # Throw an error if the token type does not match the expected type
    if token_type != exp_type:
      self.error(f"Expected {exp_type}, but got {token_type}")

    # Throw an error if the lexeme does not match the expected lexeme
    if exp_lexeme is not None and lexeme != exp_lexeme:
      self.error(f"Expected {exp_lexeme}, but got {lexeme}")

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
  def syntax_error(expected):
    raise SyntaxError(f"Syntax Error: {expected}")

  # Parsing function
  def parse(self):
    self.Rat25S()

    # In the event that all of the input tokens have been parsed but there are still tokens left
    if self.current is not None:
      self.syntax_error("Unexpected tokens at end of input.")
# Functions for each syntax rule


  def Rat25S(self):
    print("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")
    self.match("Separator", "$$")
    self.optFunctionDefinitions()
    self.match("Separator", "$$")
    self.optDeclarationList()
    self.match("Separator", "$$")
    self.statementList()
    self.match("Separator", "$$")


  def optFunctionDefinitions(self):
    print("<Opt Function Definitions> -> <Function Definitions> | <Empty>")

    self.functionDefinitions()
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

    self.parameterList()
    self.empty()

  def parameterList(self):
    print("<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>")
    self.match("Separator", ",")
    self.parameterList()

  def parameter(self):
    print("<Parameter> -> <IDs> <Qualifier>")


  def qualifier(self):
    print("<Qualifier> -> integer | boolean | real")

  def body(self):
    print("<Body> -> { <Statement List> }")
    self.match("Separator", "{")
    self.statementList()
    self.match("Separator", "}")

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

    self.returnPrime()
    self.match("Separator", ";")
    self.expression()
    self.match("Separator", ";")

  def _print(self):
    print("<Print> ::= print ( <Expression>) ;")
    self.match("Separator", "(")
    self.expression()
    self.match("Separator", ")")
    self.match("Separator", ";")

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
    if self.current[1] in ["==", "!=" ,">", "<", "<=", ">="]:
      self.match("Operator")
    else:
      self.syntax_error("Relational operator expected.")


  def expression(self):
    print("<Expression> -> <Term> <Expression Prime>")
    self.term()
    self.expressionPrime()

  def expressionPrime(self):
    print("Expression Prime -> +<Term><Expression Prime> | -<Term><Expression Prime> | empty")
    if self.current and self.current[1] in ["+", "-"]:
      self.match("Operator")
      self.term()
      self.expressionPrime()
    else:
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
    if self.current and self.current[1] == "-":
      self.match("Operator")
      self.primary()
    else:
      self.primary()

  def primary(self):
    print("<Primary> -> <Identifier> <Primary Prime> | <Integer> | ( <Expression> ) | <Real> | true | false ")

  def primaryPrime(self):

    print("<Primary Prime> -> ( <IDs> ) | empty")

    self.match("Separator", "(")
    self.ids()
    self.match("Separator", ")")
    self.empty()

  def empty(self):
    print("<Empty> -> epsilon")


# Actual usage of parser

# Create three test files
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