# Neurify DAVE

This is the Neurify-DAVE benchmark, originally introduced in [Efficient Formal Safety Analysis of Neural Networks](https://arxiv.org/pdf/1809.08098.pdf) by Shiqi Wang et al., for the evaluation of the Neurify verifier.
The problems are local reachability properties specified for a network based on the [DAVE](https://arxiv.org/pdf/1604.07316.pdf) model, which was trained to predict steering angles given images from a vehicle mounted front-facing camera.
While the original benchmark used a smaller version of the DAVE network, further usage of the benchmark has included a larger DAVE model.

## Benchmark Description

We provide 2 problem sets for Neurify-DAVE.
The first is the original set of verification problems posed by Shiqi Wang et al.
The problems for this benchmark are in `problems_original.csv`.
The problem set consists of 10 local reachability problems.
The second set is the set of verification problems used by several evaluations since then, such as [DNNF](https://davidshriver.me/files/publications/ICSE21-DNNF.pdf).
This set contains all problems in the first benchmark, but also includes a larger DAVE model and associated properties.
The problems for this benchmark are in `problems_extended.csv`.
The problem set consists of 20 local reachability problems.
For both sets of problems the L-infinity radius on the input can be specified using the `--prop.epsilon=X` option to DNNV.

The two networks are provided in the `onnx` directory.
The original benchmark's smaller model is `dave_small.onnx`, while the extended benchmark also includes the larger `dave.onnx`.
Both networks have been trained on the same task.
The two networks expect different input normalization.

The properties are provided in the `properties` directory.
There are 10 local reachability properties for each network.
Each specification performs the necessary input normalization for their corresponding network.
