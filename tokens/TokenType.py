from enum import Enum, auto

class TokenType(Enum):
    #single characters
    LPAREN = auto() 
    RPAREN = auto() 
    LBRACE = auto() 
    RBRACE = auto() 
    COMMA = auto() 
    DOT = auto() 
    MINUS = auto() 
    PLUS = auto() 
    SEMICOLON = auto() 
    SLASH = auto() 
    STAR = auto() 

    #1+ characters 
    BANG = auto() 
    BANG_EQUAL = auto() 
    EQUAL = auto() 
    EQUAL_EQUAL = auto() 
    GREATER = auto() 
    GREATER_EQUAL = auto() 
    LESS = auto() 
    LESS_EQUAL = auto() 

    #literals 
    IDENT = auto() 
    STRING = auto() 
    NUMBER = auto() 

    #keywords
    AND = auto() 
    CLASS = auto() 
    IF = auto() 
    ELSE = auto() 
    TRUE = auto() 
    FALSE = auto() 
    FUN = auto() 
    FOR = auto() 
    WHILE = auto()
    OR = auto() 
    SHOW = auto() 
    VAR = auto() 


    LET = auto() 
    GUARD = auto()
    EOF = auto() 
    NIL = auto()
    RETURN = auto()
