#%%
import pandas as pd
import yaml
from azure.storage.blob import BlobClient

params=yaml.safe_load(open("../blob_keys.yaml"))
blob = BlobClient.from_connection_string(conn_str=params["conn_str"],
                                        container_name=params["container_name"],
                                        blob_name=params["blob_name"])

with open("../data/test.txt", "rb") as data:
    blob.upload_blob(data)


blob.get