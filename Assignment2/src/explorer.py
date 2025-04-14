import time
import heapq
import pygame
from typing import Tuple, List
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        self.backtrack_count = 0
        self.maze = maze
        self.start = maze.start_pos
        self.end = maze.end_pos
        self.visualize = visualize
        self.path = []
        self.time_taken = 0

        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - A* Pathfinding")
            self.clock = pygame.time.Clock()

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.maze.width and 0 <= ny < self.maze.height
                    and self.maze.grid[ny][nx] == 0):
                neighbors.append((nx, ny))
        return neighbors

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        self.path = path

    def draw_state(self, pos):
        self.screen.fill(WHITE)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.start[0] * CELL_SIZE, self.start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.end[0] * CELL_SIZE, self.end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLUE, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        self.clock.tick(60)

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        start_time = time.time()
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.end)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == self.end:
                self.time_taken = time.time() - start_time
                self.reconstruct_path(came_from, current)
                if self.visualize:
                    for step in self.path:
                        self.draw_state(step)
                    pygame.time.wait(2000)
                    pygame.quit()
                self.print_statistics()
                return self.time_taken, self.path

            for neighbor in self.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, self.end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        self.time_taken = time.time() - start_time
        return self.time_taken, []

    def print_statistics(self):
        print("\n=== A* Maze Exploration Statistics ===")
        print(f"Total time taken: {self.time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.path)}")
        print(f"Average moves per second: {len(self.path) / self.time_taken if self.time_taken else 0:.2f}")
        print("====================================\n")
