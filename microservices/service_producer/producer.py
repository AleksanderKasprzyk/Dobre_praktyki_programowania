import pika
import json
import time
import uuid

QUEUE_NAME = "image_tasks"

def connect():
    while True:
        try:
            print("[PRODUCER] Connecting to RabbitMQ...")
            return pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq"))

        except pika.exceptions.AMQPConnectionError:
            print("[PRODUCER] RabbitMQ not ready, retry in 3s...")
            time.sleep(3)

connection = connect()

channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

message = {
    "task_id": str(uuid.uuid4()),
    "people": 3}

channel.basic_publish(
    exchange="",
    routing_key=QUEUE_NAME,
    body=json.dumps(message))

print("[PRODUCER] Message sent:", message)
connection.close()
