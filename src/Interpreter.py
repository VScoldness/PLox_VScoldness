import AST
from Token import TokenType


class Interpreter(AST.VisitorExpr):
    def __init__(self):
        pass

    def interpreter(self, ast_list: list[AST]):
        for ast in ast_list:
            print(self.__evaluate(ast))

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
            case ">": return left > right
            case ">=": return left >= right
            case "<": return left < right
            case "<=": return left <= right
            case _:
                raise f"not support binary operator {binary.operator}"

    def visit_unary(self, unary: AST.Unary) -> object:
        if unary.operator == "!":
            return not self.__evaluate(unary.right)
        elif unary.operator == "-":
            return -1 * self.__evaluate(unary.right)
        else:
            print("Here")
            raise Exception("only support '-' and '!' in the unary operation")

    def visit_primary(self, primary: AST.Primary) -> object:
        match primary.literal.type:
            case TokenType.STRING:
                return primary.literal.val
            case TokenType.NUMBER:
                return primary.literal.val
            case TokenType.FALSE:
                return False
            case TokenType.TRUE:
                return True


