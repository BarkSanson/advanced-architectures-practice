import threading

import paho.mqtt.client as paho
import paho.mqtt.publish as publish

from message import Message


class MessageManager:
    _HOST, _PORT, _KEEP_ALIVE = "localhost", 1883, 60

    def __init__(self):
        self.client = paho.Client()

        self.message_handler = None
        self.client.on_message = self.on_message

        self.client.connect(MessageManager._HOST,
                            MessageManager._PORT,
                            MessageManager._KEEP_ALIVE)
        print(f"Connected to {MessageManager._HOST}:{MessageManager._PORT}")

        self.client.subscribe("tic-tac-toe", 0)

        self.client.loop_start()

    def set_handler(self, message_handler):
        self.message_handler = message_handler

    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        message = Message.from_json(payload)

        threading.Thread(
            target=self.message_handler,
            args=[message]
        ).start()

        client.publish("pong", "ack", 0)

    def send_move(self, message: Message):
        payload = message.to_json()

        publish.single(topic="tic-tac-toe",
                       payload=payload,
                       hostname=MessageManager._HOST,
                       port=MessageManager._PORT)
