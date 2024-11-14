# MAKE SURE YOU HAVE PYTHON INSTALLED!

# this script will install any dependencies onto the machine
python3 -m venv .venv 
source .venv bin/activate 
rustc --version || curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

echo please close and restart the terminal. then run this script again

pip install maturin
maturin develop