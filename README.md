# Deep Sea Tactics Software
## 2024-2025

This is the official repository for the Deep Sea Tactics Software team 2024-2025. Not to be confused with the `software` repository, which isn't the primary repository for the 2024-2025 year.

If you're reading this, you're in the right place for software!

## IMPORTANT!

Please don't commit directly to the `main` branch unless all the features you're writing are completely finished. For any development changes, please use the aptly named `development` branch.

## Technical Overview

This repository is written in Python and Rust using PyO3 bindings. This repository will be tested and used on a debian based linux. Furthermore, **this repository is designed to run on debian linux** (specifically rasbian). Please use a debian based distrobution for all testing.

# Install guide:
### Run this once when downloading the repository for the first time/creating a new virtual workspace

*(Make sure you're in the /workspace/software-2024-2025/ directory!)*

In the terminal, run:

`source dev_shell_scripts/install.sh`

When prompted by rustup (the thing that installs rust) to 'set up the install,' simply press enter.

**Restart/kill and reopen** a new terminal

In the terminal, run:

`source dev_shell_scripts/install.sh` again to complete the installation of vital tools.

## Virtual environment

In the terminal, run

`source .venv/bin/activate` to activate virtual environment. **For any dependencies to work, you must activate the virtual environment!**

Notice a little **(venv)** next to the path in your command line. This means you are now working in a python virtual environment.

## Running/testing code

In the terminal, run

`source dev_shell_scripts/run.sh`

to compile everything rust + load it into python, and run the main python file.

# Dependencies

For any and all Python libraries, please add the `pip install` command to the `dev_shell_scripts/install.sh` script