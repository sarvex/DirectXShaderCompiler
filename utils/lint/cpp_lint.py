#!/usr/bin/python
#
# Checks C++ files to make sure they conform to LLVM standards, as specified in
# http://llvm.org/docs/CodingStandards.html .
#
# TODO: add unittests for the verifier functions:
# http://docs.python.org/library/unittest.html .

import common_lint
import re
import sys

def VerifyIncludes(filename, lines):
  """Makes sure the #includes are in proper order and no disallows files are
  #included.

  Args:
    filename: the file under consideration as string
    lines: contents of the file as string array
  """
  lint = []

  include_gtest_re = re.compile(r'^#include "gtest/(.*)"')
  include_llvm_re = re.compile(r'^#include "llvm/(.*)"')
  include_support_re = re.compile(r'^#include "(Support/.*)"')
  include_config_re = re.compile(r'^#include "(Config/.*)"')
  include_system_re = re.compile(r'^#include <(.*)>')

  DISALLOWED_SYSTEM_HEADERS = ['iostream']

  prev_config_header = None
  prev_system_header = None
  for line_num, line in enumerate(lines, start=1):
    if config_header := include_config_re.match(line):
      curr_config_header = config_header[1]
      if prev_config_header and prev_config_header > curr_config_header:
        lint.append((
            filename,
            line_num,
            f'Config headers not in order: "{prev_config_header}" before "{curr_config_header}"',
        ))

    if system_header := include_system_re.match(line):
      curr_system_header = system_header[1]

      # Is it blacklisted?
      if curr_system_header in DISALLOWED_SYSTEM_HEADERS:
        lint.append((
            filename,
            line_num,
            f'Disallowed system header: <{curr_system_header}>',
        ))
      elif prev_system_header:
        # Make sure system headers are alphabetized amongst themselves
        if prev_system_header > curr_system_header:
          lint.append((
              filename,
              line_num,
              f'System headers not in order: <{prev_system_header}> before <{curr_system_header}>',
          ))

      prev_system_header = curr_system_header

  return lint


class CppLint(common_lint.BaseLint):
  MAX_LINE_LENGTH = 80

  def RunOnFile(self, filename, lines):
    lint = []
    lint.extend(VerifyIncludes(filename, lines))
    lint.extend(common_lint.VerifyLineLength(filename, lines,
                                             CppLint.MAX_LINE_LENGTH))
    lint.extend(common_lint.VerifyTabs(filename, lines))
    lint.extend(common_lint.VerifyTrailingWhitespace(filename, lines))
    return lint


def CppLintMain(filenames):
  all_lint = common_lint.RunLintOverAllFiles(CppLint(), filenames)
  for lint in all_lint:
    print '%s:%d:%s' % (lint[0], lint[1], lint[2])
  return 0


if __name__ == '__main__':
  sys.exit(CppLintMain(sys.argv[1:]))
