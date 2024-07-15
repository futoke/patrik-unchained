import os

# Set path for script.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import pprint
import yaml


with open("actions.yml", 'r') as fh:
    data = yaml.safe_load(fh)

pprint.pprint(data["actions"])