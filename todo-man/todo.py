#!/usr/bin/env python
'''todo.py

Author: Rylan Santinon
'''

class Todo:
  def __init__(self, filepath, line_number, text):
    self.filepath = filepath
    self.line_number = str(line_number)
    self.text = text

  def __repr__(self):
    """Object representation of Todo

    >>> print Todo('abc', 34, 'bar')
    Todo(filepath='abc', line_number='34', text='bar')
    """
    return "Todo(filepath=%r, line_number=%r, text=%r)" % \
     (self.filepath, self.line_number, self.text)

if __name__ == '__main__':
  import doctest
  doctest.testmod()
