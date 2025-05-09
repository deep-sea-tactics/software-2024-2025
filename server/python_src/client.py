"""
You're likely incredibly confused as to why "client.py"
is located in the "server" directory.

Due to an idiotic oversight, python's
module organization ended up conflicting
with the current repository organization.

To maintain the ease of use of our
custom `freighter` package management
system, "client.py" is located in
this directory.

:)
"""
import frontend.dss.deep_seashell as dss
dss.init()
dss.Interpret.run("out client dss is initialized")
import sys
import os
sys.path.append(os.getcwd() + "/client/python_src/thruster")
from thruster import * # type: ignore (python doesn't realise this is valid)
