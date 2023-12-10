from format_translators import translation
from typing import List

class Protocol(object):

    def __init__(self, roles, algebra, name, ):
        self.algebra = algebra
        self.name = name
        self.roles = roles
        self.proto = self.__build()

    def __build(self) -> str:
        proto = f"(defprotocol {self.name} {self.algebra}\n\t"
        for r in self.roles:
            proto += r.final + '\n'
        proto += ')'
        return proto