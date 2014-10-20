import argparse
import os

def get_files(suffix):
  file_list = []
  for root, dirs, files in os.walk('.'):
    for f in files:
      if f.endswith(suffix):
	file_list.append(os.path.join(root, f))
  return file_list

def main():
  parser = argparse.ArgumentParser(description='Process.')
  parser.add_argument('out', metavar='O', nargs='?', default='TODO.md', help='The markdown file to write TODOs to')
  parser.add_argument('file_type', metavar='T', nargs=1, help='The file suffix of source code files (ex: py, js, java)')
  args = parser.parse_args()
  print args.out
  print args.file_type[0]

  output_md = args.out
  file_suffix = args.file_type[0]

  print get_files(file_suffix)

if __name__ == '__main__':
  main()
