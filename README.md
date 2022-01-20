# DNNV Benchmarks

A collection of DNN verification benchmarks, specified in 
[DNNP](https://dnnv.readthedocs.io/en/stable/usage/specifying_properties.html) 
and 
[ONNX](https://onnx.ai) 
for use with DNNV.

## Usage

This repository uses [git-lfs](https://github.com/git-lfs/git-lfs) to help manage large files, such as ONNX models.
To use the benchmarks in this repo, you will first need to install git-lfs on your system following the [installation instructions](https://github.com/git-lfs/git-lfs#installing) for your system.
After installation, be sure to run `git lfs install` to ensure that git-lfs is properly configured.

Once git-lfs is installed, simply clone this repo:
```bash
$ git clone https://github.com/dlshriver/benchmarks.git
```

We currently include 5 benchmarks in DNNP and ONNX format.
Each one is in its own sub-directory in the `benchmarks` directory, and each has a README with a description of the benchmark.

We also include some useful tool scripts in the `tools` directory.
`tools/resmonitor.py` will run a command with specified memory and time limits.
`tools/run_dnnv.py` can run all the problems in a specified benchmark using dnnv on multiple processes with resource limits.
