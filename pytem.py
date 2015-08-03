#!/bin/env python3
from __future__ import print_function
import re, os, shutil, sys, markdown

def print_err(*args):
  print(*args, file=sys.stderr)

def get_subdir(dirs):
  subdirs = dirs.split(os.sep)[1:] # return subdirectory path exclduing the root directory
  return os.sep.join(subdirs)

def md_files_only(src,names):
  ignore = [ n for n in names if n.endswith('.md') ]
  return ignore

def files_only(src,names):
  if src.endswith("res"): # Copy files from resource folders
    return []
  else: # Otherwise, only copy directories.
    return [ name for name in names if not os.path.isdir(os.path.join(src,name))] # return only the directories in src

def create_tree(src,dst): # Create directory tree from src in dst
  try:
    shutil.copytree(src,dst,ignore=md_files_only) # If directory doesn't exist yet, just make it.
  except FileExistsError as e: # If directory already exists, prompt before deleting.
    sys.stdout.write("%s exists, Overwrite (y/n) "%dst)
    overwrite = input()
    if overwrite == 'y' or overwrite == 'Y':
      print_err("Deleting %s"%dst)
      shutil.rmtree(dst)
      print_err("Creating directories")
      shutil.copytree(src,dst,ignore=md_files_only)
    else: # Exit with error if not overwriting.
      print_err("Directory exists, not overwriting, exiting.")
      sys.exit(-1)

if len(sys.argv) != 4: # print usage instructions if any parameters are missing.
  print("Usage: %s <templatedir> <indir> <outdir>"%sys.argv[0])
  sys.exit(-1)

templatedir = sys.argv[1]
indir = sys.argv[2]
outdir = sys.argv[3]

create_tree(indir,outdir) # Recreate directory tree of indir under outdir

templates = {}
for fn in os.listdir(templatedir):
  if fn.endswith('.html'): # Check for .html file extension
    fpath = os.path.join(templatedir,fn)
    with open(fpath, 'r') as f: # Read template
      data = f.read()
    basename = os.path.splitext(fn)[0] # Remove file extension
    templates[basename] = data # Associate template with name

# iterate through all subdirectories under root.
for root, subdirs, filenames in os.walk(indir):
  for fn in filenames:
    if fn.endswith('.md'): # read all files ending in .md
      filepath = os.path.join(root,fn)
      with open(filepath, 'r') as df:
        datafile = df.read()
      
      try: # Check for data/content delimiter (---)
        (data,content) = datafile.split('---')
      except:
        raise Exception("Bad file format, missing content, or content divider (---).")
      

      # --- Parse input file for tags and content ---
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

      # --- Place values and content into template ---
      try:      
        output = templates[tags['template']]
      except: # Skip file if no template found.
        print_err("ERROR on %s: Template not found"%fn)
        continue
      p = re.compile(r'`(.*)`') # regex to find all tags between a pair of backticks
      for m in p.finditer(output): # find all tags in the template
        tag = m.group(1)
        try: # replace tag with value
          output = re.sub('`('+tag+')`',tags[tag],output)
        except: # default to blank value
          output = re.sub('`('+tag+')`',"",output)

      # --- write content to output file ---
      outname=os.path.splitext(fn)[0]+".html" # Replace .md with .html
      subdir=get_subdir(root)
      outpath=os.path.join(outdir,subdir,outname)
      print_err(filepath+" -> "+outpath)
      with open(outpath, 'w') as o:
        o.write(output)
