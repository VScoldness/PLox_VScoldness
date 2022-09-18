from typing import Optional, Union
from Scanner import Scanner
from Parser import Parser
from Interpreter import Interpreter


class PLox:
    def __init__(self) -> None:
        self.parser = Parser()
        self.interpreter = Interpreter()

    def run(self, input: Optional[str]) -> None:
        if not input:
            self.repl()
        else:
            self.runFile(input)
    
    def repl(self) -> None:
        while True:
            source_code = input("> ")
            self.__run(source_code)

    def runFile(self, input: str) -> None:
        f = open(input, "r")
        source_code = f.read()
        f.close()
        self.__run(source_code)

    def __run(self, source_code: str) -> None:
        token_list = Scanner(source_code).scan()
        ast = self.parser.parse(token_list)
        self.interpreter(ast)

