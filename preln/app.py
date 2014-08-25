# The MIT License (MIT)
#
# Copyright (c) 2014 Philippe Proulx <eepp.ca>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import os
import argparse
import preln


def _parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument('-V', '--version', action='version',
                    version='%(prog)s v{}'.format(preln.__version__))
    ap.add_argument('-d', '--depth', action='store', default=1, type=int,
                    help='Depth of output directories (default: 1)')
    ap.add_argument('-i', '--ignore-case', action='store_true',
                    help='Ignore case distinctions in SRC')
    ap.add_argument('-o', '--output', action='store', type=str,
                    default=os.getcwd(),
                    help='Path to output directory (default: CWD)')
    ap.add_argument('-s', '--space-replacement', action='store', type=str,
                    default=' ',
                    help='Space character replacement')
    ap.add_argument('src', metavar='SRC', action='store', type=str,
                    help='Path to source file/directory')

    # parse args
    args = ap.parse_args()

    # validate depth
    if args.depth < 1:
        print('Error: depth must be greater than or equal to 1',
              file=sys.stderr)
        sys.exit(1)

    # validate space replacement
    if len(args.space_replacement) > 1:
        print('Error: space replacement must be zero or one character',
              file=sys.stderr)
        sys.exit(1)

    # validate output directory
    if not os.path.isdir(args.output):
        print('Error: output is not an existing directory',
              file=sys.stderr)
        sys.exit(1)

    # source absolute path
    args.src = os.path.abspath(args.src)

    return args


def _extract_prefixes(src, depth, ignore_case, space_replacement):
    file = os.path.basename(src)
    file = file.replace(' ', space_replacement)

    prefixes = file[:min(len(file), depth)]

    if ignore_case:
        prefixes = prefixes.lower()

    return prefixes


def _create_prefixes_branches(src, output, prefixes):
    file = os.path.basename(src)
    output_dir = os.path.join(output, os.path.join(*prefixes))
    output_link = os.path.join(output_dir, '_' + file)

    try:
        # create prefixes directories
        os.makedirs(output_dir, mode=0o755, exist_ok=True)

        # remove existing file where symlink will be
        if os.path.lexists(output_link):
            os.remove(output_link)

        # create symlink
        os.symlink(src, output_link)
    except:
        return False, output_link

    return True, output_link


def create_prefix_path(src, output, depth, ignore_case, space_replacement):
    prefixes = _extract_prefixes(src, depth, ignore_case, space_replacement)
    res, link = _create_prefixes_branches(src, output, prefixes)

    if not res:
        msg = 'Error: could not create "{}"'.format(link)
        print(msg, file=sys.stderr)
    else:
        msg = 'Created "{}"'.format(link)
        print(msg)


def run():
    args = _parse_args()
    create_prefix_path(args.src, args.output, args.depth,
                       args.ignore_case, args.space_replacement)
