class Environment:
    def __init__(self, parent=None) -> None:
        self.variables = {}
        self.parent = parent

    def declare_variable(self, name: str, val: object) -> None:
        self.variables[name] = val

    def assign_variable(self, name: str, val: object) -> None:
        if name in self.variables:
            self.variables[name] = val
            return
        if self.parent:
            self.parent.assign_variable(name, val)
            return
        raise Exception(f"Can not assign a non-exist variable: {name}. Declare it first!!!")

    def get_variable(self, name: str) -> object:
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_variable(name)
        raise Exception(f"Variable {name} not in the environment")

