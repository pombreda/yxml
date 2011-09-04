#!/usr/bin/env python
#coding: utf-8
#
# Copyright (c) 2011 Jan Stępień
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from yaml import load
from sys import stdin, stdout, stderr, exit
from xml.etree.ElementTree import Element, ElementTree
from optparse import OptionParser

parser = OptionParser(usage="%prog [options] [filename]")
parser.add_option("-e", dest="encoding", default='UTF-8',
    help="target XML encoding (default: UTF-8)")
parser.add_option("-r", dest="root", default=None,
    help="root element's tag (default: 'yaml', used only if there are " +
    "multiple root elements in the input file)")
parser.add_option("-o", dest="output", default=None,
    help="write output to a file named OUTPUT (default: standard output)")
parser.add_option("-n", dest="newline", default=True, action="store_false",
    help="don't add a new line character at the end")
(options, args) = parser.parse_args()

def list_to_elem(key, input):
  root = Element(key)
  singular = key[0:-1] if key[-1] == "s" else "child"
  for val in input:
    root.append(to_elem(singular, val))
  return root

def dict_to_elem(key, input):
  root = Element(key)
  for (key, val) in input.items():
    root.append(to_elem(key, val))
  return root

def to_elem(key, input):
  if isinstance(input, list):
    return list_to_elem(key, input)
  elif isinstance(input, dict):
    return dict_to_elem(key, input)
  else:
    elem = Element(key)
    elem.text = str(input)
    return elem

if len(args) > 1:
  parser.print_help(stderr)
  exit(1)

input = open(args[0], "r") if any(args) and args[0] != "-" else stdin
element = to_elem(options.root or 'yaml', load(input.read()))
if not options.root and len(list(element)) == 1:
  element = list(element)[0]
output = open(options.output, "w") if options.output else stdout
ElementTree(element).write(output, options.encoding)
if options.newline:
  output.write("\n")
