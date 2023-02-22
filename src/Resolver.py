import AST
from enum import Enum


class FunctionType(Enum):
    NONE = 1
    FUNCTION = 2
    METHOD = 3
    INITIALIZER = 4


class ClassType(Enum):
    NONE = 1
    CLASS = 2


class Resolver(AST.VisitorExpr):
    def __init__(self, interpreter) -> None:
        self.interpreter = interpreter
        self.scopes = []
        self.cur_func_type = FunctionType.NONE
        self.cur_class_type = ClassType.NONE

    def resolve(self, ast_list: list[AST.AST]):
        for ast in ast_list:
            self.__resolve(ast)

    def __resolve(self, ast) -> None:
        ast.accept(self)

    def __resolve_block(self, stmts: list[AST.Stmt]) -> None:
        for stmt in stmts:
            self.__resolve(stmt)

    def __resolve_local(self, name: str) -> None:
        for i in range(len(self.scopes) - 1, -1, -1):
            if name in self.scopes[i]:
                self.interpreter.resolve(name, len(self.scopes)-1-i)
                return

    def visit_class(self, class_dec: AST.Class) -> None:
        enclosing_class = self.cur_class_type
        self.cur_class_type = ClassType.CLASS

        self.__declare(class_dec.name)
        self.__define(class_dec.name)

        self.__begin_scope()

        self.scopes[-1]['this'] = True
        for method in class_dec.methods:
            cur_func_tye = FunctionType.METHOD
            if method.name == 'init':
                cur_func_tye = FunctionType.INITIALIZER
            self.__resolve_func(method, cur_func_tye)

        self.__end_scope()
        self.cur_class_type = enclosing_class

    def visit_block(self, block: AST.Block) -> None:
        self.__begin_scope()
        self.__resolve_block(block.stmts)
        self.__end_scope()

    def visit_var_decl(self, var: AST.VarDecl) -> None:
        self.__declare(var.name)
        if var.val:
            self.__resolve(var.val)
        self.__define(var.name)

    def visit_variable(self, var: AST.Variable) -> None:
        if self.scopes and self.scopes[-1].get(var.name, None) is False:
            raise Exception(f"Can not read local variable {var.name} in its own initializer.")

    def visit_assign(self, assign: AST.Assign) -> None:
        self.__resolve(assign.val)
        self.__resolve_local(assign.name)

    def visit_func(self, func_decl: AST.FuncDecl) -> None:
        self.__declare(func_decl.name)
        self.__define(func_decl.name)
        self.__resolve_func(func_decl, FunctionType.FUNCTION)

    def __resolve_func(self, func_decl: AST.FuncDecl, func_type: FunctionType) -> None:
        enclosing_function = self.cur_func_type
        self.cur_func_type = func_type
        self.__begin_scope()
        for para in func_decl.arg_list:
            self.__declare(para)
            self.__define(para)
        self.__resolve(func_decl.body)
        self.__end_scope()
        self.cur_func_type = enclosing_function

    def visit_if(self, ifStmt: AST.IfStmt) -> None:
        self.__resolve(ifStmt.condition)
        self.__resolve(ifStmt.if_block)
        if ifStmt.else_block:
            self.__resolve(ifStmt.else_block)

    def visit_print(self, print_val: AST.PrintStmt) -> None:
        self.__resolve(print_val.val)

    def visit_return(self, return_stmt: AST.ReturnStmt) -> None:
        if self.cur_func_type == FunctionType.NONE:
            raise Exception("Can not return from top-level code.")
        if return_stmt.expr:
            if self.cur_func_type == FunctionType.INITIALIZER:
                raise Exception("Can not return a value from an initializer!")
            self.__resolve(return_stmt.expr)

    def visit_while(self, while_stmt: AST.WhileStmt) -> None:
        self.__resolve(while_stmt.condition)
        self.__resolve(while_stmt.body)

    def visit_for(self, for_stmt: AST.ForStmt) -> None:
        self.__begin_scope()
        self.__resolve(for_stmt.initialization)
        self.__resolve(for_stmt.condition)
        self.__resolve(for_stmt.body)
        self.__resolve(for_stmt.increment)
        self.__end_scope()

    def visit_call(self, call_expr: AST.Call) -> None:
        self.__resolve(call_expr.name)
        for arg in call_expr.arg_list:
            self.__resolve(arg)

    def visit_binary(self, binary: AST.Binary) -> None:
        self.__resolve(binary.left)
        self.__resolve(binary.right)

    def visit_unary(self, unary: AST.Unary) -> None:
        self.__resolve(unary.right)

    def visit_primary(self, primary: AST.Primary) -> None:
        return

    def visit_get(self, obj: AST.Get) -> None:
        self.__resolve(obj.obj)

    def visit_set(self, expr: AST.Set) -> None:
        self.__resolve(expr.val)
        self.__resolve(expr.expr)

    def visit_this(self, this: AST.This) -> None:
        if self.cur_class_type == ClassType.NONE:
            raise Exception("Can not use 'this' outside of a class")
        self.__resolve_local(this.keyword)

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
