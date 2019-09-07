import pandas as pd
import glob
import os

def clean_filter_concat_pkl(path_pkls, path_destination):
    os.chdir(path_pkls)
    extension = 'pkl'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    df = pd.DataFrame()
    for i in all_filenames:
        print(i)
        df_i = pd.read_pickle(i)
        print(df_i.shape)
        df_i = df_i.query('Market == "Energy" and RegionID == "SA1"')
        df = pd.concat([df, df_i])
        print(df.shape)
    df.to_pickle(path_destination)