#!/usr/bin/python
#
# Common lint functions applicable to multiple types of files.

import re

def VerifyLineLength(filename, lines, max_length):
  """Checks to make sure the file has no lines with lines exceeding the length
  limit.

  Args:
    filename: the file under consideration as string
    lines: contents of the file as string array
    max_length: maximum acceptable line length as number

  Returns:
    A list of tuples with format [(filename, line number, msg), ...] with any
    violations found.
  """
  lint = []
  for line_num, line in enumerate(lines, start=1):
    length = len(line.rstrip('\n'))
    if length > max_length:
      lint.append((filename, line_num,
                   'Line exceeds %d chars (%d)' % (max_length, length)))
  return lint

def VerifyTabs(filename, lines):
  """Checks to make sure the file has no tab characters.

  Args:
    filename: the file under consideration as string
    lines: contents of the file as string array

  Returns:
    A list of tuples with format [(line_number, msg), ...] with any violations
    found.
  """
  tab_re = re.compile(r'\t')
  return [(filename, line_num, 'Tab found instead of whitespace')
          for line_num, line in enumerate(lines, start=1)
          if tab_re.match(line.rstrip('\n'))]


def VerifyTrailingWhitespace(filename, lines):
  """Checks to make sure the file has no lines with trailing whitespace.

  Args:
    filename: the file under consideration as string
    lines: contents of the file as string array

  Returns:
    A list of tuples with format [(filename, line number, msg), ...] with any
    violations found.
  """
  trailing_whitespace_re = re.compile(r'\s+$')
  return [(filename, line_num, 'Trailing whitespace')
          for line_num, line in enumerate(lines, start=1)
          if trailing_whitespace_re.match(line.rstrip('\n'))]


class BaseLint:
  def RunOnFile(self, lines):
    raise Exception('RunOnFile() unimplemented')


def RunLintOverAllFiles(linter, filenames):
  """Runs linter over the contents of all files.

  Args:
    lint: subclass of BaseLint, implementing RunOnFile()
    filenames: list of all files whose contents will be linted

  Returns:
    A list of tuples with format [(filename, line number, msg), ...] with any
    violations found.
  """
  lint = []
  for filename in filenames:
    file = open(filename, 'r')
    if not file:
      print 'Cound not open %s' % filename
      continue
    lines = file.readlines()
    lint.extend(linter.RunOnFile(filename, lines))

  return lint
