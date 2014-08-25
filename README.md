preln
=====

**preln**, which stands for <b>pre</b>fix tree **ln**, is a command line
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
      Alabama_ -> /some/path/Alabama
      Alaska_ -> /some/path/Alaska
      Arkansas_ -> /some/path/Arkansas
    D/
      Delaware_ -> /some/path/Delaware
    I/
      Illinois_ -> /some/path/Illinois
      Indiana_ -> /some/path/Indiana
    M/
      Maine_ -> /some/path/Maine
      Maryland_ -> /some/path/Maryland
      Missouri_ -> /some/path/Missouri
    N/
      Nebraska_ -> /some/path/Nebraska
      New Hampshire_ -> /some/path/New Hampshire
    O/
      Ohio_ -> /some/path/Ohio
      Oregon_ -> /some/path/Oregon
    U/
      Utah_ -> /some/path/Utah
    W/
      Wisconsin_ -> /some/path/Wisconsin
      Wyoming_ -> /some/path/Wyoming

Symbolic links are always suffixed with `_` to avoid conflicts with
directories: with source files

    h
    hello
    hi

preln needs to create an output directory `h` and a symbolic link `h`,
which is impossible. Thus, `h` will be the directory containing
symbolic links, while `h/h_` being a symbolic link pointing to the
original `h`:

    h/
      h_ -> /some/path/h
      hello_ -> /some/path/hello
      hi_ -> /some/path/hi

preln supports custom depths (the default depth is 1):

    find /some/path -mindepth 1 -maxdepth 1 -exec preln -d 3 -o /tmp/links '{}' \;

would create:

    ...
    M/
      a/
        i/
          Maine_ -> /some/path/Maine
        r/
          Maryland_ -> /some/path/Maryland
      i/
        s/
          Missouri_ -> /some/path/Missouri
    ...

preln is case sensitive by default: `Grand` and `giraffe` sources
will lead to the creation of both `G` and `g` prefixes.
Case sensitivity can be turned off using the `-i` option (applies to
all depth levels). In this case, all created prefix directories will
be in lowercase.

For a complete list of options, do

    preln --help
