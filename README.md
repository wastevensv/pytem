# pytem[![Build Status](https://travis-ci.org/wastevensv/pytem.svg?branch=master)](https://travis-ci.org/wastevensv/pytem)
A minimal, no logic, python template script.

## Command Syntax
```bash
./pytem.py template in out (globalfile)
```

## Tag File Format
```
  template : post
  title : Notes
  tag1 : value1
  tag2 : value2
  ---
  
  Markdown formatted content
```

## Template file format
There is no standard file format for templates. Except that text surrounded by percent signs (%) %like this% is treated as a tag.
Tags are replaced by the corresponding value from the input file. The %content% tag is replaced by the markdown-compiled-to-html
content below the three dashes (---) in the input file.


## API Rewrite 2015-09-27
### Class: Pytem
* Global variables:
  * indir - directory containing tag files
  * outdir - directory to place generated site
  * global_tags - dictionary of tag:value pairs for every rendered file.
  * templates - dictionary of names and template strings.
* Functions:
  * **__init__**
    * Creates a new Pytem instance
    * Calls:
      * _init_templates
      * parse_file (for globals)
    * Input:
      * templatedir - directory containing template files
      * globalfile - filename of global tags (optional)
  * **_init_templates**
    * Reads templates from templatedir. Puts them in templates dictionary.
    * NOTE: Interacts with filesystem.
  * **render_site**
    * Iterates through all files in indir to outdir and processes each one.
      * indir - directory containing tag files
      * outdir - directory to place generated site
    * NOTE: Interacts with filesystem.
  * **render_string**
    * Reads, renders, and writes a single file.
    * Input:
      * data - a string representation of a tag file.
      * html - boolean True if data is already an HTML string (default=False)
    * Globals read:
      * global_tags - Used for default value of tags.
      * templates - use template tag to determine what template to use for render_content.
    * Calls:
      * parse_string
      * render_content
    * Returns:
      * A rendered string.
  * **parse_string**
    * Takes in a tag file (as a string) and separates it into tags.
    * Input:
      * data - string representation of file
    * Returns:
      * dictionary of tag:value pairs (including content and template).
  * **render_content**
    * Takes tags and content and places them in the template.
    * Input:
      * template - the template string to render tags into.
      * tags - dictionary containing tag:value pairs (including HTML content)
    * Returns:
      * rendered page as a string.

### Class: Utils
* Functions:
  * **create_tree**
    * Creates the directory tree of indir in outdir and copies all content files.
    * Input:
      * indir
      * outdir
    * Returns:
      * Nothing
    * NOTE: Interacts with filesystem.
* NOTE: Class also includes various filters.