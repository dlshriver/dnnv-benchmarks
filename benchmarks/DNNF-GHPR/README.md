# DNNF-GHPR

The GHPR benchmark was introduced to evaluate the effectiveness of property reductions for enabling the application of falsification tools in [Reducing DNN Properties to Enable Falsification with Adversarial Attacks](https://davidshriver.me/files/publications/ICSE21-DNNF.pdf) by Shriver et al.

## Benchmark Description

This benchmark consists of two problem sets, GHPR-DroNet and GHPR-MNIST.

GHPR-Dronet, is a set of global halfspace-polytope reachability properties for the [DroNet](https://rpg.ifi.uzh.ch/docs/RAL18_Loquercio.pdf) network.
These problems are specified in `problems_dronet.csv`.
All problems in this problem set use the DroNet model, `onnx/dronet.onnx`.
The DroNet model is a large ResNet-based architecture which takes in images from a vehicle-mounted front-facing camera and predicts a steering angle and a probability of collision.
The GHPR-DroNet properties codify the desired behavior that, if the probability for collision is low, then the system should not make sharp turns. 
The properties are of the form: for all inputs, if the probability of collision is between `pmin` and `pmax`, then the steering angle is within `d` degrees of 0.

GHPR-MNIST, is a set of global halfspace-polytope reachability properties for two MNIST classifier models taken from the ERAN-MNIST dataset.
These problems are specified in `problems_mnist.csv`.
The problem set consists of 10 properties applied to 2 MNIST models.
The models, `onnx/convSmallRELU__Point.onnx` and `onnx/convMedGRELU__Point.onnx`, are taken from the ERAN-MNIST benchmark and have had normalization built into the front of the networks so that they accept input images with values between 0 and 1.
The GHPR-MNIST properties are of the form: for all inputs, the output values for classes `a` and `b` are closer to one another than either is to the output value of class `c`. 
The values of `a`, `b`, and `c` are selected from the confusion matrix of the medium-sized convolutional network on the MNIST test set, shown in the following table with the diagonal values removed. 
We select the 10 pairs of a and b with the most confusion. 
We then select a value for `c`, such that images of digit `a` were never classified as `c`, and images of digit `b` were never classified as `c`. 
As an example, we would select 4 and 9 for `a` and `b`, since images of fours were classified as nines 13 times, more than any other pair. We then select the value 8 for `c`, since no images of fours or nines were ever misclassified as eights. 

| True/Predicted Label |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |
| -------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|          0           |  *  |  1  |  1  |  0  |  1  |  0  |  0  |  0  |  2  |  1  |
|          1           |  0  |  *  |  1  |  3  |  0  |  1  |  0  |  0  |  0  |  0  |
|          2           |  1  |  2  |  *  |  1  |  0  |  0  |  1  |  2  |  0  |  0  |
|          3           |  0  |  0  |  0  |  *  |  0  |  1  |  0  |  2  |  1  |  4  |
|          4           |  0  |  0  |  1  |  0  |  *  |  0  |  4  |  2  |  0  |  13 |
|          5           |  2  |  0  |  1  |  10 |  0  |  *  |  1  |  1  |  1  |  1  |
|          6           |  7  |  3  |  0  |  1  |  2  |  3  |  *  |  0  |  0  |  0  |
|          7           |  1  |  4  |  7  |  1  |  0  |  0  |  0  |  *  |  1  |  3  |
|          8           |  4  |  0  |  5  |  10 |  0  |  4  |  0  |  2  |  *  |  5  |
|          9           |  2  |  3  |  0  |  2  |  4  |  2  |  0  |  3  |  0  |  *  |
