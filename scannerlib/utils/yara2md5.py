# Extracts MD5 meta elements from yara files (not perfect, doesn't capture multiple md5 meta categories and the like)
# Used to generate the current malhash file (with some manual adjustments)

import sys

with open(sys.argv[1]) as f:
    a = f.readlines()

b = []

for i in a:
    i = "".join(i.split())
    if i.startswith("md5=\""):
        for j in i.removeprefix("md5=\"").removesuffix('"').split(","):
            b.append(j)

with open(sys.argv[2], "w") as f:
    for i in b:
        f.write("MD5 " + i + "\n")
