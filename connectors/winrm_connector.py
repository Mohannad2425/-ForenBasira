import json
import winrm

def test_winrm_connection():
    """
    Test a WinRM connection to a target Windows machine.
    Reads credentials and IP from config.json.
    """
    try:
        # Load configuration
        config_path = r"C:\ForenBasira\ForenBasira_Project\config\config.json"
        with open(config_path, "r") as f:
            config = json.load(f)

        target = config["targets"][0]
        ip = target["ip"]
        username = target["auth"]["username"]
        password = target["auth"]["password"]

        # Choose authentication method
        # Use 'ntlm' if domain or server doesn't allow plaintext
        # Use 'plaintext' only if AllowUnencrypted=True on server
        session = winrm.Session(
            f"http://{ip}:5985/wsman",
            auth=(username, password),
            transport="ntlm",  # or "plaintext"
            server_cert_validation="ignore"  # only needed for HTTPS
        )

        # Run a simple command
        result = session.run_cmd("ipconfig")
        return result.std_out.decode()

    except winrm.exceptions.InvalidCredentialsError:
        return "❌ Invalid credentials or authentication type not allowed by server."
    except winrm.exceptions.WinRMTransportError as e:
        return f"❌ WinRM Transport Error: {str(e)}"
    except FileNotFoundError:
        return f"❌ Config file not found at {config_path}"
    except KeyError as e:
        return f"❌ Missing key in config.json: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

if __name__ == "__main__":
    output = test_winrm_connection()
    print(output)
