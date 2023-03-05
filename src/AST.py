from __future__ import annotations
from Token import Token
from typing import Optional


class AST:
    def accept(self, visitor: VisitorExpr) -> object:
        pass


class Stmt(AST):
    pass


class Expr(AST):
    pass


class Block(Stmt):
    def __init__(self, stmts: list[Stmt]) -> None:
        self.stmts = stmts

    def accept(self, visitor) -> object:
        return visitor.visit_block(self)


class FuncDecl(Stmt):
    def __init__(self, name: str, arguments: list[str], body: Block) -> None:
        self.name = name
        self.arg_list = arguments
        self.body = body

    def accept(self, visitor) -> object:
        return visitor.visit_func(self)


class ReturnStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor) -> object:
        return visitor.visit_return(self)


class VarDecl(Stmt):
    def __init__(self, name: str, val: Expr) -> None:
        self.name = name
        self.val = val

    def accept(self, visitor) -> object:
        return visitor.visit_var_decl(self)


class ForStmt(Stmt):
    def __init__(self, initialization: VarDecl, condition: Expr, increment: Expr, body: Block):
        self.initialization = initialization
        self.condition = condition
        self.increment = increment
        self.body = body

    def accept(self, visitor) -> object:
        return visitor.visit_for(self)


class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Block) -> None:
        self.condition = condition
        self.body = body

    def accept(self, visitor) -> object:
        return visitor.visit_while(self)


class IfStmt(Stmt):
    def __init__(self, condition: Expr, if_block: Block, else_block: Optional[Block]) -> None:
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def accept(self, visitor) -> object:
        return visitor.visit_if(self)


class PrintStmt(Stmt):
    def __init__(self, val: Expr) -> None:
        self.val = val

    def accept(self, visitor) -> object:
        return visitor.visit_print(self)


class Class(Stmt):
    def __init__(self, name: str, superclass: Class, methods: list[FuncDecl]) -> None:
        self.name = name
        self.methods = methods
        self.superclass = superclass

    def accept(self, visitor) -> object:
        return visitor.visit_class(self)


class Assign(Expr):
    def __init__(self, name: str, val: Expr) -> None:
        self.name = name
        self.val = val

    def accept(self, visitor) -> object:
        return visitor.visit_assign(self)


class Binary(Expr):
    def __init__(self, left: Expr, right: Expr, operator: object) -> None:
        self.left = left
        self.right = right
        self.operator = operator

    def accept(self, visitor) -> object:
        return visitor.visit_binary(self)

    def __str__(self) -> str:
        return str(self.left) + str(self.operator) + str(self.right)


class Unary(Expr):
    def __init__(self, operator: object, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor) -> object:
        return visitor.visit_unary(self)


class Call(Expr):
    def __init__(self, name: Expr, arguments: list[Expr]) -> None:
        self.name = name
        self.arg_list = arguments

    def accept(self, visitor) -> object:
        return visitor.visit_call(self)


class Get(Expr):
    def __init__(self, obj: Expr, name: str):
        self.obj = obj
        self.name = name

    def accept(self, visitor) -> object:
        return visitor.visit_get(self)


class Set(Expr):
    def __init__(self, expr: Expr, name: str, val: Expr):
        self.expr = expr
        self.name = name
        self.val = val

    def accept(self, visitor) -> object:
        return visitor.visit_set(self)


class This(Expr):
    def __init__(self, keyword: str):
        self.keyword = keyword

    def accept(self, visitor) -> object:
        return visitor.visit_this(self)


class Super(Expr):
    def __init__(self, keyword: str, method: str):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor) -> object:
        return visitor.visit_super(self)


class Primary(Expr):
    def __init__(self, literal: Token) -> None:
        self.literal = literal

    def accept(self, visitor) -> object:
        return visitor.visit_primary(self)

    def __str__(self) -> str:
        return str(self.literal.val)


class Variable(Expr):
    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor) -> object:
        return visitor.visit_variable(self)


class VisitorExpr:
    def visit_binary(self, binary: Binary):
        pass

    def visit_unary(self, unary: Unary):
        pass

    def visit_primary(self, primary: Primary):
        pass

    def visit_print(self, print_val: PrintStmt):
        pass

    def visit_var_decl(self, var: VarDecl):
        pass

    def visit_assign(self, assign: Assign):
        pass

    def visit_block(self, block: Block):
        pass

    def visit_if(self, ifStmt: IfStmt):
        pass

    def visit_while(self, while_stmt: WhileStmt):
        pass

    def visit_for(self, for_stmt: ForStmt):
        pass

    def visit_call(self, call_expr: Call):
        pass

    def visit_func(self, func_decl: FuncDecl):
        pass

    def visit_return(self, return_stmt: ReturnStmt):
        pass

    def visit_variable(self, var: Variable):
        pass

    def visit_class(self, class_dec: Class):
        pass

    def visit_get(self, obj: Get):
        pass

    def visit_set(self, expr: Set):
        pass

    def visit_this(self, this: This):
        pass

    def visit_super(self, lox_super: Super):
        pass

