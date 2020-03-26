import sys
import os
import re
from compyler import _run as run

path = sys.argv[1]

pattern = re.compile(r".*?\.php")
if pattern.search(path) is None:
    raise Exception("[-] invalid input file")

with open(os.path.abspath(path), "r") as file:
    code = file.read()

print(run(code))
