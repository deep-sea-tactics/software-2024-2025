use pyo3::prelude::*;

//Hey! If you intend to add extra functionality to this repository with Rust, please create a new module folder.
//Unless of course you're writting debug code and bindings between Python. You probably don't have to worry about this though... 

mod simulation;

/// Lil' test function written by the engineers over at PyO3
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// Main python module for all things rust related.
#[pymodule]
fn rust_robot(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
