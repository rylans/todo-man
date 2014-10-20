from setuptools import setup, find_packages

setup(name='todo-man',
      version='0.0.1',
      author='Rylan Santinon',
      description='Grab TODOs in your source code them and put them into a markdown document',
      scripts=['todo-man/todo-man.py'],
      license='Apache',
      packages=['todo-man'])
