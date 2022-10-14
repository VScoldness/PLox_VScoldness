import AST
from Token import TokenType
from Environment import Environment


class Interpreter(AST.VisitorExpr):
    def __init__(self):
        self._global = Environment()

    def interpreter(self, ast_list: list[AST]):
        for ast in ast_list:
            self.__evaluate(ast)

    def __evaluate(self, expr: AST.AST):
        return expr.accept(self)

    def visit_print(self, print_stmt: AST.PrintStmt) -> None:
        val = self.__evaluate(print_stmt.val)
        print(val)

    def visit_var_decl(self, var: AST.VarDecl) -> None:
        val = None
        if var.val:
            val = self.__evaluate(var.val)
        self._global.declare_variable(var.name, val)

    def visit_assign(self, assign: AST.Assign) -> None:
        val = self.__evaluate(assign.val)
        self._global.assign_variable(assign.name, val)

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
            case TokenType.IDENTIFIER:
                return self._global.get_variable(primary.literal.val)
            case _:
                raise Exception(f"Do not support the primary datastructure {primary.literal.val}")


