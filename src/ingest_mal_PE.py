'''
This script ingests malware
PE files from virusShare
archives and save the content
as ASCII codes
'''

from zipfile import ZipFile
from tqdm import tqdm
from utils import is_pe
import numpy as np
import os

RESUME_FROM = 0
WRITE_THRESH = 1000
PWD = b'infected'
PE_FMT_ID = b'MZ'


def write_archive(data_list, fname_list, idx, ext_list, out_dir):
    dat_np = np.array(data_list)
    np.savez(os.path.join(out_dir, str(idx)),
             np.array(fname_list), dat_np, np.array(ext_list))


def ingest_malware(input_arch, out_dir):
    data_list = []
    fname_list = []
    ext_list = []
    with ZipFile(input_arch) as hotzip:
        mware_fname = hotzip.namelist()
        for idx, fname in tqdm(enumerate(mware_fname[RESUME_FROM:],
                                         start=RESUME_FROM+1)):
            with hotzip.open(fname, pwd=PWD) as mfile:
                content = mfile.read()
                if content[:2] == PE_FMT_ID:
                    ext = is_pe(content)
                    if ext:
                        data_list.append(np.array(list(content),
                                                  dtype='uint8'))
                        fname_list.append(fname)
                        ext_list.append(ext)

            if (((idx % WRITE_THRESH) == 0) or (idx == mware_fname.__len__())):
                write_archive(data_list, fname_list, idx, ext_list, out_dir)
                data_list = []
                fname_list = []
                ext_list = []
                print(idx)


if __name__ == "__main__":
    ingest_malware(r'data/VirusShare_00375.zip',
                   r'data/vshare_out_data/vshare_29G')
