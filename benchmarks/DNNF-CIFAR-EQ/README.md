# DNNF-CIFAR-EQ

The CIFAR-EQ benchmark was introduced to evaluate the effectiveness of property reductions for enabling the application of falsification tools in [Reducing DNN Properties to Enable Falsification with Adversarial Attacks](https://davidshriver.me/files/publications/ICSE21-DNNF.pdf) by Shriver et al.
The benchmark includes several different types of differencing or equivalence properties.

## Benchmark Description

This benchmark consists of four problem sets: CIFAR-EQ-GlobalDiff, CIFAR-EQ-GlobalEquivalence, CIFAR-EQ-LocalDiff, and CIFAR-EQ-LocalEquivalence.
All problems sets are comprised of either equivalence or differencing properties between two networks trained on the CIFAR10 dataset.
The models are the `onnx/convBigRELU__DiffAI.onnx` and `onnx/ResNet18__DiffAI.onnx` which are ONNX versions of two models from the [ERAN-CIFAR10 benchmarks](https://github.com/eth-sri/eran#neural-networks-and-datasets).

CIFAR-EQ-GlobalDiff is comprised of 90 properties that specify a difference property between the two networks.
For this benchmark, we create a property for each pair of distinct output classes `A` and `B` and specify that if one network predicts class `A`, then the other cannot predict class `B`.

CIFAR-EQ-GlobalEquivalence is comprised of a single property that asserts class-level equivalence between the two networks on all inputs.

CIFAR-EQ-LocalDiff is comprised of 90 properties that specify a difference property between the two networks, local to a given input.
These properties specify that if either of the networks predicts the correct class `C` on an input within some L-infinity distance `epsilon` of a given input point `x`, then the other network must not predict a different class `B` on that input.
The properties were created by selecting the first 10 images from the CIFAR10 dataset which were correctly classified by both networks, and creating one property for each possible wrong prediction, giving 9 properties per input.
In the original study two epsilon values were used, 1/255 and 10/255, which can be specified to DNNV with the option `--prop.epsilon=0.003922` and `--prop.epsilon=0.03922`.

CIFAR-EQ-LocalEquivalence is comprised 10 properties that asserts class-level equivalence between the two networks around a given input point.
For these properties, we use the same 10 input points as defined previously and assert that the networks must predict the same class on all input values within an L-infinity distance of `epsilon` from the given point.
As before, the original study used two epsilon values, 1/255 and 10/255, which can be specified to DNNV with the option `--prop.epsilon=0.003922` and `--prop.epsilon=0.03922`.
