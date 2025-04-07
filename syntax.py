import sys
from lexi import Lexical

class Syntax:
  def __init__(self, input):
    self.input = input
    self.lexer = Lexical(input)
    self.tokens = self.lexer.parse() # Parse all tokens from input
    self.current_index = 0
    self.current = self.tokens[0] if self.tokens else None # Takes the first token if one exists
    self.output_content = []  # To store output in the required format
    self.last_production_rules = []  # Store last rules before adding token

  def match(self, exp_type, exp_lexeme=None):
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

    # Append the production rules that led to this token
    for rule in self.last_production_rules:
      self.output_content.append(f"     {rule}")

    # Clear the production rules now that they've been used
    self.last_production_rules = []

    # Store the token and lexeme in the output
    self.output_content.append(f"**Token: {token_type:<15} Lexeme: {lexeme}**")

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

  # Add production rule to the list
  def add_production(self, rule):
    print(rule)
    self.last_production_rules.append(rule)

  # Error function
  def syntax_error(self, expected):
    self.output_content.append(f"\n SYNTAX ERROR: \n{expected}")
    raise SyntaxError(expected)

  # Parsing function
  def parse(self):
    try:
      self.Rat25S()

      # In the event that all of the input tokens have been parsed but there are still tokens left
      if self.current is not None:
        self.syntax_error("Unexpected tokens at end of input.")

      return self.output_content
    except SyntaxError as e:
      return self.output_content

# Functions for each syntax rule

  def Rat25S(self):
    rule = "<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$"
    self.add_production(rule)

    self.match("Separator", "$$")
    self.optFunctionDefinitions()
    self.match("Separator", "$$")
    self.optDeclarationList()
    self.match("Separator", "$$")
    self.statementList()
    self.match("Separator", "$$")

  def optFunctionDefinitions(self):
    if self.current and self.current[1] == "function":
      rule = "<Opt Function Definitions> -> <Function Definitions>"
      self.add_production(rule)
      self.functionDefinitions()
    else:
      rule = "<Opt Function Definitions> -> <Empty>"
      self.add_production(rule)
      self.empty()

  def functionDefinitions(self):
    rule = "<Function Definitions> -> <Function> | <Function> <Function Definitions>"
    self.add_production(rule)

    self.function()

    if self.current and self.current[1] == "function":
      self.functionDefinitions()

  def function(self):
    rule = "<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>"
    self.add_production(rule)

    self.match("Keyword", "function")
    self.match("Identifier")
    self.match("Separator", "(")
    self.optParameterList()
    self.match("Separator", ")")
    self.optDeclarationList()
    self.body()

  def optParameterList(self):
    if self.current and self.current[0] == "Identifier":
      rule = "<Opt Parameter List> -> <Parameter List>"
      self.add_production(rule)
      self.parameterList()
    else:
      rule = "<Opt Parameter List> -> <Empty>"
      self.add_production(rule)
      self.empty()

  def parameterList(self):
    rule = "<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>"
    self.add_production(rule)

    self.parameter()
    if self.current and self.current[1] == ",":
      self.match("Separator", ",")
      self.parameterList()

  def parameter(self):
    rule = "<Parameter> -> <IDs> <Qualifier>"
    self.add_production(rule)

    self.ids()
    self.qualifier()

  def qualifier(self):
    rule = "<Qualifier> -> integer | boolean | real"
    self.add_production(rule)

    if self.current is None:
      self.syntax_error("Unexpected end of input in <Qualifier>")

    token_type, lexeme = self.current
    if token_type == "Keyword" and lexeme in ["integer", "boolean", "real"]:
      self.match("Keyword", lexeme)
    else:
      self.syntax_error("Invalid qualifier. Expected 'integer', 'boolean', or 'real'")

  def body(self):
    rule = "<Body> -> { <Statement List> }"
    self.add_production(rule)

    self.match("Separator", "{")
    self.statementList()
    self.match("Separator", "}")

  def optDeclarationList(self):
    if self.current and self.current[0] == "Keyword" and self.current[1] in ["integer", "boolean", "real"]:
      rule = "<Opt Declaration List> -> <Declaration List>"
      self.add_production(rule)
      self.declarationList()
    else:
      rule = "<Opt Declaration List> -> <Empty>"
      self.add_production(rule)
      self.empty()

  def declarationList(self):
    rule = "<Declaration List> -> <Declaration> ; | <Declaration> ; <Declaration List>"
    self.add_production(rule)

    self.declaration()
    self.match("Separator", ";")
    if self.current and self.current[0] == "Keyword" and self.current[1] in ["integer", "real", "boolean"]:
      self.declarationList()

  def declaration(self):
    rule = "<Declaration> -> <Qualifier><IDs>"
    self.add_production(rule)

    self.qualifier()
    self.ids()

  def ids(self):
    rule = "<IDs> -> <Identifier> | <Identifier>, <IDs>"
    self.add_production(rule)

    self.match("Identifier")

    if self.current and self.current[1] == ",":
      self.match("Separator", ",")
      self.ids()

  def statementList(self):
    rule = "<Statement List> -> <Statement> | <Statement> <Statement List>"
    self.add_production(rule)

    self.statement()

    # Check if there are more statements
    if self.current and self.current[0] in ["Identifier", "Separator", "Keyword"] and \
       (self.current[1] not in ["$$", "}", "endif", "endwhile"]):
        self.statementList()

  def statement(self):
    rule = "<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>"
    self.add_production(rule)

    if not self.current:
        self.syntax_error("Unexpected end of input in <Statement>")

    token_type, lexeme = self.current

    if token_type == "Separator" and lexeme == "{":
        self.compound()
    elif token_type == "Identifier":
        self.assign()
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
            self.syntax_error(f"Unexpected keyword '{lexeme}' in <Statement>")
    else:
        self.syntax_error(f"Invalid token for <Statement>: {token_type}, {lexeme}")

  def compound(self):
    rule = "<Compound> -> { <Statement List> }"
    self.add_production(rule)

    self.match("Separator", "{")
    self.statementList()
    self.match("Separator", "}")

  def assign(self):
    rule = "<Assign> -> <Identifier> = <Expression> ;"
    self.add_production(rule)

    self.match("Identifier")
    self.match("Operator", "=")
    self.expression()
    self.match("Separator", ";")

  def _if(self):
    rule = "<If> -> if(<Condition>)<Statement> <If Prime>"
    self.add_production(rule)

    self.match("Keyword", "if")
    self.match("Separator", "(")
    self.condition()
    self.match("Separator", ")")
    self.statement()
    self.ifPrime()

  def ifPrime(self):
    if self.current and self.current[1] == "endif":
      rule = "<If Prime> -> endif"
      self.add_production(rule)
      self.match("Keyword", "endif")
    else:
      rule = "<If Prime> -> else <Statement> endif"
      self.add_production(rule)
      self.match("Keyword", "else")
      self.statement()
      self.match("Keyword", "endif")

  def _return(self):
    rule = "<Return> -> return <Return Prime>"
    self.add_production(rule)

    self.match("Keyword", "return")
    self.returnPrime()

  def returnPrime(self):
    if self.current and self.current[1] == ";":
      rule = "<Return Prime> -> ;"
      self.add_production(rule)
      self.match("Separator", ";")
    else:
      rule = "<Return Prime> -> <Expression> ;"
      self.add_production(rule)
      self.expression()
      self.match("Separator", ";")

  def _print(self):
    rule = "<Print> -> print ( <Expression>) ;"
    self.add_production(rule)

    self.match("Keyword", "print")
    self.match("Separator", "(")
    self.expression()
    self.match("Separator", ")")
    self.match("Separator", ";")

  def scan(self):
    rule = "<Scan> -> scan(<IDs>);"
    self.add_production(rule)

    self.match("Keyword", "scan")
    self.match("Separator", "(")
    self.ids()
    self.match("Separator", ")")
    self.match("Separator", ";")

  def _while(self):
    rule = "<While> -> while ( <Condition> ) <Statement> endwhile"
    self.add_production(rule)

    self.match("Keyword", "while")
    self.match("Separator", "(")
    self.condition()
    self.match("Separator", ")")
    self.statement()
    self.match("Keyword", "endwhile")

  def condition(self):
    rule = "<Condition> -> <Expression> <Relop> <Expression>"
    self.add_production(rule)

    self.expression()
    self.relop()
    self.expression()

  def relop(self):
    rule = "<Relop> -> == | != | > | < | <= | =>"
    self.add_production(rule)

    if self.current and self.current[0] == "Operator" and self.current[1] in ["==", "!=", ">", "<", "<=", "=>"]:
      self.match("Operator", self.current[1])
    else:
      self.syntax_error("Relational operator expected.")

  def expression(self):
    rule = "<Expression> -> <Term> <Expression Prime>"
    self.add_production(rule)

    self.term()
    self.expressionPrime()

  def expressionPrime(self):
    if self.current and self.current[0] == "Operator" and self.current[1] in ["+", "-"]:
      rule = "<Expression Prime> -> +<Term><Expression Prime> | -<Term><Expression Prime>"
      self.add_production(rule)

      op = self.current[1]
      self.match("Operator", op)
      self.term()
      self.expressionPrime()
    else:
      rule = "<Expression Prime> -> <Empty>"
      self.add_production(rule)
      self.empty()

  def term(self):
    rule = "<Term> -> <Factor><Term Prime>"
    self.add_production(rule)

    self.factor()
    self.termPrime()

  def termPrime(self):
    if self.current and self.current[0] == "Operator" and self.current[1] in ["*", "/"]:
      rule = "<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime>"
      self.add_production(rule)

      op = self.current[1]
      self.match("Operator", op)
      self.factor()
      self.termPrime()
    else:
      rule = "<Term Prime> -> <Empty>"
      self.add_production(rule)
      self.empty()

  def factor(self):
    if self.current and self.current[0] == "Operator" and self.current[1] == "-":
      rule = "<Factor> -> - <Primary>"
      self.add_production(rule)

      self.match("Operator", "-")
      self.primary()
    else:
      rule = "<Factor> -> <Primary>"
      self.add_production(rule)
      self.primary()

  def primary(self):
    rule = "<Primary> -> <Identifier> <Primary Prime> | <Integer> | ( <Expression> ) | <Real> | true | false"
    self.add_production(rule)

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
    elif token_type == "Boolean" or (token_type == "Keyword" and lexeme in ["true", "false"]):
      if token_type == "Boolean":
        self.match("Boolean")
      else:
        self.match("Keyword", lexeme)
    else:
      self.syntax_error(f"Invalid <Primary>: {token_type}, {lexeme}")

  def primaryPrime(self):
    if self.current and self.current[0] == "Separator" and self.current[1] == "(":
      rule = "<Primary Prime> -> ( <IDs> )"
      self.add_production(rule)

      self.match("Separator", "(")
      self.ids()
      self.match("Separator", ")")
    else:
      rule = "<Primary Prime> -> <Empty>"
      self.add_production(rule)
      self.empty()

  def empty(self):
    rule = "<Empty> -> epsilon"
    self.add_production(rule)

# Function to fix the identifier method in Lexical class
def fix_is_identifier(lexer_instance):
    # Override the is_identifier method with the corrected version
    def fixed_is_identifier(self, string):
        if not string or not (string[0].isalpha() or string[0] == '_'):
            return False
        for ch in string:
            if not (ch.isalnum() or ch == '_'):
                return False
        if string in self.keywords:
            return False  # Keyword != Identifier
        return True

    # Attach the fixed method to the instance
    import types
    lexer_instance.is_identifier = types.MethodType(fixed_is_identifier, lexer_instance)
    return lexer_instance

# Main program with file output implementation
def main():
    # Read three test files
    filenames = ["test1.txt", "test2.txt", "test3.txt", "test4.txt"]
    all_results = ""

    for name in filenames:  # Go through each file
        try:
            with open(name, 'r') as file:  # Open the file
                input_text = file.read()  # Read the file

            # Apply the fix to lexer
            lexer = Lexical(input_text)
            fix_is_identifier(lexer)

            # Then parse and get output content
            parser = Syntax(input_text)
            try:
                output_content = parser.parse()

                file_results = f"Analysis for {name}\n"
                file_results += "="*50 + "\n\n"
                file_results += "\n".join(output_content)
                file_results += "\n\n"

                # Write to individual file
                with open(f"{name}_output.txt", 'w') as output_file:
                    output_file.write(file_results)

                # Append to combined results
                all_results += file_results

                print(f"Syntax Analyzer successfully parsed the file: {name}")

            except SyntaxError as e:
                print(f"Error parsing {name}: {e}")
                # The error will be in the output_content already

        except FileNotFoundError:
            print(f"File {name} not found")
            all_results += f"File {name} not found\n\n"

    # Write all results to a single output file
    with open("output.txt", 'w') as output_file:
        output_file.write(all_results)

    print("Combined results written to output.txt")

if __name__ == "__main__":
    main()