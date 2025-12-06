import csv
import time
import os

QUEUE_FILE = "queue.csv"


def init_queue_file():
    if not os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["task_id", "status"])


def add_task(task_id: int):
    with open(QUEUE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([task_id, "pending"])
    print(f"[PRODUCER] Dodano zadanie {task_id}")


if __name__ == "__main__":
    init_queue_file()

    for i in range(1, 101):
        add_task(i)
        time.sleep(0.1)
