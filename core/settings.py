import json
import sys
import asyncio

def read_config_json(path_confg_file, param):
    with open(path_confg_file, "r", encoding="utf-8") as f:
        _config = json.load(f)
    return _config.get(param)
