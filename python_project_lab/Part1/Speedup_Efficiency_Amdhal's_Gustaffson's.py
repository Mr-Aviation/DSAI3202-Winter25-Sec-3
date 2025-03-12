
sequential_time = 0.00135
threading_time = 0.00312
processes_time = 0.11966
num_threads = 2
num_processes = 2

speedup_threading = sequential_time / threading_time
speedup_processes = sequential_time / processes_time

efficiency_threading = speedup_threading / num_threads
efficiency_processes = speedup_processes / num_processes

print("Speedup Calculation")
print(f"        Speedup Threading: {speedup_threading}")
print(f"        Speedup Processes: {speedup_processes}")

print(f"\nEfficiency Calculation")
print(f"        Efficiency Threading: {efficiency_threading}")
print(f"        Efficiency Processes: {efficiency_processes}")

N = 2 #no.of processes/threads
P = 6/25 #no.of code lines used to create/start/join a process or thread divided by total lines of code

Speedup_Amdahl = 1 / ( (1 - P) + (P / N) )
Speedup_Gustaffson = P * (1 + N / (1 - P))

print(f"\nSpeedup using Amdhal's Law: {Speedup_Amdahl}")
print(f"Speedup using Gustaffson's Law: {Speedup_Gustaffson}")
print("\nBoth of the above laws give a value that is a multiplier/ratio of the total lines of code.")