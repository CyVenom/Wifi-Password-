import subprocess

def get_wifi_passwords():
    try:
        # Run the command to get the list of Wi-Fi profiles
        profiles_data = subprocess.check_output("netsh wlan show profiles").decode("utf-8", errors="backslashreplace")
        
        # Find all the Wi-Fi profile names
        profiles = [i.split(":")[1][1:-1] for i in profiles_data.split("\n") if "All User Profile" in i]
        
        wifi_details = []
        
        # Loop over all profiles and get the password for each
        for profile in profiles:
            profile_info = subprocess.check_output(f"netsh wlan show profile \"{profile}\" key=clear").decode("utf-8", errors="backslashreplace")
            try:
                # Extract the password
                password = [b.split(":")[1][1:-1] for b in profile_info.split("\n") if "Key Content" in b][0]
            except IndexError:
                password = None
            wifi_details.append((profile, password))
        
        return wifi_details
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def display_wifi_details(wifi_details):
    if wifi_details:
        for ssid, password in wifi_details:
            print(f"SSID: {ssid}, Password: {password if password else 'None'}")
    else:
        print("No Wi-Fi details found or an error occurred.")

if __name__ == "__main__":
    wifi_details = get_wifi_passwords()
    display_wifi_details(wifi_details)
