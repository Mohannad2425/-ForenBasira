import json
import os

class ConfigError(Exception):
    """Custom error for config-related issues."""
    pass

def load_config(path="C:\ForenBasira\project\config.json"):
    
    """
    Load and validate ForenBasira configuration.
    Returns a dictionary containing the config.
    """
    if not os.path.exists(path):
        raise ConfigError(f"Configuration file not found at: {path}")

    with open(path, "r") as f:
        config = json.load(f)

    # Basic validation checks
    required_sections = ["vms", "splunk", "response", "api_keys"]
    for section in required_sections:
        if section not in config:
            raise ConfigError(f"Missing required section: {section}")

    # Validate VMs
    for vm in config["vms"]:
        for key in ["id", "ip", "os", "role"]:
            if key not in vm:
                raise ConfigError(f"Missing key '{key}' in VM config: {vm}")

    print("[✔] Configuration loaded successfully.")
    return config


def get_vm_by_name(config, name):
    """Return VM details by its name."""
    for vm in config["vms"]:
        if vm["name"].lower() == name.lower():
            return vm
    raise ConfigError(f"No VM found with name '{name}'.")


def get_splunk_config(config):
    """Return Splunk connection details."""
    return config["splunk"]


def get_response_scripts(config):
    """Return paths to response scripts (block/isolate)."""
    return config["response"]
