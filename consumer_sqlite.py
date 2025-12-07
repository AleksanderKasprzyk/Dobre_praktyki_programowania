import time
from queue_db import init_db, get_next_pending, update_status


def main():
    print("Consumer startuje...")
    init_db()

    while True:
        row = get_next_pending()
        if row is None:
            print("Brak zadań pending, śpię 5s...")
            time.sleep(5)
            continue

        task_id, status = row
        print(f"Pobrano zadanie {task_id}, status={status}")
git branch
        update_status(task_id, "in_progress")
        print(f"Zadanie {task_id} w trakcie (30s)...")
        time.sleep(30)

        update_status(task_id, "done")
        print(f"Zadanie {task_id} zakończone.")


if __name__ == "__main__":
    main()
