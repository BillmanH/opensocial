#%%
# Purpose: To scan through the drive and get some info on the scope and size of the data upload. 

import os
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

# %%
base_path = 'D:\FamilyPhotos'

dirs = os.listdir(base_path)
all_files = pd.DataFrame()



# %%

def has_access(ipath):
    try: 
        os.listdir(ipath)
        return True
    except PermissionError:
        return False

def has_items(ipath):
    df = [get_all_files_in_folder(path) for path in get_folders(ipath) if has_access(path)]
    if len(df)>0:
        return True
    else:
        return False

def get_size(ipath):
    return os.path.getsize(ipath)

def get_items(ipath):
    #Get all of the items in a path. 
    df = pd.DataFrame([[i, os.path.isdir(os.path.join(ipath, i))] for i in os.listdir(ipath)], columns=['item','isdir'])
    df['path'] = ipath
    df['fullpath'] = df['path'] + "\\" + df['item']
    return df

def get_split_of_item(x):
    try: 
        y = x.split(".")[1]
    except IndexError:
        y = np.nan
    return y

def get_files(df):
    df = df[df['isdir']==False]
    df['extension'] = df['item'].apply(get_split_of_item)
    df['size'] = df['fullpath'].apply(get_size)
    return df


def get_all_files_in_folder(ipath):
    df = get_items(ipath)
    df = get_files(df)
    return df


def get_folders(ipath):
    df = get_items(ipath)
    df = df[df['isdir']]
    if 'fullpath' in df.columns:
        folders = df['fullpath'].tolist()
    else:
        return []
    return folders


def process_all_in_folder(ipath):
    dfs = pd.DataFrame()
    for path in get_folders(ipath):
        print(path)
        if (has_access(path))&(has_items(ipath)):
            df = get_all_files_in_folder(path)
            dfs = pd.concat([dfs,df])
    dfs = dfs.reset_index(drop=True)
    return dfs




def traverse_folders(folders, base_path, df):
    while len(folders)>0:
        for f in folders:
            print(f)
            if has_access(f):
                folders += get_folders(f)
                df2 = process_all_in_folder(f)
                if len(df2)>0:
                    df = pd.concat([process_all_in_folder(f), df])
            folders.remove(f)
        print("totalnumber of folders: ",len(folders))
    return df



folders = get_folders(base_path)
# df = process_all_in_folder(base_path)
df = pd.DataFrame()
df2 = traverse_folders(folders, base_path, df)
 # %%


try:
    df2.to_csv("../data/files.csv")
except:
    df2.to_csv("files.csv")