import os


class Node:
    def __init__(self, node_name):
        self.__node_name = node_name
    
    def name(self):
        return self.__node_name

    def run_command(self, cmd):
        return os.system(cmd)

    def run_commands(self, *cmds):
        for i in cmds:
            code = os.system(i)
            if code != 0:
                return code
