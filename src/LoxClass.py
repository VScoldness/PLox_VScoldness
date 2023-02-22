from LoxFunction import LoxFunction


class LoxClass:
    def __init__(self, name: str, methods: dict[str, LoxFunction]) -> None:
        self.name = name
        self.methods = methods

    def call(self, interpreter, arguments: list[object]) -> object:
        instance = LoxInstance(self)

        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def find_method(self, name: str) -> LoxFunction:
        return self.methods.get(name, None)

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer:
            return initializer.arity()
        return 0

    def __str__(self) -> str:
        return self.name


class LoxInstance:
    def __init__(self, lox_class: LoxClass):
        self.lox_class = lox_class
        self.fields = {}

    def get(self, name: str) -> object:
        if name in self.fields:
            return self.fields[name]

        method = self.lox_class.find_method(name)
        if method:
            return method.bind(self)

        raise Exception(f"undefined property {name}.")

    def set(self, name: str, val: object) -> None:
        self.fields[name] = val

    def __str__(self):
        return self.lox_class.name + " instance"


