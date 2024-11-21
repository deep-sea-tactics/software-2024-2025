# Deep Sea Tactics Software
## 2024-2025

This is the official repository for the Deep Sea Tactics Software team 2024-2025. Not to be confused with the `software` repository, which isn't the primary repository for the 2024-2025 year.

If you're reading this, you're in the right place for software!

## IMPORTANT!

Please don't commit directly to the `main` branch unless all the features you're writing are completely finished. For any development changes, please use the aptly named `development` branch.

## Technical Overview

This repository is written in Python and Rust using PyO3 bindings. This repository will be tested and used on a debian based linux. Furthermore, **this repository is designed to run on debian linux** (specifically rasbian). Please use a debian based distribution for all testing.

# Install guide:
### Run this once when downloading the repository for the first time/creating a new virtual workspace

*(Make sure you're in the `software-2024-2025/` directory!)*

In the terminal, run:

`source dev_shell_scripts/install.sh`

When prompted by rustup (the thing that installs rust) to 'set up the install,' simply press enter.

**Restart/kill and reopen** a new terminal

In the terminal, run:

`source .venv/bin/activate`
If a **venv** appears next to your current directory, the Python virtual environment has been successfully initialized.

`source dev_shell_scripts/install.sh` again to complete the installation of vital tools.

## Running/testing code

In the terminal, run

`source dev_shell_scripts/run.sh`

to compile everything Rust + load it into Python, and run the main python file. In the `dev_shell_scripts` directory, there are other commands for running each subsystem.

# Dependencies

For any and all Python libraries that *you add*, please append the `pip install` command to the `dev_shell_scripts/install.sh` script
