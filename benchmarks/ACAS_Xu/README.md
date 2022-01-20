# ACAS Xu

This is the ACAS Xu benchmark, originally introduced in [Reluplex: An Efficient SMT Solver for Verifying Deep Neural Networks](https://arxiv.org/pdf/1702.01135.pdf) by Katz et al. for evaluation of the Reluplex verifier. 
It has since been used extensively by other verifiers, and has been used consistently used as a benchmark in VNN-COMP ([2020](https://sites.google.com/view/vnn20/vnncomp), [2021](https://arxiv.org/pdf/2109.00498.pdf)).

## Benchmark Description

We provide 2 problem sets for ACAS Xu.
The first is the original set of verification problems posed by Katz et al.
The problems for this benchmark are in `problems_original.csv`.
The second set is the set of verification problems used by several evaluations since then, such as VNN-COMP.
This set contains all problems in the first benchmark, but also extends the application of the first 4 properties to all networks, increasing the size of the benchmark by 15 problems.
The problems for this benchmark are in `problems_extended.csv`.

The two benchmarks use the same 45 networks, which can be found in ONNX format in the `onnx` directory.
Each network is named with the convention `N_aprev_tau`, where `aprev` is the index of the previous advisory ([[Clear-of-Conflict, weak left, weak right, strong left, strong right]), and `tau` is the index of the discretized time to vertical separation (`[0, 1, 5, 10, 20, 40, 60, 80, 100]`).

Both benchmarks use the same 10 property specifications, which can be found in the `properties` directory.
Each property is specified in DNNP and includes a text description of the property semantics.
Because the ACAS Xu networks expect normalized inputs, the specifications normalize values by their corresponding mean and range.
