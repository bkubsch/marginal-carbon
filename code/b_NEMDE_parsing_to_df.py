import pandas as pd
import glob
import os
import xml.etree.ElementTree as ET

def xml_to_dataframe(path_chunks, path_destination):
    '''
    Divide whole dataset into chunks procssable for available computing power.
    E.g. divide 10,000 files into 10 x 1000 files chunks. Per chunk, prepare one folder for 1000 files each time (here: 10 folders)
    path_chunks="directory to location of chunks to parsed"
    path destination="directory to store chunks as one file at a time (here: 10 files)"
    '''
    len(os.listdir(path_chunks))
    lst = list(range(1,len(os.listdir(path_chunks)) + 1))

    for i in lst:
        print(i)
        path_chunk_i = path_chunks + '/{}'.format(i)
        print(path_chunk_i)
        glob.glob(path_chunk_i)
        os.chdir(path_chunk_i)

        extension = 'xml'
        all_filenames = [i for i in glob.glob('**/*.{}'.format(extension), recursive=True)]

        print(len(all_filenames))

        data = []
        for j in all_filenames:
            root = ET.parse(j).getroot()
            attributes = ([c.attrib for c in root])
            for k in attributes:
                data.append(k)

        print("Next please")
        df = pd.DataFrame(data)
        df.to_pickle(path_destination + '/{}.pkl'.format(i))
        


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