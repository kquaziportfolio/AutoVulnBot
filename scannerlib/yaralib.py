import yara
import os

# Generate the rules by traversing the scannerlib/rules directory
# Algo:
#    Iterate through OS.WALK
#    Iterate through files recieved
#    If FILE ends with .YARA, add it to DEFAULT_RULES with key as the complete file name
NOSCAN = ["macho.yara"]
DEFAULT_RULES = {}
for dirpath, _, files in os.walk(os.path.join("scannerlib", "rules")):
    for i in files:
        if i.endswith(".yara") and i not in NOSCAN:
            DEFAULT_RULES[os.path.join(dirpath, i)] = os.path.join(dirpath, i)


class YaraScanner:
    """
Main YARASCANNER class
Only implements two methods: __init__ and scandata
Useful for scanning many documents from a consistent set of yara rules
    """

    def __init__(self, rulelist=None):
        if rulelist is None:
            rulelist = DEFAULT_RULES
        self.rules = yara.compile(filepaths=rulelist)

    def scandata(self, data):
        return self.rules.match(data=data)
