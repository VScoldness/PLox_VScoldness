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
            expr = self.__stmt()
            ast_list.append(expr)
        return ast_list

    def __stmt(self) -> AST.AST:
        if self.__match(Token.TokenType.PRINT):
            return self.__print_stmt()
        else:
            return self.__exprStmt()

    def __exprStmt(self) -> AST.Expr:
        expr = self.__expression()
        assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after expression"
        return expr

    def __print_stmt(self):
        self.__advance()
        expr = self.__expression()
        assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after print statement"
        return AST.PrintStmt(expr)

    def __expression(self) -> AST.Expr:
        expr = self.__logic_or()
        # assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after expression"
        return expr

    def __logic_or(self) -> AST.Expr:
        return self.__logic_and()

    def __logic_and(self) -> AST.Expr:
        return self.__equality()

    def __equality(self) -> AST.Expr:
        expr = self.__comparison()
        while self.__match(Token.TokenType.EQUAL_EQUAL, Token.TokenType.NOT_EQUAL):
            operator = self.__advance()
            right = self.__comparison()
            expr = AST.Binary(expr, right, operator.val)
        return expr

    def __comparison(self) -> AST.Expr:
        expr = self.__term()
        while self.__match(Token.TokenType.GREATER, Token.TokenType.GREATER_EQUAL,
                           Token.TokenType.LESS, Token.TokenType.LESS_EQUAL):
            operator = self.__advance()
            right = self.__term()
            expr = AST.Binary(expr, right, operator.val)
        return expr

    def __term(self) -> AST.Expr:
        expr = self.__factor()
        while self.__match(Token.TokenType.ADD, Token.TokenType.MINUS):
            operator = self.__advance()
            right = self.__factor()
            expr = AST.Binary(expr, right, operator.val)
        return expr

    def __factor(self) -> AST.Expr:
        expr = self.__unary()
        while self.__match(Token.TokenType.STAR, Token.TokenType.DIVISION):
            operator = self.__advance()
            right = self.__unary()
            expr = AST.Binary(expr, right, operator.val)
        return expr

    def __unary(self) -> AST.Expr:
        if self.__match(Token.TokenType.MINUS, Token.TokenType.NOT):
            operator = self.__advance()
            right = self.__unary()
            return AST.Unary(operator.val, right)
        return self.__primary()

    def __call(self) -> AST.Expr:
        pass

    def __primary(self) -> AST.Expr:
        cur_token = self.__advance()
        match cur_token.type:
            case Token.TokenType.IDENTIFIER:
                pass
            case Token.TokenType.LEFT_PAREN:
                expr = self.__expression()
                assert self.__advance().type == Token.TokenType.RIGHT_PAREN, "Expect ')' after expression"
                return expr
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

    def __match(self, *args) -> bool:
        for arg in args:
            if arg == self.__peek().type:
                return True
        return False

