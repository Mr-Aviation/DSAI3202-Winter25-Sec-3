
import time

def sequential_sum(n):
    start_time = time.time()
    total = sum(range(1, n + 1))
    end_time = time.time()
    print(f"Sequential Sum: {total}, Time: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    N = 10**7
    sequential_sum(N)
