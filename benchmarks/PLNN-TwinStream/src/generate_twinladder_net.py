#!/usr/bin/env python
# based on the version in the PLNN-Verification repo
# https://github.com/oval-group/PLNN-verification/blob/9eb91f4a53d30aee432258d3f81bceffdbf49421/tools/generate_twinladder_net.py
import argparse
import torch

from pathlib import Path
from torch import nn

torch.set_default_tensor_type("torch.DoubleTensor")


def generate_network(ladder_dimension, margin):
    """
    Create a twin ladder network
    A twin ladder network is composed of two copies of the
    same network, each running separately on identical inputs.
    The final output is the difference between the two streams,
    which by construction should always be zero.

    We are going to make the two streams together.
    The first half of the variables correspond to the first stream
    The second half of the variables correspond to the second stream

    To account for numerical error, we will add a tiny bias to the output,
    and our final proof would be to show that we can't have a negative output.
    """

    stream = []
    nb_inputs = ladder_dimension[0]
    nb_stream_out = ladder_dimension[-1]

    inp_domain = torch.Tensor([[-10, 10]] * nb_inputs)

    prev_size = nb_inputs
    for lay_out_size in ladder_dimension[1:]:
        stream.append(nn.Linear(prev_size, lay_out_size, bias=True))
        prev_size = lay_out_size

    twin_net_layers = []
    # Add a linear layer duplicating the input
    dup_layer = nn.Linear(nb_inputs, 2 * nb_inputs)
    dup_weight = dup_layer.weight.data
    dup_bias = dup_layer.bias.data
    dup_weight.zero_()
    dup_bias.zero_()
    dup_weight[:nb_inputs, :] = torch.eye(nb_inputs)
    dup_weight[-nb_inputs:, :] = torch.eye(nb_inputs)
    twin_net_layers.append(dup_layer)

    # Create linear layers that are block diagonals
    # with the same blocks
    prev_size = 2 * nb_inputs
    for stream_lay in stream:
        nb_in = stream_lay.in_features
        nb_out = stream_lay.out_features
        twin_lay = nn.Linear(2 * nb_in, 2 * nb_out, bias=True)
        twin_lay_weight = twin_lay.weight.data
        twin_lay_bias = twin_lay.bias.data
        twin_lay_weight.zero_()

        twin_lay_weight[:nb_out, :nb_in].copy_(stream_lay.weight.data)
        twin_lay_weight[-nb_out:, -nb_in:].copy_(stream_lay.weight.data)
        twin_lay_bias[:nb_out].copy_(stream_lay.bias.data)
        twin_lay_bias[-nb_out:].copy_(stream_lay.bias.data)

        twin_net_layers.append(twin_lay)
        twin_net_layers.append(nn.ReLU())
        prev_size = 2 * nb_out

    # Delete the last ReLU created
    del twin_net_layers[-1]
    # Create the final linear layers that merge the two streams back
    closing_layer = nn.Linear(prev_size, 1, bias=True)
    closing_layer.bias.data.fill_(margin)
    closing_layer.weight.data[0, :nb_stream_out].fill_(1)
    closing_layer.weight.data[0, -nb_stream_out:].fill_(-1)

    twin_net_layers.append(closing_layer)

    return twin_net_layers, inp_domain


def main():
    parser = argparse.ArgumentParser(
        description="Generate a twin-ladder network problem"
        "according to the dimension given as CLI arguments."
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Where to write down the generated problem",
    )
    parser.add_argument(
        "network_name",
        type=str,
        help="Name of the generated network",
    )
    parser.add_argument(
        "property_name",
        type=str,
        help="Name of the generated property",
    )
    parser.add_argument(
        "margin",
        type=float,
        help="What should the margin by which the property is true?",
    )
    parser.add_argument(
        "ladder_dims",
        type=int,
        nargs="+",
        help="Dimension of each stage of the network",
    )
    parser.add_argument("--seed", type=int, default=0)

    args = parser.parse_args()
    assert len(args.ladder_dims) > 2, "Need several layers in the network"
    torch.manual_seed(args.seed)

    assert isinstance(args.output_dir, Path)
    args.output_dir.mkdir(exist_ok=True, parents=True)
    (args.output_dir / "onnx").mkdir(exist_ok=True, parents=True)
    (args.output_dir / "properties").mkdir(exist_ok=True, parents=True)

    network_layers, domain = generate_network(args.ladder_dims, args.margin)

    bounds = domain.numpy().T
    lb = bounds[:1]
    ub = bounds[1:]

    model = nn.Sequential(*network_layers)
    x = torch.from_numpy((ub + lb) / 2)
    torch.onnx.export(model, x, args.output_dir / "onnx" / f"{args.network_name}.onnx")

    specification = """from dnnv.properties import *
import numpy as np

N = Network("N")
input_lb = np.full(N.input_shape[0], -10, dtype=N.input_details[0].dtype)
input_ub = np.full(N.input_shape[0], 10, dtype=N.input_details[0].dtype)

Forall(x, Implies(input_lb <= x <= input_ub, N(x) > 0))
"""

    with open(
        args.output_dir / "properties" / f"{args.property_name}.py", "w+"
    ) as dnnp_file:
        dnnp_file.write(specification)

    with open(args.output_dir / "problems.csv", "a+") as f:
        f.write(
            f"{args.network_name},properties/{args.property_name}.py,N,onnx/{args.network_name}.onnx\n"
        )


if __name__ == "__main__":
    main()
