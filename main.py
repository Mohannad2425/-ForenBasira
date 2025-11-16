from gui.GUI import launch_gui
from config.config_loader import load_config

def main():
    print("Starting ForenBasira...")
    
    config = load_config()
    print("Configuration loaded successfully.")
    
    # Launch GUI
    launch_gui(config)

if __name__ == "__main__":
    main()
