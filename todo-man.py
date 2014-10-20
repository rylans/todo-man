import argparse
import os
#TODO: put in docstring

class Todo:
  def __init__(self, filepath, line_number, text):
    self.filepath = filepath
    self.line_number = line_number
    self.text = text

  def __repr__(self):
    return '[' + ','.join([self.filepath, str(self.line_number), self.text]) + ']'

def get_files(suffix):
  file_list = []
  for root, dirs, files in os.walk('.'):
    for f in files:
      if f.endswith(suffix):
	file_list.append(os.path.join(root, f))
  return file_list

def get_todos(file_list):
  todo_list = []
  for file_ in file_list:
    with open(file_, 'r') as f:
      i = 0
      for line in f.readlines():
	i += 1
	if 'TODO:' in line:
	  if len(line.strip().split('TODO')[0]) <= 2:
	    todo = line.split('TODO:')[1].strip()
	    todo_list.append(Todo(file_, i, todo))
  return todo_list

def main():
  parser = argparse.ArgumentParser(description='Process.')
  parser.add_argument('out', metavar='O', nargs='?', default='TODO.md', help='The markdown file to write TODOs to')
  parser.add_argument('file_type', metavar='T', nargs=1, help='The file suffix of source code files (ex: py, js, java)')
  #TODO: Make an argument '-f' to force the output file to get overwritten
  args = parser.parse_args()
  print args.out
  print args.file_type[0]

  output_md = args.out
  file_suffix = args.file_type[0]

  files = get_files(file_suffix)
  print get_todos(files)

if __name__ == '__main__':
  #TODO: Import logging and use it
  main()
