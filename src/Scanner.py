from Token import Token, TokenType


class Scanner:
    def __init__(self, source_code: str) -> None:
        self.start = 0
        self.current = 0
        self.source_code = source_code
        self.token_list = []
        self.keywords = self.__keywords()

    @staticmethod
    def __keywords() -> dict[str, TokenType]:
        keyword = {"fun": TokenType.FUN, "for": TokenType.FOR, "while": TokenType.WHILE, "if": TokenType.IF,
                   "else": TokenType.ELSE, "and": TokenType.AND, "or": TokenType.OR, "true": TokenType.TRUE,
                   'false': TokenType.FALSE, 'nil': TokenType.NIL, 'var': TokenType.VAR}
        return keyword

    def scan(self) -> list[Token]:
        while not self.__atEnd():
            char = self.__advance()
            match char:
                case " ":
                    pass
                case "\t":
                    pass
                case "\r":
                    pass
                case "\n":
                    pass
                case "(":
                    self.__add_token(self.__tokenize(TokenType.LEFT_PAREN, "("))
                case ")":
                    self.__add_token(self.__tokenize(TokenType.RIGHT_PAREN, ")"))
                case "{":
                    self.__add_token(self.__tokenize(TokenType.LEFT_BRACKET, "{"))
                case "}":
                    self.__add_token(self.__tokenize(TokenType.RIGHT_BRACKET, "}"))
                case ",":
                    self.__add_token(self.__tokenize(TokenType.COMMA, ","))
                case ";":
                    self.__add_token(self.__tokenize(TokenType.SEMICOLON, ";"))
                case "+":
                    self.__add_token(self.__tokenize(TokenType.ADD, "+"))
                case "-":
                    self.__add_token(self.__tokenize(TokenType.MINUS, "-"))
                case "*":
                    self.__add_token(self.__tokenize(TokenType.STAR, "*"))
                case "/":
                    self.__add_token(self.__tokenize(TokenType.DIVISION, "/"))
                case "<":
                    if self.__peek() == "=":
                        self.__add_token(self.__tokenize(TokenType.LESS_EQUAL, "<="))
                        self.__advance()
                    else:
                        self.__add_token(self.__tokenize(TokenType.LESS, "<"))
                case ">":
                    if self.__peek() == "=":
                        self.__add_token(self.__tokenize(TokenType.GREATER_EQUAL, ">="))
                        self.__advance()
                    else:
                        self.__add_token(self.__tokenize(TokenType.GREATER, ">"))
                case "=":
                    if self.__peek() == "=":
                        self.__add_token(self.__tokenize(TokenType.EQUAL_EQUAL, "=="))
                        self.__advance()
                    else:
                        self.__add_token(self.__tokenize(TokenType.EQUAL, "="))
                case "!":
                    if self.__peek() == "=":
                        self.__add_token(self.__tokenize(TokenType.NOT_EQUAL, "!="))
                        self.__advance()
                    else:
                        self.__add_token(self.__tokenize(TokenType.NOT, "!"))
                case "'":
                    self.__add_token(self.__string())
                case _:
                    if char.isdigit():
                        token = self.__number()
                        self.__add_token(token)
                    elif char.isalpha():
                        token = self.__identifier()
                        self.__add_token(token)
                    else:
                        raise Exception(f"Invalid syntax: {char}")
            self.start = self.current
        self.token_list.append(self.__tokenize(TokenType.EOF, " "))
        return self.token_list

    def __identifier(self) -> Token:
        while self.__peek().isalpha():
            self.__advance()
        string = self.source_code[self.start: self.current]
        type = self.keywords.get(string, TokenType.IDENTIFIER)
        return self.__tokenize(type, string)

    def __number(self) -> Token:
        while self.__peek().isdigit() or self.__peek() == ".":
            self.__advance()
        val = float(self.source_code[self.start:self.current])
        return self.__tokenize(TokenType.NUMBER, val)

    def __string(self) -> Token:
        while self.__peek() != "'":
            self.__advance()
        self.__advance()
        string = self.source_code[self.start: self.current]
        return self.__tokenize(TokenType.STRING, string)

    def __advance(self) -> str:
        self.current += 1
        return self.source_code[self.current - 1]

    def __peek(self) -> str:
        if self.__atEnd():
            return "\0"
        return self.source_code[self.current]

    def __atEnd(self) -> bool:
        return self.current >= len(self.source_code)

    @staticmethod
    def __tokenize(type: TokenType, val: object) -> Token:
        return Token(type, val)

    def __add_token(self, token: Token) -> None:
        self.token_list.append(token)
