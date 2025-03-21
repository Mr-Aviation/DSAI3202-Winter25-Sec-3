Q3 Remarks 

Benchmark Results for 1,000,000 Numbers  
```
Sequential execution time: 0.0481 sec  
Multiprocessing Pool (map, synchronous): 0.1006 sec  
Multiprocessing Pool (map_async, asynchronous): 0.1001 sec  
Multiprocessing Pool (apply, synchronous): 189.1396 sec  
Multiprocessing Pool (apply_async, asynchronous): 43.5481 sec  
Concurrent.futures: 99.7121 sec  
```

Benchmark Results for 10,000,000 Numbers  
```
Sequential execution time: 0.4284 sec  
Multiprocessing Pool (map, synchronous): 0.7202 sec  
Multiprocessing Pool (map_async, asynchronous): 0.5112 sec  
Multiprocessing Pool (apply_async, asynchronous): 486.4132 sec  
```

Main Takeaways  
- The **`apply` method (synchronous)** was very slow, taking **189 seconds for 1M numbers**.  
- **`apply_async` (asynchronous)** was a bit better but still slower than **map-based** methods.  
- **Concurrent.futures** was also much slower than `map()`.  
- Some tests for **10M numbers** could not run because they needed too much memory.  
- The **`apply()` method (synchronous)** was not tested for 10M numbers because it was too slow.  
- **`map()` and `map_async()`** were the fastest and most efficient.  

---  

Q4 Remarks 

What Happens When Too Many Connections Are Requested?
- If more processes try to connect than available, they have to **wait** until one is free.  
- A **semaphore** controls access, allowing only `max_connections` at a time.  

How the Semaphore Prevents Problems:
- The **`acquire()` method** stops extra processes from connecting until space is available.  
- The **`release()` method** gives back used connections so others can use them, keeping things organized.

