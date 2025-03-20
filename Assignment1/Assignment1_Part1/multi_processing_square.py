import time
import random
import multiprocessing
from concurrent.futures import ProcessPoolExecutor


def square(n):

    return n * n


def generate_numbers(size):

    numbers = []  

    for _ in range(size):  
        numbers.append(random.randint(1, 1000))  
    return numbers 


def sequential_square(numbers):

    results = []  

    for n in numbers:  
        results.append(square(n))  
    return results 


def multiprocessing_square(numbers):

    processes = []
    results = []

    for num in numbers:
        p = multiprocessing.Process(target=square, args=(num,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return results


def multiprocessing_pool_map(numbers):

    pool = multiprocessing.Pool()  
    result = pool.map(square, numbers)

    pool.close()  
    pool.join()

    return result  


def multiprocessing_pool_apply(numbers):

    pool = multiprocessing.Pool()  
    result = []  

    for num in numbers:  
        result.append(pool.apply(square, (num,))) 

    pool.close()  
    pool.join()  

    return result  


def concurrent_futures(numbers):

    executor = concurrent.futures.ProcessPoolExecutor()
    result = list(executor.map(square, numbers))
    executor.shutdown()
    
    return result


def benchmark():

    sizes = [10**6, 10**7]

    for size in sizes:
        numbers = generate_numbers(size)
        print(f"\nTesting with {size} numbers")
        
        start = time.time()
        sequential_square(numbers)
        print("Sequential Time:", time.time() - start)
        
        start = time.time()
        multiprocessing_square(numbers)
        print("Multiprocessing (Individual Processes) Time:", time.time() - start)
        
        start = time.time()
        multiprocessing_pool_map(numbers)
        print("Multiprocessing Pool (map) Time:", time.time() - start)
        
        start = time.time()
        multiprocessing_pool_apply(numbers)
        print("Multiprocessing Pool (apply) Time:", time.time() - start)
        
        start = time.time()
        concurrent_futures(numbers)
        print("Concurrent Futures Time:", time.time() - start)


if __name__ == "__main__":
    benchmark()