import sys
from lexi import Lexical

class Syntax:
  def __init__(self, input):
    self.input = input
    self.lexer = Lexical(input)
    self.tokens = self.lexer.parse() # Parse all tokens from input
    self.current_index = 0
    self.current = self.tokens[0] if input else None # Takes the first character of the input if one exists
    self.parsed_tokens = []
    self.production_rules = []

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

    self.parsed_tokens.append((token_type, lexeme))

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

  def add_production(self, rule):
    print(rule)
    # Add a production rule to the syntax
    self.production_rules.append(rule)

  # Parsing function
  def parse(self):
    self.Rat25S()

    # In the event that all of the input tokens have been parsed but there are still tokens left
    if self.current is not None:
      self.syntax_error("Unexpected tokens at end of input.")

    return self.parsed_tokens, self.production_rules

# Functions for each syntax rule


  def Rat25S(self):
    self.add_production("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")

    self.match("Separator", "$$")
    self.optFunctionDefinitions()
    self.match("Separator", "$$")
    self.optDeclarationList()
    self.match("Separator", "$$")
    self.statementList()
    self.match("Separator", "$$")

  # <Opt Function Definitions> -> <Function Definitions> | <Empty>
  def optFunctionDefinitions(self):
    if self.current and self.current[1] == "function":
      self.add_production("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
      self.functionDefinitions()
    else:
      self.add_production("<Opt Function Definitions> -> <Empty>")
      self.empty()


  def functionDefinitions(self):
    self.add_production("<Function Definitions -> <Function> | <Function> <Function Definitions>")

    self.function()

    if self.current and self.current[1] == "function":
      self.functionDefinitions()

  def function(self):
    self.add_production("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")

    self.match("Keyword", "function")
    self.match("Identifier")
    self.match("Separator", "(")
    self.optParameterList()
    self.match("Separator", ")")
    self.optDeclarationList()
    self.body()

  # <Opt Parameter List> -> <Parameter List> | <Empty>
  def optParameterList(self):
    if self.current and self.current[0] == "Identifier":
      self.add_production("<Opt Parameter List> -> <Parameter List>")
      self.parameterList()
    else:
      self.add_production("<Opt Parameter List> -> <Empty>")
      self.empty()

  def parameterList(self):
    self.add_production("<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>")

    self.parameter()
    if self.current and self.current[1] == ",":
      self.match("Separator", ",")
      self.parameterList()


  def parameter(self):
    self.add_production("<Parameter> -> <IDs> <Qualifier>")

    self.ids()
    self.qualifier()


  def qualifier(self):
    self.add_production("<Qualifier> -> integer | boolean | real")

    if self.current is None:
      self.syntax_error("Unexpected end of input in <Qualifier>")

    token_type, lexeme = self.current
    if token_type == "Keyword" and lexeme in ["integer", "boolean", "real"]:
      self.match("Keyword", lexeme)
    else:
      self.syntax_error("Error: expected 'integer', 'boolean', or 'real' in <Qualifier>")

  def body(self):
    self.add_production("<Body> -> { <Statement List> }")

    self.match("Separator", "{")
    self.statementList()
    self.match("Separator", "}")

  #3 <Opt Declaration List> -> <Declaration List> | <Empty>
  def optDeclarationList(self):
    if self.current and self.current[0] == "Keyword" and self.current[1] in ["integer", "boolean", "real"]:
      self.declarationList()
      self.add_production("<Opt Declaration List> -> <Declaration List>")
    else:
      self.empty()
      self.add_production("<Opt Declaration List> -> <Empty>")

  def declarationList(self):
    self.add_production("<Declaration List> -> <Declaration> ; | <Declaration> ; <Declaration List>")

    self.declaration()
    self.match("Separator", ";")

    if self.current and self.current[0] == "Keyword" and self.current[1] in ["integer", "real", "boolean"]:
      self.declarationList()


  def declaration(self):
    self.add_production("<Declaration> -> <Qualifier><IDs>")

    self.qualifier()
    self.ids()

  def ids(self):
    self.add_production("<IDs> -> <Identifier> | <Identifier>, <IDs>")

    self.match("Identifier")

    if self.current and self.current[1] == ",":
      self.match("Separator", ",")
      self.ids()

  def statementList(self):
    self.add_production("<Statement List> -> <Statement> | <Statement> <Statement List>")

    self.statement()

    if self.current and self.current[0] in ["Identifier", "Separator", "Keyword"] and \
      (self.current[1] not in ["}", "endif", "endwhile"]):
        self.statementList()

  def statement(self):
    self.add_production("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")

    if not self.current:
      self.syntax_error("Unexpected end of input in <Statement>")

    token_type, lexeme = self.current

    # <Compound>
    if token_type == "Separator" and lexeme == "{":
      self.compound()

    # <Assign>
    elif token_type == "Identifier":
      self.assign()

    # <If>, <Return>, <Print>, <Scan>, <While>
    elif token_type == "Keyword":
      if lexeme == "if":
        self._if()
      elif lexeme == "return":
        self._return()
      elif lexeme == "print":
        self._print()
      elif lexeme == "scan":
        self.scan()
      elif lexeme == "while":
        self._while()
      else:
        self.syntax_error("Unexpected keyword in <Statement>")
    else:
      self.syntax_error("Unexpected token for <Statement>")


  def compound(self):
    self.add_production("<Compound> -> { <Statement List> }")
    self.match("Separator", "{")
    self.statementList()
    self.match("Separator", "}")


  def assign(self):
    self.add_production("<Assign> -> <Identifier> = <Expression>")
    self.match("Identifier")
    self.match("Operator", "=")
    self.expression()


  def _if(self):
    self.add_production("<If> -> if(<Condition>)<Statement> <If Prime>")
    self.match("Keyword", "if")
    self.match("Separator", "(")
    self.condition()
    self.match("Separator", ")")
    self.statement()
    self.ifPrime()

  def ifPrime(self):
    # <If Prime> -> endif | else <Statement> endif")
    if self.current and self.current[1] == "endif":
      self.add_production("<If Prime> -> endif")
      self.match("Keyword", "endif")
    else:
      self.add_production("<If Prime> -> else <Statement> endif")
      self.match("Keyword", "else")
      self.statement()
      self.match("Keyword", "endif")


  def _return(self):
    self.add_production("<Return> -> return <Return Prime>")
    self.match("Keyword", "return")
    self.returnPrime()


  def returnPrime(self):
    if self.current and self.current[1] == ";":
      self.add_production("<Return Prime> -> ;")
      self.match("Separator", ";")
    else:
      self.add_production("<Return Prime> -> <Expression> ;")
      self.expression()
      self.match("Separator", ";")

  def _print(self):
    self.add_production("<Print> -> print ( <Expression>) ;")

    self.match("Keyword", "print")
    self.match("Separator", "(")
    self.expression()
    self.match("Separator", ")")
    self.match("Separator", ";")


  def scan(self):
    self.add_production("<Scan> -> scan(<IDs>);")

    self.match("Keyword", "scan")
    self.match("Separator", "(")
    self.ids()
    self.match("Separator", ")")
    self.match("Separator", ";")


  def _while(self):
    self.add_production("<While> -> while ( <Condition> ) <Statement> endwhile")

    self.match("Keyword", "while")
    self.match("Separator", "(")
    self.condition()
    self.match("Separator", ")")
    self.statement()
    self.match("Keyword", "endwhile")


  def condition(self):
    self.add_production("<Condition> -> <Expression> <Relop> <Expression>")

    self.expression()
    self.relop()
    self.expression()


  def relop(self):
    self.add_production("<Relop> -> == | != | > | < | <= | =>")
    if self.current and self.current[0] == "Operator" and self.current[1] in ["==", "!=", ">", "<", "<=", ">="]:
      self.match("Operator", self.current[1])
    else:
      self.syntax_error("Relational operator expected.")



  def expression(self):
    self.add_production("<Expression> -> <Term> <Expression Prime>")
    self.term()
    self.expressionPrime()

  # Expression Prime -> + <Term> <Expression Prime> | - <Term> <Expression Prime> | <Empty>
  def expressionPrime(self):
    if self.current and self.current[0] == "Operator" and self.current[1] in ["+", "-"]:
      self.add_production("Expression Prime -> +<Term><Expression Prime> | -<Term><Expression Prime>")

      self.match("Operator", self.current[1])
      self.term()
      self.expressionPrime()
    else:
      self.add_production("Expression Prime -> <Empty>")
      self.empty()


  def term(self):
    self.add_production("<Term> -> <Factor><Term Prime>")
    self.factor()
    self.termPrime()

  # <Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime> | <Empty>
  def termPrime(self):
    if self.current and self.current[0] == "Operator" and self.current[1] in ["*", "/"]:
      self.add_production("<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime>")

      self.match("Operator", self.current[1])
      self.factor()
      self.termPrime()
    else:
      self.add_production("<Term Prime> -> <Empty>")
      self.empty()


  # <Factor> -> - <Primary> | <Primary>
  def factor(self):
    self.add_production("<Factor> -> - <Primary> | <Primary>")
    if self.current and self.current[0] == "Operator" and self.current[1] == "-":
      self.add_production("<Factor> -> - <Primary>")
      self.match("Operator", "-")
      self.primary()
    else:
      self.add_production("<Factor> -> <Primary>")
      self.primary()


  def primary(self):
    self.add_production("<Primary> -> <Identifier> <Primary Prime> | <Integer> | ( <Expression> ) | <Real> | true | false ")

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
    elif token_type == "Boolean":
      self.match("Boolean")
    else:
      self.syntax_error(f"Invalid <Primary>: {token_type}, {lexeme}")


  # <Primary Prime> -> ( <IDs> ) | <Empty> )
  def primaryPrime(self):
    if self.current and self.current[0] == "Separator" and self.current[1] == "(":
      self.add_production("<Primary Prime> -> ( <IDs> )")
      self.match("Separator", "(")
      self.ids()
      self.match("Separator", ")")
    else:
      self.add_production("<Primary Prime> -> <Empty>")
      self.empty()


  def empty(self):
    self.add_production("<Empty> -> epsilon")


# Actual usage of parser
def main():
  # Read three test files
  filenames = ["test1.txt", "test2.txt", "test3.txt"]

  for name in filenames: # Go through each file
    try:
      with open(name, 'r') as file: # Open the file
        input_text = file.read() # Read the file

      # Get lexical tokens using lexi.py
      lexer = Lexical(input_text)

      tokens = lexer.parse()

      parser = Syntax(input_text)


      try:
        parsed_tokens, production_rules = parser.parse()

        output_filename = f"{name}_output.txt"
        with open(output_filename, "w") as output_file:

          output_file.write("Tokens and Lexemes:\n")
          output_file.write(f"{'Token':<15}{'Lexeme':<15}\n")
          output_file.write("-"*30 + "\n")
          for token_type, lexeme in tokens:
            output_file.write(f"{token_type:<15}{lexeme:<15}\n")

          output_file.write("\nProduction Rules: \n")
          output_file.write("-"*50 + "\n")
          for i, rule in enumerate(production_rules, 1):
            output_file.write(f"Rule {i}: {rule}\n")

          output_file.write(f"\nSYNTAX ERROR: \n{e}\n")

        print("Syntax Analyzer successfully parsed the file: ", name)
        print(f"Results saved to: {output_filename}")

      except SyntaxError as e:
        print(f"Error parsing file {name}: {e}")

        output_filename = f"{name}_output.txt"
        with open(output_filename, "w") as output_file:
          output_file.write(f"Analyzing {name}...\n")
          output_file.write("="*50 + "\n\n")

          output_file.write("Tokens and Lexemes:\n")
          output_file.write(f"{'Token':<15}{'Lexeme':<15}\n")
          output_file.write("-"*30 + "\n")
          for token_type, lexeme in tokens:
            output_file.write(f"{token_type:<15}{lexeme:<15}\n")

          output_file.write(f"\n SYNTAX ERROR: \n{e}\n")

    except FileNotFoundError:
      print(f"File {name} not found")

if __name__ == "__main__":
  main()