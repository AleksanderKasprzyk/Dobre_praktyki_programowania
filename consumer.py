import csv
import time
import os

QUEUE_FILE = "queue.csv"


def read_tasks():
    tasks = []
    if not os.path.exists(QUEUE_FILE):
        return tasks

    with open(QUEUE_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append(row)
    return tasks


def write_tasks(tasks):
    with open(QUEUE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["task_id", "status"])
        for t in tasks:
            writer.writerow([t["task_id"], t["status"]])


def consume_task():
    tasks = read_tasks()

    for task in tasks:
        if task["status"] == "pending":
            task_id = task["task_id"]
            print(f"[CONSUMER] Pobieram zadanie {task_id}")

            task["status"] = "in_progress"
            write_tasks(tasks)

            time.sleep(5)
            task["status"] = "done"
            write_tasks(tasks)

            print(f"[CONSUMER] Zadanie {task_id} ukończone")
            return

    print("[CONSUMER] Brak zadań w statusie pending")


if __name__ == "__main__":
    print("[CONSUMER] Startuję...")

    while True:
        consume_task()
        time.sleep(5)