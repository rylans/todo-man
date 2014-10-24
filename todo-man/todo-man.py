#!/usr/bin/env python
'''todo-man.py
Extracts 'TODOs' from source code and renders them in markdown

Author: Rylan Santinon
'''
import argparse
import textwrap
import os
#TODO: Level 0 todo

from todo import Todo
from sourcecodeline import SourceCodeLine
from filehandler import FileHandler

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

  >>> todoman('__test.md', 'js', False)
  >>> with open('__test.md') as f:
  ...	ln = len(f.readlines())
  >>> ln == 1
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
  args = parser.parse_args()

  context = (args.out, args.file_type[0], args.md_format)
  todoman(*context)

if __name__ == '__main__':
  #TODO: Import logging and use it
  import doctest
  doctest.testmod()
  main()
