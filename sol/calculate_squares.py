
from mpi4py import MPI
import numpy as np
import time

def compute_squares(start, end):
    return [i ** 2 for i in range(start, end)]

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Adjust the upper limit here for larger tests (like 1e8)
N = int(1e6)

chunk_size = N // size
start_index = rank * chunk_size
end_index = start_index + chunk_size if rank != size - 1 else N

start_time = MPI.Wtime()

local_squares = compute_squares(start_index, end_index)

# Gather results at root
gathered = comm.gather(local_squares, root=0)

if rank == 0:
    all_squares = np.concatenate(gathered)
    print(f"Total squares computed: {len(all_squares)}")
    print(f"Last square value: {all_squares[-1]}")
    print(f"Time taken: {MPI.Wtime() - start_time:.4f} seconds")
