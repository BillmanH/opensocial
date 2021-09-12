#%%
import pandas as pd
import numpy as np
import yaml
from azure.storage.blob import BlobClient

acceptable_image_types = ["png", "jpg"]

params = yaml.safe_load(open("../blob_keys.yaml"))


def get_blob(name):
    blob = BlobClient.from_connection_string(
        conn_str=params["conn_str"],
        container_name=params["container_name"],
        blob_name=name,
    )
    return blob

def clean_tags(pic):
    acceptable_keys = [k for k in list(pic.keys()) if k not in ["Unnamed: 0","fullpath","isdir","size"]]
    clean_pic = {k: str(pic[k].replace('\\','+')) for k in acceptable_keys}
    return clean_pic


df = pd.read_csv("../data/social_files.csv")
df = df[df["extension"].isin(acceptable_image_types)].dropna()
pictures = df.to_dict(orient="records")
print(f'uploading {len(pictures)} documents to {params["container_name"]}')

unable_to_upload = []
for i, pic in enumerate(pictures):
    if i % 100 == 0:
        print(np.round((i / len(pictures) * 100), decimals=4), "% completed")
    get_blob(pic.get("item")).upload_blob(
        open(pic.get("fullpath"), "rb"),
        tags=clean_tags(pic),
        overwrite=params["overwrite_blob"],
    )


pd.DataFrame(unable_to_upload).to_csv("../data/unable_to_upload.csv")
