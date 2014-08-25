preln
=====

**preln**, which stands for **pre**fix tree **ln**, is a command line
utility used to create a prefix path of one or more directories and one
symbolic link to categorize a file/directory according to its first
character(s). It can be used in conjunction with `find` to create a
prefix tree of symbolic links.


installing
----------

Make sure you have Python 3 and
[setuptools](https://pypi.python.org/pypi/setuptools).

Clone using Git and run `setup.py`:

    git clone https://github.com/eepp/preln.git
    cd preln
    sudo python3 setup.py install


using
-----

With the following files in `/some/path`:

    Alabama
    Alaska
    Arkansas
    Delaware
    Illinois
    Indiana
    Maine
    Maryland
    Missouri
    Nebraska
    New Hampshire
    Ohio
    Oregon
    Utah
    Wisconsin
    Wyoming

use preln with `find` like this:

    find /some/path -mindepth 1 -maxdepth 1 -exec preln -o /tmp/links '{}' \;

and `/tmp/links` will look like this:

    A/
      _Alabama -> /some/path/Alabama
      _Alaska -> /some/path/Alaska
      _Arkansas -> /some/path/Arkansas
    D/
      _Delaware -> /some/path/Delaware
    I/
      _Illinois -> /some/path/Illinois
      _Indiana -> /some/path/Indiana
    M/
      _Maine -> /some/path/Maine
      _Maryland -> /some/path/Maryland
      _Missouri -> /some/path/Missouri
    N/
      _Nebraska -> /some/path/Nebraska
      _New Hampshire -> /some/path/New Hampshire
    O/
      _Ohio -> /some/path/Ohio
      _Oregon -> /some/path/Oregon
    U/
      _Utah -> /some/path/Utah
    W/
      _Wisconsin -> /some/path/Wisconsin
      _Wyoming -> /some/path/Wyoming

Symbolic links are always prefixed with `_` to avoid conflicts with
directories: with source files

    h
    hello
    hi

preln needs to create an output directory `h` and a symbolic link `h`,
which is impossible. Thus, `h` will be the directory containing
symbolic links `_hello` and `_hi`, while `h/_h` will be a symbolic link
pointing to the original `h`:

    h/
      _h -> /some/path/h
      _hello -> /some/path/hello
      _hi -> /some/path/hi

preln supports custom depths (the default depth is 1):

    find /some/path -mindepth 1 -maxdepth 1 -exec preln -d 3 -o /tmp/links '{}' \;

would create:

    ...
    M/
      a/
        i/
          _Maine -> /some/path/Maine
        r/
          _Maryland -> /some/path/Maryland
      i/
        s/
          _Missouri -> /some/path/Missouri
    ...

preln is case sensitive by default: `Grand` and `giraffe` sources
will lead to the creation of both `G` and `g` prefixes.
Case sensitivity can be turned off using the `-i` option (applies to
all depth levels). In this case, all created prefix directories will
be in lowercase.

For a complete list of options, do

    preln --help
