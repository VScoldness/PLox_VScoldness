import AST
from Environment import Environment


class LoxFunction:
    def __init__(self, func: AST.FuncDecl, closure: Environment) -> None:
        self.func = func
        self.closure = closure

    def call(self, interpreter, arg_list: list[object]) -> None:
        prev_env = self.closure
        func_env = Environment(self.closure)
        for idx in range(len(arg_list)):
            func_env.declare_variable(self.func.arg_list[idx], arg_list[idx])
        try:
            interpreter.execute_block(self.func.body, func_env)
        except Exception as err:
            self.closure = prev_env
            return err.args[0]
        return

    def arity(self) -> int:
        return len(self.func.arg_list)
