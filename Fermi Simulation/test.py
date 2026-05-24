import numpy as np
import matplotlib.pyplot as plt
import time

for i in range(5):
    print(f"Running test {i + 1}/5...\r", end="")
    time.sleep(1)  # Simulate some work being done