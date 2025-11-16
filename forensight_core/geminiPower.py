import google.generativeai as genai
import os
import threading
import time

gemini_lock = threading.Lock()

# Cache the API configuration to avoid repeated setup
API_CONFIGURED = False

def configure_api(api_key):
    global API_CONFIGURED
    if not API_CONFIGURED:
        with gemini_lock:
            genai.configure(api_key=api_key)
            API_CONFIGURED = True

def check_powerShell(api_key, powershell_command):
    try:
        # Configure the API only once per thread
        configure_api(api_key)
        
        # Build a compact, context-focused prompt
        prompt = f"""
        Assess the following PowerShell command for potentially malicious behavior. 
        Focus on indicators like data exfiltration, privilege escalation, and unauthorized execution.
        Command:
        {powershell_command}
        Required Result one word: "suspicious" or "normal"
        """
        
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        result = response.text.strip().lower()

        # Print the result for logging
        print(f"Analyzed Command: {powershell_command[:50]}... -> {result}")
        return result
        
    except Exception as e:
        error_message = str(e)
        
        # Handle rate limit errors with exponential backoff
        if "ResourceExhausted" in error_message or "429" in error_message:
            print("Rate limit exceeded. Retrying in 60 seconds...")
            time.sleep(60)
            try:
                # Retry after a delay
                response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
                return response.text.strip().lower()
            except Exception as retry_e:
                print(f"Retry failed: {retry_e}")
                return "unknown"
        else:
            print(f"Error in API call: {error_message}")
            return "unknown"


