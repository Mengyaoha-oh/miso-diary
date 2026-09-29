"""Read passwords verbatim, before encryptcontent initializes its keys."""

import os

from mkdocs.exceptions import ConfigurationError
from mkdocs.plugins import event_priority


@event_priority(100)
def on_config(config):
    # YAML's !ENV coerces numeric-looking passwords (including hex) into ints.
    # Read the original environment values to preserve the exact answers.
    inventory = {}
    for level in ("books", "films", "notes"):
        variable = f"{level.upper()}_PASSWORD"
        password = os.environ.get(variable)
        if not password:
            raise ConfigurationError(f"Missing required environment variable: {variable}")
        inventory[level] = password
    config.plugins["encryptcontent"].config["password_inventory"] = inventory
    return config
