from Token import Token


class AST:
    def accept(self, visitor) -> object:
        pass


class Stmt(AST):
    def __init__(self) -> None:
        pass


class Expr(AST):
    pass


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


