#!/usr/bin/env python3
print("Content-type: text/html\n")
import cgi, sys
import os
from hashlib import md5
BASE_DIR = os.path.abspath('.')

form = cgi.FieldStorage()

filename = form.getvalue('filename')
password = form.getvalue('password')
text = form.getvalue('text')

if not (filename and password and text):
    print('Invalid parameters.')
    sys.exit()
if md5(password.encode()).hexdigest() != md5('root1234'.encode()).hexdigest():
    print('Invalid password')
    sys.exit()
f = open(os.path.join(BASE_DIR,filename), 'w')
f.write(text)
f.close()
print('The file has been saved.')
