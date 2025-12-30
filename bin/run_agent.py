#!/usr/bin/env python3
import sys
import os

# Add the project root and the packages directory to the python path
sys.path.insert(0, '/srv/janus')
sys.path.insert(0, '/srv/janus/02_FORGE/packages')

import sys
import os

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.daemon import main

if __name__ == "__main__":
    main()
