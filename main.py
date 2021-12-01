import scanner 
import interpreter
from print_ast import AstPrinter
from parser import Parser  
import sys
from tokens.TokenType import TokenType
from tokens.token import Token



class GuardML:
    def __init__(self, scanner=None) -> None:
        self.had_error = False
        self.scanner = scanner
        self.interpreter = interpreter.Interpreter()
    def run_file(self, file_path):
        with open(file_path, 'r') as f:
            source_code = f.read() 

            self.run(source_code)

    def repl(self):
        while True: 
            line = input("gml~ ")
            if line == "exit":
                break
            self.run(line)

    def run(self, source):
        if self.scanner == None:
            self.scanner = scanner.Scanner(source, self)
        tokens = list(self.scanner.scan_tokens() )
        parser = Parser(tokens) 
        expr = parser.parse() 
        
        if self.had_error:
            sys.exit(65)

        print(expr)
    def error(self, line: int, kind="", err_message=None):
        self.report_error(line, kind, err_message)
        self.had_error = True

    def report_error(self, line, kind, err_message):
        print(f"<Line {line}> Error {kind}: {err_message}")

    def error(self, token: Token, err_message: str): 
        if token.type == TokenType.EOF:
            self.report_error(token.line, " at end", err_message) 
        else: 
            self.report_error(token.line, " at ", token.lexeme + "'", err_message)


if __name__ == "__main__":
    gml = GuardML()
    gml.repl()