
import re


class Preprocessor:

    @staticmethod
    def run(code):
        return re.sub(r"/\*.*?\*/", '', code, flags=re.DOTALL)
