#!/usr/bin/env python
import numpy as np
from scurve import fromSize
from PIL import Image
import os

SIZE = 256**2
TOT_SIZE = 2**18

bins = np.arange(0, 257)
mapping = fromSize(curve="hilbert", dimension=2, size=SIZE)
mapping = np.array(list(mapping), dtype='uint16')
mapping = np.vstack([mapping]*4)
for i in range(1, 4):
    mapping[i*SIZE:(i+1)*SIZE, 1] += (i*256)

x = mapping[:, 0]
y = mapping[:, 1]


def get_SFC_features(arr=None,
                     fname=None,
                     bytecode=False,
                     bmap_dest=None,
                     hist_features=True):
    if arr is None:
        with open(fname) as f:
            data = f.read()
            if bytecode:
                arr = np.array(data.split())
                del_mask = np.arange(0, arr.size, 17)
                arr = np.delete(arr, del_mask)
                # TODO: Few files are plagued with ?? characters. Research.
                arr = np.array([int(i, 16) for i in arr if i != '??'],
                               dtype='uint8')
            else:
                arr = np.array(list(data), dtype='uint8')

    out = np.zeros((1024, 256), dtype='uint8')

    step = len(arr)/float(TOT_SIZE)

    off = np.arange(TOT_SIZE, dtype='uint32')
    off = np.multiply(off, step).astype('uint32')

    try:
        out[[y], [x]] = arr[off]
    except IndexError:
        return np.zeros((1024), dtype='uint32')
    else:
        if bmap_dest:
            im = Image.fromarray(out)
            out_path = os.path.join(bmap_dest, fname+'.jpeg')
            im.save(out_path)

        # Ideally, dtype has to be uint32 as max would be (1 + 2**16)
        # but encountering such scenario is close to impossible
        if hist_features:
            feature_vec = [np.histogram(out[256*i:256*(i+1), :].flatten(),
                           bins=bins)[0] for i in range(4)]
            feature_vec = np.array(feature_vec, dtype='uint32')
            return feature_vec.flatten()


if __name__ == '__main__':
    get_SFC_features(fname=r'data/malware-classification/train/ \
                             58kxhXouHzFd4g3rmInB.bytes',
                     bytecode=True)
