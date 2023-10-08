import requests
import random
import sys
import time
import enum
import json

from server_state import ServerState

API = 'http://localhost:5000'
MIN, MAX = 1, 10


def main():
    if len(sys.argv) != 2:
        print("Incorrect usage")
        print("Correct syntax: python client.py <id>")
        return

    id = sys.argv[1]

    headers = {'Content-Type': 'application/json'}

    while True:
        n = random.randint(MIN, MAX)
        print(f"Generated random number: {n}")

        data = json.dumps({"number": n})

        requests.post(f'{API}/number', data=data, headers=headers)

        res = requests.get(f'{API}/state/{id}').json()
        state = res["state"]

        while state == ServerState.WAITING.value:
            time.sleep(5)

            res = requests.get(f'{API}/state/{id}').json()
            state = res["state"]

            print(f"Server state {state}")

        if state == ServerState.SUCCESS.value:
            print("Majority!")
            break

        print("Try failed. Trying again.")
        # Wait some time to give some space to the other
        # clients to ask for state
        time.sleep(10)


if __name__ == "__main__":
    main()
