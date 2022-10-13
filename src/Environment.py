class Environment:
    def __init__(self) -> None:
        self.variables = {}

    def declare_variable(self, name: str, val: object) -> None:
        self.variables[name] = val

    def assign_variable(self, name: str, val: object) -> None:
        assert name in self.variables, f"Can not assign a non-exist variable: {name}. Declare it first!!!"
        self.variables[name] = val

    def get_variable(self, name) -> object:
        assert name in self.variables, f"Variable {name} not in the environment"
        return self.variables[name]
