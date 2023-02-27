import pyRAPL
from statistics import mean
import time
import random
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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
    while time.time() - start_time < WARMUP_TIME:
        r = fibonacci(i)
        i += 1
    else:
        print(f"Warmup number: {i}th fibonacci number is {r}")


def measure_remote():
    measurement = pyRAPL.Measurement("remote!")

    element = WebDriverWait(driver, timeout=100).until(lambda d: d.find_element(By.CSS_SELECTOR, ".split-menu-button"))

    measuring = False
    results = []
    s = 0
    while len(results) < N:
        time.sleep(0.1)
        loading = element.get_attribute("data-ol-loading")
        if not measuring and loading == "false":
            pass
        elif not measuring and loading == "true":
            measurement.begin()
            measuring = True
            s = time.time()
        elif measuring and loading == "false":
            measurement.end()
            measuring = False
            pkg, dram = measurement.result.pkg[0] / 1_000_000, measurement.result.dram[0] / 1_000_000
            print(f"{pkg}, {dram}, {(time.time() - s):.4f}")
            results.append((pkg, dram, time.time() - s))
            measurement = pyRAPL.Measurement("remote!")

    pkg_avg = mean([x[0] for x in results])
    dram_avg = mean([x[1] for x in results])
    print(f"pkg average: {pkg_avg}J")
    print(f"dram average: {dram_avg}J")
    print(f"total average: {pkg_avg + dram_avg}J")

    with open(OUT_FILE, "a+") as outfile:
        for r in results:
            outfile.write(f"{r[0]}, {r[1]}, {r[2]:.4f}\n")

if __name__ == '__main__':
    OUT_FILE = "out-online.csv"
    WARMUP_TIME = 60
    N = 5

    pyRAPL.setup()
    random.seed(42)

    opts = FirefoxOptions()
    driver = webdriver.Firefox(options=opts, service=FirefoxService("/home/otto/geckodriver"))

    driver.get("https://overleaf.com/login")
    driver.find_element(By.NAME, "email").send_keys("sseoverleaf@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("password")

    warmup()

    measure_remote()

    driver.quit()




