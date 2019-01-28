#!/usr/bin/python3

import sys
import os

from lib.root import Root
from lib.styles import set_style


if len(sys.argv)<2:
    sys.exit("Usage: opview [contract name]")

if not os.path.exists("build/contracts/"+sys.argv[-1]+".json"):
    sys.exit("ERROR: No compiled contract named '{}' in the build/contracts folder.".format(sys.argv[1]))

root = Root()
set_style()
root.mainloop()