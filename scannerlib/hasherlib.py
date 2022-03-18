import hashlib
import os

ALGORITHMS = list(hashlib.algorithms_guaranteed)


class HashScanner:
    """
Main HASHSCANNER class'
Only implements two methods: __init__ and scandata
Useful for scanning many documents against a set of hashes of different types (SHA1, SHA256, SHA512, MD5)
    """

    def __init__(self, rulelist=os.path.join("scannerlib", "malhash.txt")):
        self.rules = []
        with open(rulelist) as f:
            for line in f.readlines():
                self.rules.append(tuple(line.split()))

    def scandata(self, data):
        outarr = list()
        if type(data) == str:
            data = data.encode()
        hashes = {}
        for algorithm in ALGORITHMS:
            key = algorithm
            try:
                value = getattr(hashlib, algorithm)(data).hexdigest()
            except TypeError:
                value = getattr(hashlib, algorithm)(data).hexdigest(64)
            hashes[key] = value
        for rule in self.rules:
            if hashes.get(rule[0].lower()) == rule[1]:
                outarr.append(rule[1])
        return outarr
