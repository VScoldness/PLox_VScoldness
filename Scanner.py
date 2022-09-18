from Token import Token, TokenType


class Scanner:
    def __init__(self, source_code: str) -> None:
        self.start = 0
        self.current = 0
        self.source_code = source_code
        self.token_list = []

    def scan(self) -> list[Token]:
        while not self.__atEnd():
            char = self.__advance()
            match char:
                case "+":
                    self.token_list.append(self.__tokenize(TokenType.ADD, "+"))
                case "-":
                    self.token_list.append(self.__tokenize(TokenType.ADD, "-"))
                case "*":
                    self.token_list.append(self.__tokenize(TokenType.ADD, "*"))
                case "/":
                    self.token_list.append(self.__tokenize(TokenType.ADD, "/"))
                case _:
                    pass
        self.token_list.append(self.__tokenize(TokenType.EOF, " "))
        return self.token_list

    def __advance(self) -> str:
        self.current += 1
        return self.source_code[self.current - 1]

    def __peek(self) -> str:
        return self.source_code[self.current]

    def __atEnd(self) -> bool:
        return self.current >= len(self.source_code)

    @staticmethod
    def __tokenize(type: TokenType, val: object) -> Token:
        return Token(type, val)
