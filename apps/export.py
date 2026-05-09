import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.models.PackageModel import PackageModel as Package

with open("data.json", "w") as f:
    f.write(Package.schema_json(indent=2))