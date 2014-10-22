#!/usr/bin/env python
'''sourcecodeline.py
A line of source code

Author: Rylan Santinon
'''
import re

from todo import Todo

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

if __name__ == '__main__':
  import doctest
  doctest.testmod()
