#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Content-type: text/html\n")
import cgi, sys
import os
BASE_DIR = os.path.abspath('.')

form = cgi.FieldStorage()
filename = form.getvalue('filename')
if not filename:
    print('Please enter a file name')
    sys.exit()

text = open(os.path.join(BASE_DIR, filename)).read()
print("""
<html>
    <head> <title>Editing...</title>
    </head> 
    <body>
￼￼      <form action='save.cgi' method='POST'> 18 <b>File:</b> {}<br />
        <input type='hidden' value='{}' name='filename' />
        <b>Password:</b><br />
￼       <input name='password' type='password' /><br /> <b>Text:</b><br />
        <textarea name='text' cols='40' rows='20'>{}</textarea><br /> 
        <input type='submit' value='Save' />
        </form> 
    </body>
</html>
""".format(filename, filename, text))
