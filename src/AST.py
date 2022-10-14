from Token import Token
from typing import Optional


class AST:
    def accept(self, visitor) -> object:
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


class VarDecl(Stmt):
    def __init__(self, name: str, val: Expr) -> None:
        self.name = name
        self.val = val

    def accept(self, visitor) -> object:
        return visitor.visit_var_decl(self)


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


class Unary(Expr):
    def __init__(self, operator: object, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor) -> object:
        return visitor.visit_unary(self)


class Primary(Expr):
    def __init__(self, literal: Token) -> None:
        self.literal = literal

    def accept(self, visitor) -> object:
        return visitor.visit_primary(self)


class VisitorExpr:
    def visit_binary(self, binary: Expr):
        pass

    def visit_unary(self, unary: Expr):
        pass

    def visit_primary(self, primary: Expr):
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
    


