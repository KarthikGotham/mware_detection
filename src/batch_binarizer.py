'''
Multiprocessing based batch binarizer
written to read binaries, generate SFCs
and extract histograms for every quarter
of the SFC images
'''
from SFC import get_SFC_features
from glob import glob
import pandas as pd
import numpy as np
import concurrent.futures as cf
from time import time


def map_args(SFC_args):
    arr, fname, bmap_dest = SFC_args
    return get_SFC_features(arr=arr, fname=fname, bmap_dest=bmap_dest)


def binarize(source, dest, bmap_dest):
    npz_path_list = glob(source)
    get_npz = (np.load(npz_path, mmap_mode='r', allow_pickle=True)
               for npz_path in npz_path_list)
    df_list = []

    start_time = time()
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
        end_time = time()
        print('Elapsed Time: ', end_time - start_time)

        df_chunk = pd.DataFrame(result_list)
        df_chunk['mfile_name'] = fnames
        df_chunk['ftype'] = exts
        df_list.append(df_chunk)

    df = pd.concat(df_list, axis=0)
    df.to_csv(dest, index=False)


if __name__ == '__main__':
    binarize(r'data/vshare_out_data/vshare_29G/*.npz',
             r'out/test_hist_ft_vshare_29G.csv',
             r'out/b_maps/test')

    # binarize(r'data/win_benign_out_data/dll/*.npz',
    #          r'out/train_hist_ft_benign_dll.csv')
    # binarize(r'data/win_benign_out_data/exe/*.npz',
    #          r'out/train_hist_ft_benign_exe.csv')
