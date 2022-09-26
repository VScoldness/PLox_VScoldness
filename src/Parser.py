import AST
import Token


class Parser:
    def __init__(self) -> None:
        self.tokens = None
        self.current = None

    def parse(self, tokens: list[Token.Token]) -> list[AST.AST]:
        self.current = 0
        self.tokens = tokens
        ast_list = []
        while not self.__at_end():
            self.__advance()
            expr = self.__expression()
            ast_list.append(expr)
        return ast_list

    def __expression(self) -> AST.Expr:
        expr = self.__logic_or()
        assert (self.__advance().type == Token.TokenType.SEMICOLON, "Expect a ';' after expression")
        return expr

    def __logic_or(self) -> AST.Expr:
        return self.__logic_and()

    def __logic_and(self) -> AST.Expr:
        return self.__equality()

    def __equality(self) -> AST.Expr:
        return self.__comparison()

    def __comparison(self) -> AST.Expr:
        return self.__term()

    def __term(self) -> AST.Expr:
        left = self.__factor()
        token = self.__peek()
        while token.type == Token.TokenType.ADD or token.type == Token.TokenType.MINUS:
            self.__advance()
            right = self.__term()
            return AST.Binary(left, right, token.val)
        return left

    def __factor(self) -> AST.Expr:
        left = self.__unary()
        token = self.__peek()
        while token.type == Token.TokenType.STAR or token.type == Token.TokenType.DIVISION:
            self.__advance()
            right = self.__factor()
            return AST.Binary(left, right, token.val)
        return left

    def __unary(self) -> AST.Expr:
        token = self.__previous()
        while token.type == Token.TokenType.MINUS or token.type == Token.TokenType.NOT:
            self.__advance()
            return AST.Unary(token.val, self.__unary())
        return self.__primary()

    def __call(self) -> AST.Expr:
        pass

    def __primary(self) -> AST.Expr:
        cur_token = self.__previous()
        match cur_token.type:
            case Token.TokenType.IDENTIFIER:
                pass
            case Token.TokenType.LEFT_PAREN:
                pass
            case _:
                return AST.Primary(cur_token)

    def __peek(self) -> Token.Token:
        return self.tokens[self.current]

    def __previous(self) -> Token.Token:
        return self.tokens[self.current - 1]

    def __advance(self) -> Token.Token:
        if self.__at_end():
            return self.tokens[-1]
        self.current += 1
        return self.tokens[self.current - 1]

    def __at_end(self) -> bool:
        return self.current == len(self.tokens) - 1
