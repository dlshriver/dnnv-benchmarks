# PLNN TwinStream

This is the TwinStream benchmark, originally introduced in [Piecewise Linear Neural Network verification: A comparative study](https://arxiv.org/pdf/1711.00455v1.pdf) by Bunel et al. for evaluation of the PLNN Branch-and-Bound verifier (i.e., BaB and BaBSB in DNNV).

This benchmark was designed in an attempt to learn the factors that influence verifier performance. 
The networks contain two separate data streams, each with the same architecture, weights, and inputs. 
The final layer computes the difference between the outputs of the two streams, and adds a positive bias term.
As a result, the final output will always be equal to the final bias value.
The property for this network is that the output of the network must be positive, which is true by construction.


## Benchmark Description

The problems are listed in `problems.csv`.
There are 81 problems total, consisting of 1 global reachability property applied to 81 networks of various fully-connected architectures.
The networks are provided in the `onnx` directory.
The single property specification is provided in the `properties` directory.
In addition to the networks and properties, we provide the scripts we used to generate the networks in the `src` directory.
These scripts were adapted from those in the [oval-group/PLNN-Verification](https://github.com/oval-group/PLNN-verification) repo to output DNNP and ONNX rather than RLV.
