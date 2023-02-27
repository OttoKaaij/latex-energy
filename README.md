# Measuring energy for different latex usecases

**Please see the [accompanying blogpost](https://http.cat/404)!**

This project measures latex compilation for three different ways of compiling LaTeX:

- Local: Local compilation using `xelatex`
- Hosted: Overleaf compilation with overleaf hosted in a docker container running locally
- Cloud: Overleaf compilation on [overleaf.com](https://overleaf.com). Measure only the energy used by cpu and memory locally.

# How to run

This project only runs on intel based linux machines.
The project depends on the following things running and working on your machine.

1. Pipenv to install dependencies ([pyRAPL](https://pypi.org/project/pyRAPL/) [selenium](https://selenium-python.readthedocs.io/)). Run `Pipenv install`.
2. [Selenium](https://selenium-python.readthedocs.io/) should work on your machine
3. [Overleaf toolkit](https://github.com/overleaf/toolkit)
   - Make an account
   - Import the tex projects (from `./tex`) 
   - Update the login info and project URLs in the scripts
4. User access to `/sys/class/powercap/intel-rapl`. (run `sudo chmod -R a+r /sys/class/powercap/intel-rapl`)

# Run the experiments

There are three experiments: Background, Main and Cloud.
Before running an experiment, make sure:

- Power cable is plugged in
- No external monitor or other peripherals are connected
- Screen brightness is set to 100%
- Screen saver timer is turned off
- No other programs are open
- Airplane mode is turned on (i.e. no Bluetooth, no WiFi, no notifications), except for the cloud experiment.

## Main

Measures local and hosted energy usage.

1. run `pipenv run experiment`

## Cloud

Measures cloud energy usage. Not fully automatic, because overleaf will complain that you are a bot.

1. run `pipenv run experiment`
2. log in, and navigate to the project under test
3. wait until warmup is finished and the fibonacci number is printed
4. compile the document from scratch, wait for completion, wait 30 seconds, repeat.


## Background

Measures the background energy usage.

1. run `pipenv run bg`


