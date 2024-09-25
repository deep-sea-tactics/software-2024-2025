## Note
This is the directory for all things Rust. If you intend to write **Python** code, **please do it in** `<project>/python_src.`

If any utility is performance critical, it will be written in Rust and be given its own separate module.

### Organization

Each module gets its own folder and is tied into `lib.rs`.

Consider `lib.rs` to be the 'glue' between Python and Rust.