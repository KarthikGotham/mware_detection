import numpy as np

RESUME_FROM = 0
WRITE_THRESH = 5000

def numpyfy_benign_ingest(ext='exe'):
    data_list = []
    fname_list = np.load(r'data/lt1mb_{}.npy'.format(ext), allow_pickle=True)
    f_list = []
    for idx, fname in enumerate(fname_list[RESUME_FROM:], start=RESUME_FROM+1):
        try:
            with open(fname, 'rb') as bfile:
                data_list.append(np.array(list(bfile.read())))
                f_list.append(fname.__str__())
            if ((idx % WRITE_THRESH) == 0) or (idx == fname_list.__len__()):
                dat_np = np.array(data_list)
                np.savez(r'data/win_benign_out_data/{0}/win_{0}_{1}'.format(
                         ext, idx), f_list, dat_np)
                data_list = []
                f_list = []
                print(idx)
        except Exception:
            pass

if __name__ == "__main__":
    numpyfy_benign_ingest('exe')
    numpyfy_benign_ingest('dll')
