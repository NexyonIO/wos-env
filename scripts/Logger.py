from scripts.Node import Node
import scripts.termcolor as termcolor


class Logger:
    def __init__(self, context, prefix=None):
        self.context = context
        self.prefix = prefix
    
    def __prefix(self):
        if self.prefix is None:
            return ""
        return f"[{self.prefix}] "

    def panic(self, fmt, *args, exit_code=None):
        print(termcolor.colored(f"{self.__prefix()}[{self.context} | panic]", 'red'), fmt, *args)

        if exit_code is not None:
            exit(exit_code)

    def info(self, fmt, *args):
        print(termcolor.colored(f"{self.__prefix()}[{self.context} | info]", 'cyan'), fmt, *args)

    def warn(self, fmt, *args):
        print(termcolor.colored(f"{self.__prefix()}[{self.context} | warn]", 'yellow'), fmt, *args)

    def get_from_node(self, node: Node):
        return Logger(self.context, node.name())
