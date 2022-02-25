# DNNV Benchmarks

A collection of DNN verification benchmarks, specified in 
[DNNP](https://dnnv.readthedocs.io/en/stable/usage/specifying_properties.html) 
and 
[ONNX](https://onnx.ai) 
for use with [DNNV](https://github.com/dlshriver/DNNV)
and [DNNF](https://github.com/dlshriver/DNNF).

## Usage

To access the benchmarks, simply clone this repo:

```bash
$ git clone https://github.com/dlshriver/benchmarks.git
```

We currently include 7 benchmarks in DNNP and ONNX format.
Each one is in its own sub-directory in the `benchmarks` directory, and each has a README with a description of the benchmark.

We also include some useful tool scripts in the `tools` directory.
`tools/resmonitor.py` will run a command with specified memory and time limits.
`tools/run_dnnv.py` can run all the problems in a specified benchmark using dnnv on multiple processes with resource limits.

To check the problems in the benchmarks, 
first [install DNNV](https://github.com/dlshriver/DNNV/tree/develop#installation),
as well as whichever verifiers you wish to use.
After installation, DNNV can be run on a single problem as follows:

```bash
$ dnnv /path/to/property --network N /path/to/network --VERIFIER
```

For example, to run the [nnenum](https://github.com/stanleybak/nnenum) verifier on property 1 and network `N_1_1.onnx` from the ACAS Xu benchmark, run:

```bash
$ dnnv benchmarks/ACAS_Xu/properties/property_1.py --network N benchmarks/ACAS_Xu/onnx/N_1_1.onnx --nnenum
```

To run all of the problems in a benchmark, we provide `tools/run_dnnv.py`. 
This tool expects both DNNV and [pandas](https://pypi.org/project/pandas/) to be installed.

```bash
$ tools/run_dnnv.sh -b /path/to/benchmark/dir/ -p /path/to/problems_csv --VERIFIER
```

For example, to run the [nnenum](https://github.com/stanleybak/nnenum) verifier on the ACAS Xu benchmark, run:

```bash
$ tools/run_dnnv.sh -b benchmarks/ACAS_Xu -p problems_original.csv --nnenum
```

Additional options (such as those for restricting the time and memory usage) can be seen by running:

```bash
$ tools/run_dnnv.sh -h
```

Any additionally specified arguments will be passed directly to DNNV.
