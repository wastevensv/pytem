#!/bin/env python
from __future__ import print_function
import re, os, sys, markdown

if len(sys.argv) != 3: # print usage instructions if any parameters are missing.
  print("Usage: pytem.py <templatefile> <sitedir>")
  quit()

with open(sys.argv[1], 'r') as f:
  template= f.read()

# iterate through all subdirectories under root.
for root, subdirs, filenames in os.walk(sys.argv[2]):
  for fn in filenames:
    if fn.endswith('.md'): # read all files ending in .md
      filepath = os.path.join(root,fn)
      with open(filepath, 'r') as df:
        datafile = df.read()
      
      try: # Check for data/content delimiter ---
        (data,content) = datafile.split('---')
      except:
        raise Exception("Bad file format, missing content, or content divider (---).")
      
      tags = {}
      for line in data.split('\n'): # Read file line by line
        p = line.split(':') # Pairs are written as tag : value (1 per line)
        if len(p) != 2: # If the line has any more than two parts, its not a valid pair.
          continue
        (tag, value) = (p[0], p[1])
        tag = tag.strip() # remove whitespace from tags and values
        value = value.strip()
        tags[tag] = value # place pair in dictionary
      
      tags['content'] = content # remainder of file is markdown formatted content (HTML is valid too)
      tags['content'] = markdown.markdown(tags['content'])
      
      
      output = template
      p = re.compile(r'`(.*)`') # regex to find all tags between a pair of backticks
      for m in p.finditer(template): # find all tags in the template
        tag = m.group(1)
        try: # replace tag with value
          output = re.sub('`('+tag+')`',tags[tag],output)
        except: # default to blank value
          output = re.sub('`('+tag+')`',"",output)
      
      outname=os.path.splitext(fn)[0]+".html" # Replace .md with .html
      outpath=os.path.join(root,outname)
      print(filepath+" -> "+outpath)
      with open(outpath, 'w') as o:
        o.write(output)
