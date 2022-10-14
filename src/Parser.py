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
            expr = self.__declaration()
            ast_list.append(expr)
        return ast_list

    def __declaration(self) -> AST.AST:
        if self.__match(Token.TokenType.VAR):
            return self.__var_decl()
        else:
            return self.__stmt()

    def __var_decl(self):
        self.__advance()
        name = self.__advance().val
        val = None
        if self.__match(Token.TokenType.EQUAL):
            self.__advance()
            val = self.__expression()
        assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after var statement"
        return AST.VarDecl(name, val)

    def __stmt(self) -> AST.AST:
        if self.__match(Token.TokenType.PRINT):
            return self.__print_stmt()
        elif self.__match(Token.TokenType.LEFT_BRACKET):
            return self.__block()
        elif self.__match(Token.TokenType.IF):
            return self.__if_stmt()
        else:
            return self.__exprStmt()

    def __block(self) -> AST.Block:
        self.__advance()
        stmts = []
        while not self.__match(Token.TokenType.RIGHT_BRACKET):
            stmt = self.__declaration()
            stmts.append(stmt)
            if self.__at_end():
                raise Exception("Program ends inside a block!!!")
        self.__advance()
        return AST.Block(stmts)

    def __exprStmt(self) -> AST.Expr:
        expr = self.__expression()
        assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after expression"
        return expr

    def __if_stmt(self) -> AST.IfStmt:
        condition = self.__if_condition()
        if_block = self.__if_block()
        else_block = self.__else_block()
        return AST.IfStmt(condition, if_block, else_block)

    def __if_condition(self) -> AST.Expr:
        self.__advance()
        assert self.__advance().type == Token.TokenType.LEFT_PAREN, "Expect '(' after if word"
        assert self.__peek().type != Token.TokenType.RIGHT_PAREN, "The condition in if statement is empty!!!"
        condition = self.__logic_or()
        assert self.__advance().type == Token.TokenType.RIGHT_PAREN, "Expect ')' after if condition"
        return condition

    def __if_block(self) -> AST.Block:
        if not self.__match(Token.TokenType.LEFT_BRACKET):
            raise Exception("Expect '{' after if condition statement")
        if_block = self.__block()
        return if_block

    def __else_block(self) -> AST.Block:
        else_block = None
        if self.__match(Token.TokenType.ELSE):
            self.__advance()
            if not self.__match(Token.TokenType.LEFT_BRACKET):
                raise Exception("Expect '{' after else statement")
            else_block = self.__block()
        return else_block

    def __print_stmt(self) -> AST.PrintStmt:
        self.__advance()
        expr = self.__expression()
        assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after print statement"
        return AST.PrintStmt(expr)

    def __expression(self) -> AST.Expr:
        return self.__assign()

    def __assign(self) -> AST.Expr:
        if self.__match(Token.TokenType.IDENTIFIER) and self.__next().type == Token.TokenType.EQUAL:
            name = self.__advance().val
            assert self.__advance().type == Token.TokenType.EQUAL, "Expect '=' after variable name in assign expression"
            val = self.__logic_or()
            # assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after assign expression"
            return AST.Assign(name, val)
        else:
            return self.__logic_or()

    def __logic_or(self) -> AST.Expr:
        left = self.__logic_and()
        while self.__match(Token.TokenType.OR):
            self.__advance()
            right = self.__logic_and()
            left = AST.Binary(left, right, 'or')
        return left

    def __logic_and(self) -> AST.Expr:
        left = self.__equality()
        while self.__match(Token.TokenType.AND):
            self.__advance()
            right = self.__equality()
            left = AST.Binary(left, right, 'and')
        return left

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
                return AST.Primary(cur_token)
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

    def __next(self) -> Token.Token:
        if self.__at_end():
            return self.tokens[-1]
        return self.tokens[self.current + 1]

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

