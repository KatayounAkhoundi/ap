"""Storage backend selection — Python equivalent of the EX7 Config pattern.

Reads storage_config.json (created with the default backend on first run).
Supported backends: "sqlite" and "pickle".
"""
import json
import os

CONFIG_FILE = "storage_config.json"
VALID_BACKENDS = ("sqlite", "pickle")
DEFAULT_BACKEND = "sqlite"


def get_storage_backend():
    if not os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({"backend": DEFAULT_BACKEND}, f, indent=2)
        except OSError:
            return DEFAULT_BACKEND
    try:
        with open(CONFIG_FILE) as f:
            backend = json.load(f).get("backend", DEFAULT_BACKEND)
    except (OSError, ValueError):
        return DEFAULT_BACKEND
    return backend if backend in VALID_BACKENDS else DEFAULT_BACKEND
