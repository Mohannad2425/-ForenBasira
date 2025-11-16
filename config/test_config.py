from config_loader import load_config, get_vm_by_name, get_splunk_config

# Load the configuration
config = load_config()

# Get VM info
win7_vm = get_vm_by_name(config, "Win7-Target")
print(win7_vm)

# Get Splunk details
splunk = get_splunk_config(config)
print("Splunk URL:", splunk["url"])




