# pytem
A minimal, no logic, python template script.

## Command Syntax
```bash
./pytem.py template in out
```

## Input File Format
```
  template : post
  title : Notes
  tag1 : value1
  tag2 : value2
  ---
  
  Markdown formatted content
```

## Template file format
There is no standard file format for templates. Except that text surrounded by backticks (\`) \`like this\` is treated as a tag.
Tags are replaced by the corresponding value from the input file. The \`content\` tag is replaced by the markdown-compiled-to-html
content below the three dashes (---) in the input file.
