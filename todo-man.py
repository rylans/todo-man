import argparse

def main():
  parser = argparse.ArgumentParser(description='Process.')
  parser.add_argument('out', metavar='O', nargs='?', default='TODO.md', help='The markdown file to write TODOs to')
  args = parser.parse_args()
  print args.out

if __name__ == '__main__':
  main()
