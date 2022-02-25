# Planet MNIST

This is the Planet MNIST benchmark, originally introduced in [Formal Verification of Piece-Wise Linear Feed-Forward Neural Networks](https://arxiv.org/abs/1705.01320) by Ruediger Ehlers for evaluation of the Planet verifier.


## Benchmark Description

The problems are listed in `problems.csv`.
There are 7 problems total, consisting of 4 global reachability properties, 2 local robustness properties with hyper-rectangle input constraints, and 1 local robustnes property with halfspace-polytope input constraints.

The network is provided in the `onnx` directory.
It as based on a LeNet model, and is converted to ONNX from the [trained caffe model](https://github.com/progirep/planet/blob/a898a86a352f4dbe369a555ba4aaed7f6d53bab6/casestudies/MNIST/snapshots/_iter_200000.caffemodel) in the Planet verifier repository.

The property specifications are provided in the `properties` directory.
There are 3 specifications, one for each property type.
The 4 global reachability properties use the `properties/givestrong.py` specification, which asserts that there is no input which produces an output vector where class 2 has a value of more than `delta` all other class values.
The 4 properties each specify a different value for the `--prop.delta` parameter: 20, 30, 35, 50.
The 2 local robustness properties with hyper-rectangle input constraints use the `properties/robustness.py` specification, which specify that inputs within an L-infinity distance of `epsilon` of a given input are not classified as a 4.
The two properties in the original benchmark use epsilon values of 0.08 and 0.12.
For the final local robustness property, rather than constraining the amplitude of the noise that can be added to a given image, the specification says that the noise added to adjacent pixels must not differ by more than a value of gamma.
The value of gamma used in this benchmark was 0.05.
For all local robustness properties, the chosen image on which to check robustness was the image with index 200 in the MNIST test dataset, which is the same image of a 3 used in the evaluation of planet.

Problems in the original benchmark were run with a timeout of 4 hours.
