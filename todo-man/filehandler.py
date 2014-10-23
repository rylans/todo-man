#!/usr/bin/env python
'''filehandler.py

Author: Rylan Santinon
'''
import os

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

if __name__ == '__main__':
  import doctest
  doctest.testmod()
