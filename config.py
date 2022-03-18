import os
try:
    token = os.environ["AutoVulnBotToken"]
except KeyError:
    token = input("Token: ")
