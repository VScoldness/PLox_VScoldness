import AST
from Token import TokenType
from Environment import Environment
from LoxFunction import LoxFunction


class Interpreter(AST.VisitorExpr):
    def __init__(self):
        self.global_env = Environment()

    def interpreter(self, ast_list: list[AST]):
        for ast in ast_list:
            self.__evaluate(ast)

    def __evaluate(self, expr: AST.AST) -> object:
        return expr.accept(self)

    def visit_block(self, block: AST.Block) -> None:
        self.execute_block(block, Environment(self.global_env))

    def execute_block(self, block: AST.Block, env: Environment):
        global_env = self.global_env
        self.global_env = env
        for stmt in block.stmts:
            self.__evaluate(stmt)
        self.global_env = global_env

    def visit_for(self, for_stmt: AST.ForStmt):
        self.__evaluate(for_stmt.initialization)
        while self.__evaluate(for_stmt.condition):
            self.__evaluate(for_stmt.body)
            self.__evaluate(for_stmt.increment)

    def visit_while(self, while_stmt: AST.WhileStmt) -> None:
        while self.__evaluate(while_stmt.condition):
            self.__evaluate(while_stmt.body)

    def visit_if(self, ifStmt: AST.IfStmt) -> None:
        if self.__evaluate(ifStmt.condition):
            self.__evaluate(ifStmt.if_block)
        else:
            if ifStmt.else_block:
                self.__evaluate(ifStmt.else_block)

    def visit_print(self, print_stmt: AST.PrintStmt) -> None:
        val = self.__evaluate(print_stmt.val)
        print(val)

    def visit_func(self, func_decl: AST.FuncDecl) -> None:
        func = LoxFunction(func_decl, self.global_env)
        self.global_env.declare_variable(func_decl.name, func)

    def visit_var_decl(self, var: AST.VarDecl) -> None:
        val = None
        if var.val:
            val = self.__evaluate(var.val)
        self.global_env.declare_variable(var.name, val)

    def visit_assign(self, assign: AST.Assign) -> None:
        val = self.__evaluate(assign.val)
        self.global_env.assign_variable(assign.name, val)

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
            case "or": return left or right
            case "and": return left and right
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

    def visit_call(self, call_expr: AST.Call) -> object:
        callee = self.__evaluate(call_expr.name)
        assert len(call_expr.arg_list) <= 255, "The maximum arguments are 255"
        arg_list = self.__evaluate_arguments(call_expr.arg_list)
        assert isinstance(callee, LoxFunction), "Can only call functions"
        assert len(arg_list) == callee.arity(), f"function has {callee.arity()} arguments, but give {len(arg_list)}"
        return callee.call(self, arg_list)

    def visit_return(self, return_stmt: AST.ReturnStmt) -> None:
        val = self.__evaluate(return_stmt.expr)
        raise Exception(val)

    def __evaluate_arguments(self, arg_list: list[AST.Expr]) -> list[object]:
        evaluated_arg_list = []
        for arg in arg_list:
            evaluated_arg = self.__evaluate(arg)
            evaluated_arg_list.append(evaluated_arg)
        return evaluated_arg_list

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
                return self.global_env.get_variable(primary.literal.val)
            case _:
                raise Exception(f"Do not support the primary datastructure {primary.literal.val}")


