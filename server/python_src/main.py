# This is the MAIN FILE for the ENTIRE REPOSITORY. To 'run' the software, this is the right file (unless you're unit testing..)

# Just as a general note... this file is the 'glue' between all parts of the repository.
# If you're looking to jump right into things, please create a new file (and directory) 
# to keep the repository organized.

# Thanks!
import numpy
import vectormath
import frontend.dss.freighter as freighter
import backend.statistics.plotting.plotting as plotting
import frontend.dss.deep_seashell as dss

VERSION = "0.0.1"

print("deep sea tactics software version " + VERSION)
freighter.init()
freighter.setup_packaging_system()
plotting.init()
dss.init()

dss.Interpret._input_loop()