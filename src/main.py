import os

import pyRAPL
import subprocess
from statistics import mean
import time
import random
# selenium 4
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def experiment(exps):
    # list comprehension magic
    # Shuffles a list of n times each experiment
    exps = [e for sub in [[x for _ in range(N)] for x in exps] for e in sub]
    if SHUFFLE:
        random.shuffle(exps)

    results = {e[0].__name__: [] for e in exps}

    for f, setup in exps:
        results[f.__name__].append(measure(f, setup))
        # pause between experiments
        time.sleep(PAUSE)

    for f, res in results.items():
        pkg_avg = mean([x[0] for x in res])
        dram_avg = mean([x[1] for x in res])
        t_avg = mean([x[2] for x in res])
        print(f"{f} pkg average: {pkg_avg}J")
        print(f"{f} dram average: {dram_avg}J")
        print(f"{f} total average: {pkg_avg + dram_avg}J")
        print(f"{f} time average: {t_avg}s")


    print("-----------------")
    with open(OUT_FILE, "a+") as outfile:
        for f, res in results.items():
            for r in res:
                outfile.write(f"{f}, {r[0]}, {r[1]}, {r[2]:.4f}\n")

def measure(func, setup):
    if setup:
        setup()
    measurement = pyRAPL.Measurement(func.__name__)
    s = time.time()
    measurement.begin()
    func()
    measurement.end()
    t = time.time() - s

    # Convert from uJ to J
    pkg, dram = measurement.result.pkg[0] / 1_000_000, measurement.result.dram[0] / 1_000_000
    print(f"Measured {func.__name__}: ({pkg}, {dram}) in {t:.2f} seconds")

    return pkg, dram, t


def book_local():
    subprocess.run("./src/compile-book-local.sh")

def blog_local():
    subprocess.run("./src/compile-blog-local.sh")

def blog_hosted_setup():
    BLOG_URL = "http://localhost/project/63ff49bdc0334900a1e33022"
    driver.get(BLOG_URL)
    WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.CSS_SELECTOR, ".btn-recompile[aria-label='Recompile']"))
    time.sleep(4)

def book_hosted_setup():
    BOOK_URL = "http://localhost/project/63ff653ace38db008f3b5c12"
    driver.get(BOOK_URL)
    WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.CSS_SELECTOR, ".btn-recompile[aria-label='Recompile']"))
    time.sleep(4)

def book_hosted():
    driver.find_element(By.ID, "pdf-recompile-dropdown").click()
    f = driver.find_element(By.CSS_SELECTOR, "ul[aria-labelledby='pdf-recompile-dropdown'] > li:last-of-type")
    f.click()
    WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.CSS_SELECTOR, ".btn-recompile[aria-label='Recompile']"))

def blog_hosted():
    driver.find_element(By.ID, "pdf-recompile-dropdown").click()
    f = driver.find_element(By.CSS_SELECTOR, "ul[aria-labelledby='pdf-recompile-dropdown'] > li:last-of-type")
    f.click()
    WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.CSS_SELECTOR, ".btn-recompile[aria-label='Recompile']"))

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


if __name__ == '__main__':
    OUT_FILE = "out.csv"
    WARMUP_TIME = 60
    N = 30
    PAUSE = 15
    SHUFFLE = True

    try:
        os.remove(OUT_FILE)
    except FileNotFoundError:
        pass

    exps_local = [(book_local, None), (blog_local, None)]
    exps_hosted = [(blog_hosted(), blog_hosted_setup), (book_hosted, book_hosted)]

    pyRAPL.setup()
    random.seed(42)

    warmup()

    experiment(exps_local)

    opts = FirefoxOptions()
    driver = webdriver.Firefox(options=opts, service=FirefoxService("/home/otto/geckodriver"))

    driver.get("http://localhost/login")
    driver.find_element(By.NAME, "email").send_keys("sseoverleaf@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, ".actions button").click()
    time.sleep(3)

    print("Switching to overleaf testing, waiting for fairness")
    time.sleep(2*PAUSE)
    warmup()


    experiment(exps_hosted)

    driver.quit()
