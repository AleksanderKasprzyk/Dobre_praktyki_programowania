import json
import pika
import time
import random

QUEUE_NAME = "image_tasks"


def callback(ch, method, properties, body):
    task = json.loads(body)
    print(f"[CONSUMER] Processing {task['task_id']}")

    time.sleep(5)
    people_count = random.randint(0, 10)

    print(
        f"[CONSUMER] Image {task['image_url']} -> "
        f"{people_count} people detected"
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials("admin", "admin123")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            credentials=credentials
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
    )

    print("[CONSUMER] Waiting for tasks...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
