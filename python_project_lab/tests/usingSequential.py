import time
import random
import string

def join_random_characters():
    letters = ""
    for i in range(1000):
        letters = letters + random.choice(string.ascii_letters)
    #print(letters)
    print("Joining characters task done!")

def add_random_numbers():
    numbers = 0
    for i in range(1000):
        numbers = numbers + random.randint(1, 1000)
    #print(numbers)
    print("Adding numbers task done!")

starting_time = time.time()

join_random_characters()
add_random_numbers()

ending_time = time.time()

print(f"Total time taken is: {ending_time - starting_time} seconds.")
print("Exiting Program!")