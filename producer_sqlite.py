from queue_db import init_db, add_task


def main():
    init_db()
    task_id = add_task()
    print(f"Dodano zadanie o id={task_id} (status: pending)")


if __name__ == "__main__":
    # jeśli chcesz wrzucić 100 zadań jednorazowo:
    for _ in range(100):
        main()
