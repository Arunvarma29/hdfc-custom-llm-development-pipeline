import time

from services.data_preparation.app.workers.preparation_worker import (
    PreparationWorker,
)


def main():
    worker = PreparationWorker()

    print("Data Preparation Worker started")

    while True:
        processed = worker.run_once()

        if not processed:
            time.sleep(3)


if __name__ == "__main__":
    main()