import json
import pika
import requests
import time

QUEUE_NAME = "image_tasks"
SERVICE_A_URL = "http://service_a:5000/process"

def connect():
    while True:
        try:
            print("[SERVICE B] Connecting to RabbitMQ...")
            return pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq"))

        except pika.exceptions.AMQPConnectionError:
            print("[SERVICE B] RabbitMQ not ready, retry in 3s...")
            time.sleep(3)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[SERVICE B] Received from queue: {data}")

    response = requests.post(SERVICE_A_URL, json=data)

    print(f"[SERVICE B] Sent to Service A, status={response.status_code}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = connect()

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback)

    print("[SERVICE B] Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
