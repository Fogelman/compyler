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
    ';': "SEMI"
}


class Tokenizer:
    def __init__(self, origin, position=0, actual=None):
        self.origin = origin
        self.position = position
        self.actual = actual
        self._lenght = len(origin)

    def _find(self, pattern, flags=0):
        match = pattern.match(self.origin[self.position:], flags)

        if match is None:
            raise Exception(
                f"[-] could not decode character at position {self.position}")
        return match.group()

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
        elif self.origin[self.position].isalpha():
            pattern = re.compile(r"^(\becho)|^(\bwhile)", re.IGNORECASE)
            string = self._find(pattern)
            self.actual = Token(string, "COMMAND")
        elif self.origin[self.position] in tokens:
            actual = self.origin[self.position]
            self.actual = Token(actual, tokens[actual])
        else:
            raise Exception(
                f"[-] could not decode character at position {self.position}")

        self.position += len(self.actual.value)
