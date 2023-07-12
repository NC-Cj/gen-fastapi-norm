import json
from typing import Dict, Any

from pydantic import BaseModel, create_model


def __create_dynamic_model(config: Dict[str, Any]) -> BaseModel:
    ConfigModel = create_model("ConfigModel", **config)
    return ConfigModel(**config)


def go_init():
    # Read Configuration File
    with open("config.json") as f:
        config = json.load(f)

    # Create dynamic model
    config_model = __create_dynamic_model(config)
    return config_model
