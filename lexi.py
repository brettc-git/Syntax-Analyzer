import sys
class Lexical:
    def __init__(self, input):
        self.input = input #insert code
        self.pos = 0
        self.line = 1 #First line
        self.column = 1 #First letter
        self.current = self.input[0] if input else None #takes first character if not put null
        self.is_comment = False #flag used to check if there is an end to comment

        self.keywords = {"integer", "if", "else", "endif", "while", "return", "scan", "print", "endwhile", "function", "boolean", "real", "true", "false"}
        self.single_operators = {"=", "<", ">", "+", "-", "*", "/", "%"}
        self.double_operators = {"<=", "=>", "==", "!=", "**", "//"}
        self.separators = {"(", ")", "{", "}", "[", "]", ";", ",", "$"}

    def next(self): #function used to continue to next char
        self.pos += 1
        self.column += 1

        if self.pos >= len(self.input):
            self.current = None
        else:
            self.current = self.input[self.pos]
            if self.current == '\n': #if char is new line go reset column
                self.line += 1
                self.column = 0

    def peek(self):
        if self.pos + 1 >= len(self.input):
            return None
        return self.input[self.pos+1]

    def whitespace(self):
        while self.current is not None and self.current.isspace():
            self.next()

    # Checks if current word is identifier
    def is_identifier(self, string):
        if not string or not (string[0].isalpha() or string[0] == '_'): #checks if first char is letter if not return false
            return False
        for ch in string:
            if not (ch.isalnum() and ch == '_'):
                return False
        if string in self.keywords:
            return False # Keyword != Identifier

        # Otherwise it is an identifier
        return True


    def is_integer(self, string):
        return string.isdigit() # returns boolean

    # Function to check if value is "real"
    def is_real(self, string):
        try:
            float(string)
            return "." in string
        except:
            return False


    def parse(self):
        tokens = []
        while self.current is not None:
            self.whitespace() #skips whitespace

            if self.current is None:
                break

            # Check for comment start and see if it consistently ends with *]
            if self.current == "[" and self.peek() == "*":
                self.is_comment = True
                self.next() # Skip "["
                self.next() # Skip "*"

                while self.current is not None:
                    if self.current == "*" and self.peek() == "]":
                        self.next() # Skip "*"
                        self.next() # Skip "]"
                        break
                    self.next()

                if self.current is None:
                    print("Unclosed comment error.")

                self.is_comment = False
                continue

            # Check for the $$ token
            if self.current == "$" and self.peek() == "$":
                tokens.append(("Separator", "$$"))
                self.next()
                self.next()
                continue

            # Check for separators that are single characters
            if self.current in self.separators:
                tokens.append(("Separator", self.current))
                self.next()
                continue


            # Check two character operators first (avoiding partial matches)
            if (self.current is not None) and (self.peek() is not None) and (self.current + self.peek() in self.double_operators):
                tokens.append(("Operator", self.current + self.peek()))
                self.next()
                self.next()
                continue

            # Check one character operators
            if self.current in self.single_operators:
                tokens.append(("Operator", self.current))
                self.next()
                continue

            # Case for identifiers and keywords
            if self.current is not None and (self.current.isalpha() or self.current == "_"):
                identifier = ""
                while self.current is not None and (self.current.isalnum() or self.current == "_"):
                    identifier += self.current
                    self.next()

                if identifier in self.keywords:
                    if identifier in ["true", "false"]:
                        tokens.append(("Boolean", identifier))
                    else:
                        tokens.append(("Keyword", identifier))
                else:
                    tokens.append(("Identifier", identifier))
                continue

            # Case for numbers
            if self.current is not None and self.current.isdigit():
                number = ""
                num_isReal = False

                while self.current is not None and (self.current.isdigit() or self.current == "."):
                    if self.current == ".":
                        if num_isReal:
                            break
                        num_isReal = True
                    number += self.current
                    self.next()

                if num_isReal:
                    tokens.append(("Real", number))
                else:
                    tokens.append(("Integer", number))
                continue

            if self.current is not None:
                tokens.append(("Unknown", self.current))
                self.next()

        return tokens



# Open three files first

# filenames = ["test1.txt", "test2.txt", "test3.txt"]
# result = "" #created a string to put all results of each test case into one
# for name in filenames: # Go through each file
#     # val = 1
#     try:
#         with open(name, 'r') as file: # Open file
#             data = file.read()
#             l = Lexical(data)
#             tokens = l.parse()
#             result += name + '\n'
#             result += f"{'token':<15}{'lexeme':<15}\n"
#             result += "-"*30
#             result += '\n'
#             for tokentype, lexeme in tokens:
#                 result += f"{tokentype:<15}{lexeme:<15}\n"

#         # val += 1
#     except FileNotFoundError:
#         print(f"File {name} not found")

# with open("Lexi_output.txt", 'w') as file:
#     file.write(result)
