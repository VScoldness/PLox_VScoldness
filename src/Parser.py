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
            try:
                expr = self.__declaration()
                ast_list.append(expr)
            except Exception as err:
                print(err)
        return ast_list

    def __declaration(self) -> AST.AST:
        if self.__match(Token.TokenType.VAR):
            return self.__var_decl()
        elif self.__match(Token.TokenType.CLASS):
            return self.__class_decl()
        elif self.__match(Token.TokenType.FUN):
            self.__advance()
            return self.__func_decl()
        else:
            return self.__stmt()

    def __class_decl(self) -> AST.Class:
        self.__advance()
        name = str(self.__advance().val)
        assert self.__advance().type == Token.TokenType.LEFT_BRACKET, "Expect '{' after name in class " \
                                                                      "declaration. "
        methods = []
        while self.__peek().type != Token.TokenType.RIGHT_BRACKET and not self.__at_end():
            methods.append(self.__func_decl("method"))
        assert self.__advance().type == Token.TokenType.RIGHT_BRACKET, "Expect '}' after name in class " \
                                                                       "declaration. "
        return AST.Class(name, methods)

    def __func_decl(self, kind="") -> AST.FuncDecl:
        # self.__advance()
        name = str(self.__advance().val)
        assert self.__advance().type == Token.TokenType.LEFT_PAREN, "Expect '(' after name in function " \
                                                                    "declaration. "
        arg_list = self.__func_arg_list()
        if not self.__match(Token.TokenType.LEFT_BRACKET):
            raise Exception("Expect '{' after arguments in function declaration. ")
        body = self.__block()
        return AST.FuncDecl(name, arg_list, body)

    def __func_arg_list(self) -> list[str]:
        arg_list = []
        if self.__match(Token.TokenType.RIGHT_PAREN):
            self.__advance()
            return []
        while True:
            arg = self.__advance().val
            assert isinstance(arg, str), "All arguments in function declaration should be string !!!"
            arg_list.append(arg)
            if self.__match(Token.TokenType.RIGHT_PAREN):
                break
            assert self.__advance().type == Token.TokenType.COMMA, "Expect ',' after argument in function " \
                                                                   "declaration."
        self.__advance()
        assert len(arg_list) <= 255, "The maximum arguments are 255"
        return arg_list

    def __var_decl(self):
        self.__advance()
        name = str(self.__advance().val)
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
        elif self.__match(Token.TokenType.WHILE):
            return self.__while_stmt()
        elif self.__match(Token.TokenType.FOR):
            return self.__for_stmt()
        elif self.__match(Token.TokenType.RETURN):
            return self.__return()
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

    def __return(self) -> AST.ReturnStmt:
        self.__advance()
        expr = self.__expression()
        assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after return statement"
        return AST.ReturnStmt(expr)

    def __exprStmt(self) -> AST.Expr:
        expr = self.__expression()
        assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after expression"
        return expr

    def __for_stmt(self) -> AST.Block:
        self.__advance()
        assert self.__advance().type == Token.TokenType.LEFT_PAREN, "Expect '(' after for word"
        initialization = self.__var_decl()
        condition = self.__expression()
        assert self.__advance().type == Token.TokenType.SEMICOLON, "Expect ';' after condition in for statement"
        increment = self.__expression()
        assert self.__advance().type == Token.TokenType.RIGHT_PAREN, "Expect ')' after increment in for statement"
        if not self.__match(Token.TokenType.LEFT_BRACKET):
            raise Exception("Expect '{' after for condition statement")
        body = self.__block()
        # return AST.ForStmt(initialization, condition, increment, body)
        return AST.Block([AST.ForStmt(initialization, condition, increment, body)])

    def __while_stmt(self) -> AST.WhileStmt:
        condition = self.__while_condition()
        body = self.__while_body()
        return AST.WhileStmt(condition, body)

    def __while_condition(self) -> AST.Expr:
        self.__advance()
        assert self.__advance().type == Token.TokenType.LEFT_PAREN, "Expect '(' after while word"
        assert self.__peek().type != Token.TokenType.RIGHT_PAREN, "The condition in while statement is empty!!!"
        condition = self.__logic_or()
        assert self.__advance().type == Token.TokenType.RIGHT_PAREN, "Expect ')' after while condition"
        return condition

    def __while_body(self) -> AST.Block:
        if not self.__match(Token.TokenType.LEFT_BRACKET):
            raise Exception("Expect '{' after while condition statement")
        while_block = self.__block()
        return while_block

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
        expr = self.__logic_or()
        if self.__match(Token.TokenType.EQUAL):
            name = str(self.__previous().val)
            self.__advance()
            val = self.__assign()
            if isinstance(expr, AST.Variable):
                return AST.Assign(name, val)
            elif isinstance(expr, AST.Get):
                return AST.Set(expr.obj, expr.name, val)
            raise Exception("invalid assignment target!")
        return expr

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
        else:
            return self.__call()

    def __call(self) -> AST.Expr:
        primary = self.__primary()
        while True:
            if self.__match(Token.TokenType.LEFT_PAREN):
                arg_list = self.__call_function()
                primary = AST.Call(primary, arg_list)
            elif self.__match(Token.TokenType.DOT):
                self.__advance()
                name = str(self.__advance().val)
                primary = AST.Get(primary, name)
            else:
                break
        return primary

    def __call_function(self) -> list[AST.Expr]:
        self.__advance()
        arg_list = []
        if self.__match(Token.TokenType.RIGHT_PAREN):
            self.__advance()
            return []
        while True:
            arg_list.append(self.__expression())
            if self.__match(Token.TokenType.RIGHT_PAREN):
                break
            assert self.__advance().type == Token.TokenType.COMMA, "Expect ',' after argument in call expression."
        self.__advance()
        return arg_list

    def __primary(self) -> AST.Expr:
        cur_token = self.__advance()
        match cur_token.type:
            case Token.TokenType.IDENTIFIER:
                return AST.Variable(cur_token)
            case Token.TokenType.LEFT_PAREN:
                expr = self.__expression()
                assert self.__advance().type == Token.TokenType.RIGHT_PAREN, "Expect ')' after expression"
                return expr
            case Token.TokenType.THIS:
                keyword = str(self.__previous().val)
                return AST.This(keyword)
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
