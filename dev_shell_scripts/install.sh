# this script will install any dependencies onto the machine
python3 -m venv .venv 
source .venv bin/activate 
rustc --version || curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

pip install maturin
maturin develop
