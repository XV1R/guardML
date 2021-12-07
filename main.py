#!/usr/bin/python3
import scanner 
import interpreter
from print_ast import AstPrinter
from parser import Parser  
import sys
import os 
from tokens.TokenType import TokenType
from tokens.token import Token
from argparse import ArgumentParser



class GuardML:
    def __init__(self, scanner=None) -> None:
        self.had_error = False
        self.scanner = scanner
        self.interpreter = interpreter.Interpreter()


    def run_file(self, file_path, output=None):
        try:
            with open(file_path, 'r') as f:
                source_code = f.read() 
                print(f.readline())
                self.run(source_code, output)
        except: 
            print("Failure opening input file.")

    def repl(self):
        while True: 
            line = input("gml~ ")
            if line == "exit":
                break
            self.run(line)

    def run(self, source, output=None):
        if self.scanner == None:
            self.scanner = scanner.Scanner(source, self)
        tokens = list(self.scanner.scan_tokens() )
        parser = Parser(tokens) 
        expr = parser.parse() 
        
        if self.had_error:
            sys.exit(65)
        if output == None:
            printer = AstPrinter()
            for ex in expr:
                print(ex)
            for token in tokens:
                print(token)
        else: 
            with open(output, "w") as f:
                f.write(expr) 
                f.write(tokens) 
                print(f"Generated {output} file.")

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

def generate_parser(): 
    parser = ArgumentParser(description="GuardML language")
    parser.add_argument("action", help="Main action to take.", choices=["repl", "build"])
    parser.add_argument("-f", "--file", type=str, default=None,help="Source file")
    parser.add_argument("-o", "--output", help="Output file name. Defaults to 'out.gml'.", type=str, default=f"{os.getcwd()}/out.gml") 

    return parser 


if __name__ == "__main__":
    gml = GuardML()
    arg_parser = generate_parser() 
    args = arg_parser.parse_args()
    match args.action:
        case "repl":
            gml.repl() 
        case "build":
            gml.run_file(args.file)
        case _:
            arg_parser.print_help() 