"""Read passwords from the environment or an ignored local JSON file."""

import json
import os
from pathlib import Path

from mkdocs.exceptions import ConfigurationError
from mkdocs.plugins import event_priority


@event_priority(100)
def on_config(config):
    local_file = Path(config.config_file_path).parent / "passwords.local.json"
    local_passwords = {}
    if local_file.exists():
        try:
            local_passwords = json.loads(local_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            raise ConfigurationError(
                "Cannot read passwords.local.json. Use a JSON object with quoted passwords."
            ) from None
        if not isinstance(local_passwords, dict):
            raise ConfigurationError("passwords.local.json must contain a JSON object.")

    # YAML's !ENV coerces numeric-looking passwords (including hex) into ints.
    # Preserve strings, with environment values taking precedence for deployment.
    inventory = {}
    for level in ("books", "films", "notes"):
        variable = f"{level.upper()}_PASSWORD"
        password = os.environ.get(variable, local_passwords.get(variable))
        if not isinstance(password, str) or not password:
            raise ConfigurationError(
                f"Set {variable} in the environment or as a non-empty string in passwords.local.json."
            )
        inventory[level] = password
    config.plugins["encryptcontent"].config["password_inventory"] = inventory
    return config
