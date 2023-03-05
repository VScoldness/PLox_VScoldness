import AST
from Token import TokenType
from Environment import Environment
from LoxFunction import LoxFunction
from LoxClass import LoxClass, LoxInstance


class Interpreter(AST.VisitorExpr):
    def __init__(self):
        self.global_env = Environment()
        self.locals = {}

    def interpreter(self, ast_list: list[AST]):
        for ast in ast_list:
            self.__evaluate(ast)

    def __evaluate(self, expr: AST.AST) -> object:
        return expr.accept(self)

    def visit_class(self, class_dec: AST.Class) -> None:
        superclass = None
        if class_dec.superclass:
            superclass = self.__evaluate(class_dec.superclass)
            assert isinstance(superclass, LoxClass), "Superclass must be a class."
        self.global_env.declare_variable(class_dec.name, None)

        if class_dec.superclass:
            self.global_env = Environment(self.global_env)
            self.global_env.declare_variable('super', superclass)

        methods = {}
        for method in class_dec.methods:
            class_method = LoxFunction(method, self.global_env, method.name == 'init')
            methods[method.name] = class_method
        new_class = LoxClass(class_dec.name, superclass, methods)
        if superclass:
            self.global_env = self.global_env.parent
        self.global_env.assign_variable(class_dec.name, new_class)

    def visit_block(self, block: AST.Block) -> None:
        self.execute_block(block, Environment(self.global_env))

    def execute_block(self, block: AST.Block, env: Environment):
        global_env = self.global_env
        try:
            self.global_env = env
            for stmt in block.stmts:
                self.__evaluate(stmt)
        finally:
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
        func = LoxFunction(func_decl, self.global_env, False)
        self.global_env.declare_variable(func_decl.name, func)

    def visit_var_decl(self, var: AST.VarDecl) -> None:
        val = None
        if var.val:
            val = self.__evaluate(var.val)
        self.global_env.declare_variable(var.name, val)

    def visit_assign(self, assign: AST.Assign) -> object:
        val = self.__evaluate(assign.val)
        distance = self.locals.get(assign)
        if distance:
            self.global_env.assignAt(distance, assign.name, val)
        else:
            self.global_env.assign_variable(assign.name, val)
        return val

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
        assert isinstance(callee, (LoxFunction, LoxClass)), "Can only call functions and class"
        assert len(arg_list) == callee.arity(), f"function has {callee.arity()} arguments, but give {len(arg_list)}"
        return callee.call(self, arg_list)

    def visit_return(self, return_stmt: AST.ReturnStmt) -> None:
        val = self.__evaluate(return_stmt.expr)
        raise Exception(val)

    def visit_get(self, obj: AST.Get) -> object:
        lox_obj = self.__evaluate(obj.obj)
        if isinstance(lox_obj, LoxInstance):
            return lox_obj.get(obj.name)
        raise Exception("Only LoxInstance has properties")

    def visit_set(self, expr: AST.Set) -> object:
        obj = self.__evaluate(expr.expr)
        if not isinstance(obj, LoxInstance):
            raise Exception("Only instances have fields.")
        val = self.__evaluate(expr.val)
        obj.set(expr.name, val)
        return val

    def visit_this(self, this: AST.This) -> object:
        return self.__look_up_variable(this.keyword, this)

    def visit_super(self, lox_super: AST.Super) -> object:
        distance = self.locals[lox_super.keyword]
        superclass = self.global_env.getAt(distance-1, 'super')
        assert isinstance(superclass, LoxClass), "Super can only be used in a class"
        obj = self.global_env.getAt(distance-2, 'this')
        method = superclass.find_method(lox_super.method)

        if not method:
            raise Exception(f"Undefined property: {lox_super.method}.")
        return method.bind(obj)

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
                return self.global_env.get_variable(str(primary.literal.val))
            case _:
                raise Exception(f"Do not support the primary datastructure {primary.literal.val}")

    def visit_variable(self, var: AST.Variable):
        return self.__look_up_variable(str(var.name.val), var)

    def __look_up_variable(self, name: str, expr: AST.Expr) -> object:
        distance = self.locals.get(expr)
        if distance:
            return self.global_env.getAt(distance, name)
        else:
            return self.global_env.get_variable(name)

    def resolve(self, expr: AST.Expr, distance: int):
        self.locals[expr] = distance

