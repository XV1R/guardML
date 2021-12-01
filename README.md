![imagen](https://user-images.githubusercontent.com/47250976/142684199-10b1923b-a1be-497e-a48d-a668f2209a60.png)


# GuardML-Language
CIIC4020/ICOM3046 Programming Languages project 

## Introduction 
When considering security in software, many of the vulnerabilities found come back to fundamental engineering issues. From old issues like buffer overflows in C and SQL injections in PHP, to more modern attacks like XSS in javascript; these issues come down to developers having to account for their respective tooling and it's accompanying vulnerabilities. According to the OWASP API Top 10, the most common issues involving API’s and general web development come down to issues with configuration and implementation. Like the Rust language addressing memory issues, GuardML attempts to model a modern declarative scripting language for API development that takes care of these vulnerabilities for you. 

By being declarative, GuardML abstracts most implementation details, helping protect from mistakes done by developers and helps make it easier to use and read. Developers can provide their ideal API by description and not focus on the language’s syntax or compiler details. It’s syntax is greatly inspired by the ML family of languages (in particular OCaml and ReasonML), as they leverage declarative styles and are generally easy to understand. 

# Languages Features: 
*GuardML’s features include:*
- Declarative syntax
- General purpose with extra features for API development
- Transpiling to python for ease of development
- Functional paradigm
- Secure development environment

# Implementention requirements: 
Currently, the team plans on using OCaml as the implementation language for the project. This is because as GuardML is heavily inspired by OCaml and the other ML languages, the conversion between the two is much more direct, and easier to implement. We’d also be taking advantage of OCaml’s extensive type system, as well as ease of reading. This is also an opportunity for the team to get more deeply familiar with the functional paradigm as a whole, and approach the project with a new light. 

## *In order for the language to be implemented, it needs:*
 Ocaml installed
- Comes with its lexing api
- Ocamllex
- ocamlyacc

# Example Program:

```
-- This is a comment
--* This is a multiline comment *--

-- resulting value doesn't have to have ; 
let add (x: int, y: int): int = {x + y};

let result: int = add(2,3)

show(result);

let other_result: int = {
    let first_arg =3;
    let second_arg = 10;
    add(first_arg, second _arg) 
};

 -- value stays as an expression and does not become 5 
 let value = guard(2+3);
```
# Reference Manual

## Intructions to execute de program 
-We create a Docker hub repository to work in the project: https://hub.docker.com/r/xv1r/guardml

-Download Docker Desktop application <code>https://hub.docker.com/</code> and in the terminal execute this commands:
````
docker pull xv1r/guardml:1.0
docker image ls (to see the image)
docker run xv1r/guardml:1.0

````
-Download VisualStudio Code and in extensions download <code>Remote - Containers</code> this will detect the folder for the project 

-In VisualStudio Code go to <code>clone git repository</code> and enter the URL of the repository <code>https://github.com/JonathanFigueroa1/GuardML-Language.git</code>

Note: This project was developed using Python Lex-Yacc. Therefore, you must have Python 3.10 installed on your computer.

# Lexer 
The GuardML Program have the following <code>reserved_keywords</code> 
````
reserved_keywords = { 
    "if" : "IF", 
    "elif" : "ELIF", 
    "else": "ELSE", 
    "while": "WHILE",
    "for": "FOR",
    "let" : "LET", 
    "show": "SHOW", 
    "guard" : "GUARD",
    "int" : "INT",
    "string": "STRING",
    "bool": "BOOLEAN"
}
````
## Literals
````
literals = "{}-+;/*=()[]><':" + '"'
````
## Tokens 
````
tokens = [
    #Single-character tokens.
    'LPAREN','RPAREN','LBRACKET','RBRACKET','LBRACE','RBRACE',
    'COMMA','DOT','MINUS','PLUS','COLON','SEMICOLON','SLASH','STAR',

    #BANG = !
    #One or two character tokens
    'AND', 'OR',
    'TRUE', 'FALSE',
    'BANG','BANG_EQUAL',
    'EQUAL','EQUAL_EQUAL',
    'GREATER','GREATER_EQUAL',
    'LESS','LESS_EQUAL',

    #Literals 
    'IDENTIFIER','NUMBER',

    #Keywords
    # 'AND','CLASS','ELSE','FALSE','FUN','FOR','IF','NIL','OR',
    # 'PRINT','RETURN','SUPER','THIS','TRUE','VAR','WHILE',

    'EOF'
] + list(reserved_keywords.values())
````
# Parser 
Some of the Grammar Rules for statements and functions:
````
def p_statement(self, t):
        '''
        statement : function SEMICOLON
                | expression SEMICOLON
                | IDENTIFIER EQUAL expression SEMICOLON
                | IDENTIFIER EQUAL function SEMICOLON
                | LET IDENTIFIER EQUAL GUARD SEMICOLON
                | LET IDENTIFIER EQUAL NUMBER SEMICOLON
                | GUARD SEMICOLON
                | SHOW LPAREN STRING RPAREN SEMICOLON
                | SHOW function
                | SHOW function SEMICOLON
                | if_statement
                | while_loop_statement
                | for_loop_statement
        '''


    # Parser for functions
    def p_function(self, t):
        '''
        function : LET IDENTIFIER COLON IDENTIFIER EQUAL function
                | LET IDENTIFIER LPAREN parameters RPAREN LBRACKET do RBRACKET
        '''
````

# Project Timeline:
![imagen](https://user-images.githubusercontent.com/47250976/142682740-f64fe058-92e1-4627-8773-e76e09399f0b.png)

# Contributors
- Xavier A. Rosado
- Osvaldo E. Aquino Santana
- Jonathan Figueroa Perez



