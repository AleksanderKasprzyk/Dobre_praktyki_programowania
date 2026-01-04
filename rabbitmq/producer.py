import json
import pika
import uuid

QUEUE_NAME = "image_tasks"


def send_task(image_url: str):
    credentials = pika.PlainCredentials("admin", "admin123")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            credentials=credentials
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    message = {
        "task_id": str(uuid.uuid4()),
        "image_url": image_url,
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
    )

    connection.close()

if __name__ == "__main__":
    send_task("https://example.com/image1.jpg")
