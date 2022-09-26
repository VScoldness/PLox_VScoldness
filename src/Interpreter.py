import AST
import Token


class Interpreter(AST.VisitorExpr):
    def __init__(self):
        self.ast_list = None

    def interpreter(self, ast_list: list[AST]):
        self.ast_list = ast_list

    def __evaluate(self, expr: AST.Expr):
        return expr.accept(self)

    def visit_binary(self, binary: AST.Binary):
        left = self.__evaluate(binary.left)
        right = self.__evaluate(binary.right)
        match binary.operator:
            case "+": return left + right
            case "-": return left - right
            case "*": return left * right
            case '/': return left / right
            case _:
                raise "only support '+ - * /' now"

    def visit_unary(self, unary: AST.Unary) -> object:
        if unary.operator == Token.TokenType.NOT:
            return not self.__evaluate(unary.right)
        elif unary.operator == Token.TokenType.MINUS:
            return -1 * self.__evaluate(unary.right)
        else:
            raise "only support '-' and '!' in the unary operation"

    def visit_primary(self, primary: AST.Primary) -> object:
        match primary.literal.type:
            case Token.TokenType.NUMBER:
                return float(primary.literal.val)


