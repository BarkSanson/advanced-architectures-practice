import requests
import random
import sys
import time
import enum
import json

from server_state import ServerState

API = 'http://localhost:5000'

class ServerState(enum.Enum):
    WAITING = 0
    FAILED = 1
    SUCCESS = 2

def main():
    if len(sys.argv) != 2:
        print("Incorrect usage")
        print("Correct syntax: python client.py <id>")
        return
    
    id = sys.argv[1]

    headers = { 'Content-Type': 'application/json' }

    while True:
        n = random.randint(1, 10)
        print("Generated random number: {n}")

        data = json.dumps({ "id": id, "number": n})
        
        res = requests.post(f'{API}/number', data=data, headers=headers)

        state = res.json()["state"]
 
        while state == ServerState.WAITING.value:
            res = requests.get(f'{API}/state').json()
            state = res["state"]

            print(f"Server state {state}")

            time.sleep(5)
        
        if state == ServerState.SUCCESS.value:
            print("Majority!")
            break            

if __name__ == "__main__":
    main()