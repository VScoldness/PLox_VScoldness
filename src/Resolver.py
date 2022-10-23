import AST


class Resolver(AST.VisitorExpr):
    def __init__(self, interpreter) -> None:
        self.interpreter = interpreter
        self.scopes = []

    def resolve(self, ast) -> None:
        ast.accept(self)

    def __resolve_block(self, stmts: list[AST.Stmt]) -> None:
        for stmt in stmts:
            self.resolve(stmt)

    def __resolve_local(self, expr: AST.Expr) -> None:
        for i in range(len(self.scopes)-1, -1, -1):
            if expr.name.val in self.scopes[i]:
                self.interpreter.resolve(expr)
                return

    def visit_block(self, block: AST.Block) -> None:
        self.__begin_scope()
        self.__resolve_block(block.stmts)
        self.__end_scope()

    def visit_var_decl(self, var: AST.VarDecl) -> None:
        self.__declare(var.name)
        if var.val:
            self.resolve(var.val)
        self.__define(var.name)

    def visit_variable(self, var: AST.Variable) -> None:
        if self.scopes and self.scopes[-1].get(var.name, None) == False:
            raise Exception(f"Can not read local variable {var.name} in its own initializer.")

    def visit_assign(self, assign: AST.Assign) -> None:
        self.resolve(assign.val)
        self.__resolve_local(assign)

    def visit_func(self, func_decl: AST.FuncDecl) -> None:
        self.__declare(func_decl.name)
        self.__define(func_decl.name)
        self.__resolve_func(func_decl)

    def __resolve_func(self, func_decl: AST.FuncDecl) -> None:
        self.__begin_scope()
        for para in func_decl.arg_list:
            self.__declare(para)
            self.__define(para)
        self.resolve(func_decl.body)
        self.__end_scope()

    def visit_if(self, ifStmt: AST.IfStmt) -> None:
        self.resolve(ifStmt.condition)
        self.resolve(ifStmt.if_block)
        if ifStmt.else_block:
            self.resolve(ifStmt.else_block)

    def visit_print(self, print_val: AST.PrintStmt) -> None:
        self.resolve(print_val.val)

    def visit_return(self, return_stmt: AST.ReturnStmt) -> None:
        if return_stmt.expr:
            self.resolve(return_stmt.expr)

    def visit_while(self, while_stmt: AST.WhileStmt) -> None:
        self.resolve(while_stmt.condition)
        self.resolve(while_stmt.body)

    def visit_for(self, for_stmt: AST.ForStmt) -> None:
        self.__begin_scope()
        self.resolve(for_stmt.initialization)
        self.resolve(for_stmt.condition)
        self.resolve(for_stmt.body)
        self.resolve(for_stmt.increment)
        self.__end_scope()

    def visit_call(self, call_expr: AST.Call) -> None:
        self.resolve(call_expr.name)
        for arg in call_expr.arg_list:
            self.resolve(arg)

    def visit_binary(self, binary: AST.Binary) -> None:
        self.resolve(binary.left)
        self.resolve(binary.right)

    def visit_unary(self, unary: AST.Unary) -> None:
        self.resolve(unary.right)

    def visit_primary(self, primary: AST.Primary) -> None:
        return

    def __begin_scope(self) -> None:
        self.scopes.append({})

    def __end_scope(self) -> None:
        self.scopes.pop()

    def __declare(self, name: str) -> None:
        if not self.scopes:
            return
        cur_scope = self.scopes[-1]
        assert name not in cur_scope, f"{name} is already in this scope!"
        cur_scope[name] = False

    def __define(self, name: str) -> None:
        if not self.scopes:
            return
        self.scopes[-1][name] = True


