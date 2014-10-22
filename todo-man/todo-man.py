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

class Todo: #TODO: subclass object explicitly?
  def __init__(self, filepath, line_number, text):
    self.filepath = filepath
    self.line_number = str(line_number)
    self.text = text

  def __repr__(self):
    return '[' + ','.join([self.filepath, self.line_number, self.text]) + ']'

class SourceCodeLine:
  '''A line of code in a file'''
  todo_string = 'TODO:'

  def __init__(self, line, line_number, filename):
    self.line = line
    self.line_number = line_number
    self.filename = filename

  def len_before(self, span):
    before = self.line[:span[0]].strip()
    if len(before) <= 2:
      return True
    return False

  def has_todo(self):
    """Returns true if this contains a valid TODO comment

    >>> SourceCodeLine('#todo: rethink this', 39, 'abc.py').has_todo()
    True

    >>> SourceCodeLine('//ToDo: rewrite this', 43, 'abc.py').has_todo()
    True

    >>> SourceCodeLine('public class todo(){', 899, 'abc.java').has_todo()
    False

    >>> SourceCodeLine('while(x>15) {', 26, 'abc.java').has_todo()
    False
    """
    re_search = re.search(SourceCodeLine.todo_string, self.line, re.IGNORECASE)
    if re_search and self.len_before(re_search.span()):
      return True
    return False

  def get_todo(self):
    if not self.has_todo():
      raise Exception("This line has no TODO")
    re_search = re.search(SourceCodeLine.todo_string, self.line, re.IGNORECASE)
    span = re_search.span()
    after = self.line[span[1]:].strip()
    return Todo(self.filename, self.line_number, after)

  def __repr__(self):
    """Object representation of SourceCodeLine

    >>> print SourceCodeLine('public static void', 14, 'mydir/class.java')
    SourceCodeLine(line='public static void', line_number=14, filename='mydir/class.java')

    >>> sc = SourceCodeLine('for i in xrange(20)', 243, './dir1/dir2/x.py')
    >>> repr(sc) == repr(eval(repr(sc)))
    True
    """
    return "SourceCodeLine(line=%r, line_number=%r, filename=%r)" % (self.line, self.line_number, self.filename)

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
  ignores = ['build', 'bin', 'dst', 'dest', 'dist', 'node_modules','bower_components']
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
  """Get TODOs from a list of input files"""
  todo_list = []
  for file_ in file_list:
    with open(file_, 'r') as f:
      i = 0
      for line in f.readlines():
	i += 1

	sc_line = SourceCodeLine(line, i, file_)
	if sc_line.has_todo():
	  todo_list.append(sc_line.get_todo())
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
  files = get_files(file_suffix)
  todos = get_todos(files)
  write_todos(todos, output_md, md)

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
