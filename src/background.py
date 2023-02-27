import random
import time

import pyRAPL

def warmup():
    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    # Continuously calculate fibonacci numbers for the specified time
    start_time = time.time()
    r = 0
    i = 0
    while time.time() - start_time < 60:
        r = fibonacci(i)
        i += 1
    else:
        print(f"Warmup number: {i}th fibonacci number is {r}")

if __name__ == '__main__':
    pyRAPL.setup()
    random.seed(42)

    warmup()
    time.sleep(15)
    m = pyRAPL.Measurement("bg")
    s = time.time()
    m.begin()
    time.sleep(60)
    m.end()

    print(f"{m.result.pkg[0]}, {m.result.dram[0]}, {time.time() - s}")

