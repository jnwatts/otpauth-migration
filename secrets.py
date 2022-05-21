#!env python3
import sys
import re
import base64

obj={}
pat=re.compile(r"^\s+(\w+): \"?(.*?)\"?$")
for line in sys.stdin:
    if line.startswith("otp_parameters"):
        obj={}
    elif line.startswith("  "):
        m=pat.search(line)
        if not m:
            continue
        if m.group(1) == "secret":
            secret_latin=m.group(2).encode('latin-1').decode("unicode_escape")
            secret_bytes=secret_latin.encode('latin-1')
            obj[m.group(1)]=base64.b32encode(secret_bytes).decode('latin-1')
        else:
            obj[m.group(1)]=m.group(2)
    elif line.startswith("}"):
        if "issuer" in obj:
            s="otpauth://{}/{}:{}?secret={}&issuer={}".format(
                    obj['type'],
                    obj['issuer'],
                    obj['name'],
                    obj['secret'],
                    obj['issuer'])
        else:
            s="otpauth://{}/{}?secret={}".format(
                    obj['type'],
                    obj['name'],
                    obj['secret'])
        if "algorithm" in obj:
            s += "&algorithm={}".format(obj['algorithm'])
        print(s)
