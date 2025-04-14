
from celery import Celery
from src.maze import create_maze
from src.explorer import Explorer

app = Celery('maze_tasks', broker='pyamqp://guest@localhost//', backend='rpc://')

@app.task
def run_explorer_task(index, maze_type, width, height):
    
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False)
    time_taken, moves = explorer.solve()
    
    return {
        "id": index,
        "time": time_taken,
        "moves": len(moves),
        "backtracks": 0  # A* doesn't use backtracking
    }

