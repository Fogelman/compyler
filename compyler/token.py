class Token:
    def __init__(self, value, type):
        self.type = type
        self.value = value

    def __str__(self):
        return f"{self.type}:{self.value}"
