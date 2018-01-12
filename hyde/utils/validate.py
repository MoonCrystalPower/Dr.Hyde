import re

def isEmail(email):
    return re.search(r'[\w.-]+@[\w.-]+\.[\w.]+', email)
