import time
import random
import multiprocessing
from multiprocessing import Semaphore


# Connection Pool with Semaphore
class ConnectionPool:
    def __init__(self, max_connections):

        self.pool = []

        for i in range(max_connections):
            self.pool.append(f"Connection-{i}")
        
        self.semaphore = Semaphore(max_connections)

    
    def get_connection(self):

        self.semaphore.acquire()

        return self.pool.pop()
    

    def release_connection(self, connection):

        self.pool.append(connection)
        self.semaphore.release()


# Simulating database access
def access_database(pool, process_id):

    print(f"Process {process_id} is waiting for a connection...")
    connection = pool.get_connection()

    print(f"Process {process_id} acquired {connection}")
    time.sleep(random.uniform(1, 3))  # Simulate DB operation

    pool.release_connection(connection)
    print(f"Process {process_id} released {connection}")


def test_connection_pool():

    pool = ConnectionPool(max_connections=3)

    processes = []
    
    for i in range(6):
        process = multiprocessing.Process(target=access_database, args=(pool, i))
        processes.append(process)

    
    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    test_connection_pool()