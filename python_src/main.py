# This is the MAIN FILE for the ENTIRE REPOSITORY. To 'run' the software, this is the right file (unless you're unit testing..)

# Just as a general note... this file is the 'glue' between all parts of the repository.
# If you're looking to jump right into things, please create a new file (and directory) 
# to keep the repository organized.

# Thanks!
import numpy
import vectormath
import rust_mod

VERSION = "0.0.1"

print("deep sea tactics software version " + VERSION)

print(rust_mod.sum_as_string(1, 1))

print(rust_mod.sum_as_string(1, 1))