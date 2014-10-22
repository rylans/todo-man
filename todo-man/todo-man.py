#!/usr/bin/env python
'''todo-man.py
Extracts 'TODOs' from source code and renders them in markdown

Author: Rylan Santinon
'''
import argparse
import os
import re
import textwrap
#TODO: Level 0 todo

from todo import Todo
from sourcecodeline import SourceCodeLine

class FileHandler:
  ignores = ['build', 'bin', 'dst', 'dest', 'dist', 'node_modules','bower_components']

  def __init__(self):
    pass

  def get_files(self, file_suffix):
    file_list = []
    for root, dirs, files in os.walk('.'):
      for f in files:
	if f.endswith(file_suffix):
	  file_list.append(os.path.join(root, f))

    ignored_files = []
    for z in file_list:
      for ignore in FileHandler.ignores:
	if self.in_insensitive(ignore, z):
	  ignored_files.append(z)

    return [file for file in file_list if file not in ignored_files]

  def in_insensitive(self, item, item_list):
    """Returns true if item is in item_list by comparing without case

    >>> FileHandler().in_insensitive('a', ['B','A','D'])
    True

    >>> FileHandler().in_insensitive('a', ['B','D'])
    False

    >>> FileHandler().in_insensitive('foo', 'afOobar')
    True

    >>> FileHandler().in_insensitive('foo', 'afXobar')
    False
    """
    if type(item_list) == type(''):
      return item.lower() in item_list.lower()
    for list_item in item_list:
      if self.cmp_insensitive(list_item, item):
	return True
    return False

  def cmp_insensitive(self, str1, str2):
    """Returns true if str1 and str2 are equal by comparing without case

    >>> FileHandler().cmp_insensitive('AbC', 'aBc')
    True

    >>> FileHandler().cmp_insensitive('AdC', 'aBc')
    False
    """
    return str1.lower() == str2.lower()

  def write_todos(self, todo_list, output_file, is_md):
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

def get_todos(file_list):
  """Get TODOs from a list of input files"""
  todo_list = []
  for file_ in file_list:
    with open(file_, 'r') as f:
      line_num = 0
      for line in f.readlines():
	line_num += 1
	sc_line = SourceCodeLine(line, line_num, file_)
	if sc_line.has_todo():
	  todo_list.append(sc_line.get_todo())
  return todo_list


#ToDo: USED FOR TESTING
def todoman(output_md, file_suffix, md):
  '''Get files, get ToDos in files then write them out

  >>> todoman('__test.md', 'py', False)
  >>> with open('__test.md') as f:
  ...	any(['[ ] USED FOR TESTING' in line for line in f.readlines()])
  True

  >>> todoman('__test.md', 'py', True)
  >>> with open('__test.md') as f:
  ...	any(['* USED FOR TESTING' in line for line in f.readlines()])
  True

  >>> try:
  ...	os.remove('__test.md')
  ... except OSError:
  ...	pass
  '''
  handler = FileHandler()
  files = handler.get_files(file_suffix)
  todos = get_todos(files)
  handler.write_todos(todos, output_md, md)

def main():
  desc = '''Get TODO comments from source code file and put them into a Markdown file

  Examples:
    To find all TODOs in Javascript files and put them into TODO.md:
      $ todo-man.py js

    To find all TODOs in Python files and output them using Markdown into TODO.md:
      $ todo-man.py --md TODO.md py

    To search Ruby files for TODOs and output into 'output.md':
      $ todo-man.py output.md rb
  '''
  parser = argparse.ArgumentParser(description=textwrap.dedent(desc), formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('out', metavar='O', nargs='?', default='TODO.md', help='The markdown file to write TODOs to')
  parser.add_argument('file_type', metavar='T', nargs=1, help='The file suffix of source code files (ex: py, js, java)')
  parser.add_argument('--md', dest='md_format', metavar='M', nargs='?', const=True, default=False, help='Use markdown (Default is Github-flavored markdown)')
  #TODO: Make an argument '-f' to force the output file to get overwritten
  args = parser.parse_args()

  context = (args.out, args.file_type[0], args.md_format)
  todoman(*context)

if __name__ == '__main__':
  #TODO: Import logging and use it
  import doctest
  doctest.testmod()
  main()
