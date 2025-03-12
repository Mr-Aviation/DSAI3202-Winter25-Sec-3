
import time
import threading

def sum_range(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def threaded_sum(n, num_threads=4):
    start_time = time.time()
    step = n // num_threads
    threads = []
    results = [0] * num_threads
    
    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step if i != num_threads - 1 else n
        thread = threading.Thread(target=sum_range, args=(start, end, results, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    total = sum(results)
    end_time = time.time()
    print(f"Threaded Sum: {total}, Time: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    N = 10**7
    threaded_sum(N)
