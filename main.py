import sys
if len(sys.argv) < 2:
    raise Exception("Missing Argument")

cmd = sys.argv[1]
items = []
token = ""
for i in cmd:
    if i.isdigit():
        token += i
    else:
        if token != "":
            items.append(token)
            token = ""

        if (i == "+" or i == "-"):
            items.append(i)

if token != "":
    items.append(token)

try:
    num = int(items[0])
    result = num
except:
    raise Exception("Invalid Operation")

op = None
for item in items[1:]:
    isdigit = item.isdigit()

    if not isdigit and op is None:
        op = item
    elif op is not None:
        num = int(item)
        if op == "+":
            result += num
        elif op == "-":
            result -= num
        else:
            raise Exception("Invalid Operation")
        op = None
    else:
        raise Exception("Invalid Operation")

if op is not None:
    raise Exception("Invalid Operation")

print(result)
