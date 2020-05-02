import os
import json
import re
from compyler.token import Token


tokens = {
    "+": "PLUS",
    "-": "MINUS",
    "/": "DIVIDE",
    "*": "MULTIPLY",
    "(": "OPEN",
    ")": "CLOSE",
    '{': "LBRACE",
    '}': "RBRACE",
    '=': "EQUAL",
    ';': "SEMI",
    '>': "GREATER",
    '<': "LESS",
    '!': "NOT",
    '.': "CONCAT"

}


class Tokenizer:
    def __init__(self, origin, position=0, actual=None):
        self.origin = origin
        self.position = position
        self.actual = actual
        self._lenght = len(origin)
        self.reserved = re.compile(
            r"^(\becho)|^(\bwhile)|^(\bif)|^(\breadline)|^(\belse)|^(\band)|^(\bor)|^(==)|^(>=)|^(<=)|^(!=)", re.IGNORECASE)

        self.boolean = re.compile(r"^(\btrue)|^(\bfalse)", re.IGNORECASE)

        self.tags = re.compile(r"^(\<\?php)|^(\?\>)")

        self.string = re.compile(r"^(\"[^\"]*\")")

    def _find(self, pattern, flags=0, error=True):
        match = pattern.match(self.origin[self.position:], flags)

        if match is None and error:
            raise Exception(
                f"[-] could not decode character at position {self.position}")
        elif match is None:
            return None

        return match.group()

    def _check(self, pattern, flags=0):
        match = pattern.search(self.origin[self.position:], flags)
        if match is None:
            return False
        return True

    def selectNext(self):
        self._lenght = len(self.origin)
        for i in self.origin[self.position:]:
            if i.strip() == "":
                self.position += 1
            else:
                break

        if self.position >= self._lenght:
            self.actual = Token("", "EOF")
        elif self.origin[self.position].isdigit():
            pattern = re.compile(r"^\d+", re.IGNORECASE)
            digit = self._find(pattern)
            self.actual = Token(digit, "INT")
        elif self.origin[self.position] == "$":
            pattern = re.compile(r"^\$[a-z]+[_a-z0-9]*", re.IGNORECASE)
            string = self._find(pattern)
            self.actual = Token(string, "IDENTIFIER")
        elif self._check(self.boolean):
            string = self._find(self.boolean)
            self.actual = Token(string.upper(), "BOOLEAN")
        elif self._check(self.reserved):
            string = self._find(self.reserved)
            self.actual = Token(string.upper(), "RESERVED")
        elif self._check(self.tags):
            string = self._find(self.tags)
            self.actual = Token(string.upper(), "TAGS")
        elif self.origin[self.position] == "\"":
            string = self._find(self.string)
            self.actual = Token(string.upper(), "STRING")
        elif self.origin[self.position] in tokens:
            actual = self.origin[self.position]
            self.actual = Token(actual, tokens[actual])

        else:
            raise Exception(
                f"[-] could not decode character at position {self.position}")
        self.position += len(self.actual.value)
