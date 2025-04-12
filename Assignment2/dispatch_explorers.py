
from tasks import run_explorer_task
import time
import logging

# Setup logging
logging.basicConfig(filename='dispatch_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


def run_parallel_explorers(num_explorers, maze_type="random", width=30, height=30):
    
    tasks = []
    for i in range(num_explorers):
        task = run_explorer_task.delay(i, maze_type, width, height)
        logging.info(f"Dispatched Explorer {i}")
        tasks.append(task)

    print("Waiting for results...")
    results = [task.get(timeout=60) for task in tasks]

    # Compare and display results
    print("\n=== Explorers' Performance Summary ===")
    logging.info("\n=== Explorers' Performance Summary ===")
    for result in results:
        summary = f"Explorer {result['id']}: Time = {result['time']:.2f}s | Moves = {result['moves']} | Backtracks = {result['backtracks']}"
        print(summary)
        logging.info(summary)


    best = min(results, key=lambda r: r["time"])
    best_msg = f"\nBest Route Found by Explorer {best['id']}! (Time = {best['time']:.2f}s)\n"
    print(best_msg)
    logging.info(best_msg)
    print("==================================================================================\n")


if __name__ == "__main__":
    run_parallel_explorers(4)  # Run 4 explorers
