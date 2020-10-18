
from SFC import get_SFC_features
from glob import glob
import numpy as np
import concurrent.futures as cf


def map_args(SFC_args):
    arr, fname, bmap_dest = SFC_args
    return get_SFC_features(arr=arr, fname=fname, bmap_dest=bmap_dest)


def binarize(source, bmap_dest):
    npz_path_list = glob(source)
    get_npz = (np.load(npz_path, mmap_mode='r', allow_pickle=True)
               for npz_path in npz_path_list)
    df_list = []

    for _, _ in enumerate(npz_path_list):
        npz = get_npz.__next__()
        fnames = npz[npz.files[0]]
        mfiles = npz[npz.files[1]]
        exts = npz[npz.files[2]]
        SFC_args = ((mfile, fname, bmap_dest) for mfile, fname in
                    zip(mfiles, fnames))

        with cf.ProcessPoolExecutor() as executor:
            result_list = [result for result in executor.map(map_args,
                                                             SFC_args,
                                                             chunksize=100)]


if __name__ == '__main__':
    binarize(r'data/vshare_out_data/vshare_29G/*.npz',
             r'out/b_maps/test')
