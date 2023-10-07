from flask import Flask, request, jsonify

from server_state import ServerState

app = Flask(__name__)

CLIENTS = 3
numbers = []

state = ServerState.WAITING
agents_checked = 0

@app.post('/number')
def number():
    json = request.get_json()

    if len(numbers) < CLIENTS:
        numbers.append(json["number"])

    return jsonify({ "state": state.value }), 201

@app.get('/state')
def state_check():
    if len(numbers) < CLIENTS:
        return jsonify({ "state": state.value }), 200
    
    check_if_majority()

    return jsonify({ "state": state.value }), 200


def check_if_majority():
    global state

    count = {}
    max = ('', 0)

    for n in numbers:
        if n in count:
            count[n] += 1
        else:
            count[n] = 1
        
        if count[n] > max[1]:
            max = (n, count[n])
    
    if max[1] > 1:
        state = ServerState.SUCCESS
    else:
        state = ServerState.FAILED


if __name__ == "__main__":
    app.run()