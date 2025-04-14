"""
Main entry point for the maze runner game with Celery-based dispatch option.
"""

import argparse
import logging
from src.game import run_game
from src.explorer import Explorer
from tasks import run_explorer_task


logging.basicConfig(filename='dispatch_explorer_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


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
    best_msg = f"\nBest Route Found by Explorer {best['id']}! (Time = {best['time']:.2f}s)"
    print(best_msg)
    logging.info(best_msg)
    print("======================================\n")


def main():
    parser = argparse.ArgumentParser(description="Maze Runner Game - With Celery Dispatch Option")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate (random or static)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--auto", action="store_true",
                        help="Run automated maze exploration")
    parser.add_argument("--visualize", action="store_true",
                        help="Visualize the automated exploration in real-time")
    parser.add_argument("--parallel", type=int, default=4,
                        help="Run multiple explorers in parallel using Celery (set number of explorers)")

    args = parser.parse_args()

    if args.auto:
        if args.parallel > 0:
            run_parallel_explorers(args.parallel, args.type, args.width, args.height)
            
        else:
            from src.maze import create_maze
            maze = create_maze(args.width, args.height, args.type)
            explorer = Explorer(maze, visualize=args.visualize)
            time_taken, moves = explorer.solve()
            print(f"Maze solved in {time_taken:.2f} seconds")
            print(f"Number of moves: {len(moves)}")
            if args.type == "static":
                print("Note: Width and height arguments were ignored for the static maze")
                
    else:
        run_game(maze_type=args.type, width=args.width, height=args.height)
        

if __name__ == "__main__":
    main()
