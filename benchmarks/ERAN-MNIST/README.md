# ERAN MNIST

This is the ERAN-MNIST benchmark, subsets of which were used in evaluations of the abstract domains introduced by the ERAN verifier (e.g., [DeepZono](https://files.sri.inf.ethz.ch/website/papers/DeepZ.pdf), [DeepPoly](https://files.sri.inf.ethz.ch/website/papers/DeepPoly.pdf), [RefineZono](https://files.sri.inf.ethz.ch/website/papers/RefineZono.pdf)).
We make available the MNIST networks from [this table](https://github.com/eth-sri/eran#neural-networks-and-datasets) as models in the ONNX format, and the 100 test properties used by ERAN are specified in DNNP.

## Benchmark Description

The problems are listed in `problems.csv`.
They are all local robustness properties, 3200 in total.
The properties are all specified with a default epsilon (i.e., L-infinity radius) of 2 pixel values (i.e., `2/255`).
This radius can be changed when running DNNV through the option `--prop.epsilon=X`, where X is the desired value.

The networks are provided in the `onnx` directory, with some networks in `onnx/tf` and `onnx/pyt` depending on their original file extension.
We keep the networks divided into 2 groups due to a difference in the input normalization of the two sets of networks.
The networks in `pyt` expect inputs to be normalized by subtracting 0.1307 and dividing by 0.3081, while the networks in `tf` do not expect any additional normalization on the inputs.

The properties are provided in the `properties` directory, again divided into `properties/pyt` and `properties/tf`.
The specifications in the `pyt` directory are specified with input normalization, while those in `tf` are not.
The files in `properties/inputs` are the 100 inputs used to specify the local robustness properties in this benchmark.
The same 100 inputs are common between the 2 sets of specifications, only the normalization within the specification differs.
