#!/usr/bin/env python
import numpy as np
import skimage.io as sio
import sys

from pathlib import Path

npy_path = Path(sys.argv[1])
if len(sys.argv) == 2:
    out_path = npy_path.parent / f"{npy_path.stem}.png"
else:
    out_path = Path(sys.argv[2])

x = np.load(npy_path)
if x.ndim == 4 and x.shape[0] == 1:
    x = x[0]
if x.ndim != 3:
    print("counter example is not an image")
    exit(1)
sio.imsave(str(out_path), x.transpose(1, 2, 0))
