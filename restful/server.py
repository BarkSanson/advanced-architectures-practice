from flask import Flask, request, jsonify, Response

from server_state import ServerState

app = Flask(__name__)

CLIENTS = 3
numbers = []

state = ServerState.WAITING
agents_checked = set()


@app.post('/number')
def number():
    global numbers

    json = request.get_json()

    numbers.append(json["number"])

    if len(numbers) >= CLIENTS:
        print("Checking majority...")
        check_if_majority()
        numbers = []

    return Response(status=200)


@app.get('/state/<id_client>')
def state_check(id_client):
    global state
    global agents_checked

    if state == ServerState.SUCCESS or state == ServerState.WAITING:
        return jsonify({"state": state.value}), 200

    agents_checked.add(id_client)

    if len(agents_checked) >= CLIENTS:
        print("All agents checked state. Resetting...")

        state = ServerState.WAITING
        agents_checked = set()

    return jsonify({"state": ServerState.FAILED.value }), 200


def check_if_majority():
    global state

    if state == ServerState.SUCCESS or state == ServerState.FAILED:
        return

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
