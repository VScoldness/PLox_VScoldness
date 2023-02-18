from enum import Enum


class TokenType(Enum):
    # single characters
    ADD = 0
    MINUS = 1
    STAR = 2
    DIVISION = 3
    COMMA = 4
    SEMICOLON = 5
    LEFT_BRACKET = 6
    RIGHT_BRACKET = 7
    LEFT_PAREN = 8
    RIGHT_PAREN = 9
    DOT = 10

    # single or double characters
    LESS = 20
    LESS_EQUAL = 21
    GREATER = 22
    GREATER_EQUAL = 23
    EQUAL = 24
    EQUAL_EQUAL = 25
    NOT = 26
    NOT_EQUAL = 27

    # keywords
    FUN = 30
    FOR = 31
    WHILE = 32
    IF = 33
    ELSE = 34
    AND = 35
    OR = 36
    TRUE = 37
    FALSE = 38
    NIL = 39
    VAR = 40
    PRINT = 41
    RETURN = 42
    CLASS = 43

    # literals
    STRING = 50
    NUMBER = 51
    IDENTIFIER = 52

    EOF = 100


class Token:
    def __init__(self, type: TokenType, val: object) -> None:
        self.type = type
        self.val = val

    def __str__(self) -> str:
        return f"Type: {self.type}, Val: {self.val}"
