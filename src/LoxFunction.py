import AST
from Environment import Environment


class LoxFunction:
    def __init__(self, func: AST.FuncDecl, closure: Environment, is_initializer: bool) -> None:
        self.func = func
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, lox_instance):
        env = Environment(self.closure)
        env.declare_variable("this", lox_instance)
        return LoxFunction(self.func, env, self.is_initializer)

    def call(self, interpreter, arg_list: list[object]) -> object:
        prev_env = self.closure
        func_env = Environment(self.closure)
        for idx in range(len(arg_list)):
            func_env.declare_variable(self.func.arg_list[idx], arg_list[idx])
        try:
            interpreter.execute_block(self.func.body, func_env)
        except Exception as err:
            if self.is_initializer:
                return self.closure.getAt(0, "this")
            self.closure = prev_env
            return err.args[0]

        if self.is_initializer:
            return self.closure.getAt(0, 'this')

    def arity(self) -> int:
        return len(self.func.arg_list)
