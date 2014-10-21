#!/usr/bin/env python
'''todo-man.py
Extracts 'TODOs' from source code and renders them in markdown

Author: Rylan Santinon
'''
import argparse
import os
#TODO: put in docstring

class Todo:
  def __init__(self, filepath, line_number, text):
    self.filepath = filepath
    self.line_number = str(line_number)
    self.text = text

  def __repr__(self):
    return '[' + ','.join([self.filepath, self.line_number, self.text]) + ']'

def in_insensitive(item, item_list):
  """Returns true if item is in item_list by comparing without case

  >>> in_insensitive('a', ['B','A','D'])
  True

  >>> in_insensitive('a', ['B','D'])
  False

  >>> in_insensitive('foo', 'afOobar')
  True

  >>> in_insensitive('foo', 'afXobar')
  False
  """
  if type(item_list) == type(''):
    return item.lower() in item_list.lower()
  for list_item in item_list:
    if cmp_insensitive(list_item, item):
      return True
  return False

def cmp_insensitive(str1, str2):
  """Returns true if str1 and str2 are equal by comparing without case

  >>> cmp_insensitive('AbC', 'aBc')
  True

  >>> cmp_insensitive('AdC', 'aBc')
  False
  """
  return str1.lower() == str2.lower()

def get_files(suffix):
  ignores = ['build', 'bin', 'dst', 'dest', 'dist']
  file_list = []
  for root, dirs, files in os.walk('.'):
    for f in files:
      if f.endswith(suffix):
	file_list.append(os.path.join(root, f))

  ignored_files = []
  for z in file_list:
    for ignore in ignores:
      if in_insensitive(ignore, z):
	ignored_files.append(z)

  return [file for file in file_list if file not in ignored_files]

def get_todos(file_list):
  todo_list = []
  for file_ in file_list:
    with open(file_, 'r') as f:
      i = 0
      for line in f.readlines():
	i += 1
	#TODO: Use a regular expression instead
	if 'TODO:' in line:
	  if len(line.strip().split('TODO')[0]) <= 2:
	    todo = line.split('TODO:')[1].strip()
	    todo_list.append(Todo(file_, i, todo))
  return todo_list

def write_todos(todo_list, output_file, is_md):
  wrote = {}
  gfm_prefix = "- [ ] "
  md_prefix = "* "

  if is_md:
    prefix = md_prefix
  else:
    prefix = gfm_prefix

  #TODO: Sort todo_list by file and line number
  with open(output_file, 'w') as f:
    f.write("#TODO List\n")
    
    for todo in todo_list:
      key = todo.text + todo.line_number
      if not wrote.get(key):
	f.write(prefix)
	f.write(todo.text + " ")
	f.write( "(" + todo.filepath + ":" + todo.line_number + ")\n")
	wrote[key] = key

def main():
  parser = argparse.ArgumentParser(description='Process.')
  parser.add_argument('out', metavar='O', nargs='?', default='TODO.md', help='The markdown file to write TODOs to')
  parser.add_argument('file_type', metavar='T', nargs=1, help='The file suffix of source code files (ex: py, js, java)')
  parser.add_argument('--md', dest='md_format', metavar='M', nargs='?', const=True, default=False, help='Use markdown (Default is Github-flavored markdown)')
  #TODO: Make an argument '-f' to force the output file to get overwritten
  #TODO: Make an argument for whether the output file is markdown or github-flavored markdown
  args = parser.parse_args()

  output_md = args.out
  file_suffix = args.file_type[0]
  md = args.md_format

  files = get_files(file_suffix)
  todos = get_todos(files)

  write_todos(todos, output_md, md)

if __name__ == '__main__':
  #TODO: Import logging and use it
  import doctest
  doctest.testmod()
  main()
