
def Rat25S():
  pass 

def optFunctionDefinitions():
  pass

def functionDefinitions():
  pass
  
def function():
  pass

def optParameterList():
  pass 

def parameterList(): 
  print("<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>")
  
def parameter():
  print("<Parameter> -> <IDs> <Qualifier>")

def qualifier():
  print("<Qualifier> -> integer | boolean | real")
  
def body():
  print("<Body> -> { <Statement List> }")

def optDeclarationList():
  print("<Opt Declaration List> -> <Declaration List> | <Empty>")
  
def declarationList():
  print("<Declaration List> -> <Declaration> ; | <Declaration> ; <Declaration List>")

def declaration():
  print("<Declaration> -> <Qualifier><IDs>")

def ids():
  print("<IDs> -> <Identifier> | <Identifier>, <IDs>")

def statementList():
  print("<Statement List> -> <Statement> | <Statement> <Statement List>")
  
def statement():
  print("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")

def compound():
  print("<Compound> -> { <Statement List> }")

def assign():
  print("<Assign> ::= <Identifier> -> <Expression>")

def _if():
  pass

def ifPrime():
  pass

def _return():
  pass 
  
def returnPrime():
  pass

def _print():
  pass

def scan():
  print("<Scan> -> scan(<IDs>);")

def _while():
  print("<While> -> while ( <Condition> ) <Statement> endwhile")

def condition():
  print("<Condition> -> <Expression> <Relop> <Expression>")

def relop():
  print("<Relop> -> == | != | > | < | <= | =>")

def expression():
  print("<Expression> -> <Term> <Expression Prime>")

def expressionPrime():
  pass

def term():
  print("<Term> -> <Factor><Term Prime>")

factor()
termPrime()

def termPrime():
  print("<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime> | epsilon")
  

def factor():
  print("<Factor> ::= - <Primary> | <Primary>")

def primary():
  pass

def primaryPrime():
  pass 
  
def empty():
  print("<Empty> -> epsilon")
