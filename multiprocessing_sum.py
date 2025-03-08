
import time
import multiprocessing

def sum_range(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def process_sum(n, num_processes=4):
    start_time = time.time()
    step = n // num_processes
    with multiprocessing.Manager() as manager:
        results = manager.list([0] * num_processes)
        processes = []
        
        for i in range(num_processes):
            start = i * step + 1
            end = (i + 1) * step if i != num_processes - 1 else n
            process = multiprocessing.Process(target=sum_range, args=(start, end, results, i))
            processes.append(process)
            process.start()
        
        for process in processes:
            process.join()
        
        total = sum(results)
    end_time = time.time()
    print(f"Multiprocessing Sum: {total}, Time: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    N = 10**7
    process_sum(N)
