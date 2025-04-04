
def Rat25S():
  pass 

def optFunctionDefinitions():
  pass

def functionDefinitions():
  pass
  
def function():
  print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")

def optParameterList():
  print("<Opt Parameter List> -> <Parameter List> | <Empty>")

  parameterList()
  empty()

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

  qualifier()
  ids()

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
  print("<If> -> if(<Condition>)<Statement> <If Prime>")

def ifPrime():
  print("<If Prime> -> endif | else <Statement> endif")

def _return():
  print("<Return> -> return <Return Prime>")
  
def returnPrime():
  print("<Return Prime> -> ; | <Expression> ;")

def _print():
  print("<Print> ::= print ( <Expression>);")

def scan():
  print("<Scan> -> scan(<IDs>);")

def _while():
  print("<While> -> while ( <Condition> ) <Statement> endwhile")

def condition():
  print("<Condition> -> <Expression> <Relop> <Expression>")
  expression()
  relop()
  expression()

def relop():
  print("<Relop> -> == | != | > | < | <= | =>")

def expression():
  print("<Expression> -> <Term> <Expression Prime>")
  term()
  expressionPrime()

def expressionPrime():
  print("Expression Prime -> +<Term><Expression Prime> | -<Term><Expression Prime> | empty")

def term():
  print("<Term> -> <Factor><Term Prime>")

  factor()
  termPrime()

def termPrime():
  print("<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime> | empty")
  
  empty()
  

def factor():
  print("<Factor> ::= - <Primary> | <Primary>")

def primary():
  pass

def primaryPrime():
  pass 
  
def empty():
  print("<Empty> -> epsilon")
