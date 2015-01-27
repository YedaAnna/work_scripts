#! usr/bin/python3
import os

for fn in os.listdir():
    if ".pdb" in fn:
        sub = {}
        with open(fn, 'r') as f:
            for line in f:
                c = line.split()
                if len(c) > 5 and c[0] == "ATOM":
                    sub[c[4]] = 0
        print(fn, len(sub.keys()))
