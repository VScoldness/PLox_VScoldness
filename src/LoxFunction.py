import AST
from Interpreter import Interpreter
from Environment import Environment


class LoxFunction:
    def __init__(self, func: AST.FuncDecl) -> None:
        self.func = func

    def call(self, interpreter: Interpreter, arg_list: list[AST.Expr]) -> None:
        func_env = Environment(interpreter.global_env)
        for idx in range(len(arg_list)):
            func_env.declare_variable(self.func.arg_list[idx], arg_list[idx])
        interpreter.execute_block(self.func.body, func_env)

    def arity(self) -> int:
        return len(self.func.arg_list)
