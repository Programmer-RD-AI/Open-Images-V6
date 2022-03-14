import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

try:
    from urllib.request import urlretrieve  # Python 3
except ImportError:
    from urllib import urlretrieve  # Python 2

classes = pd.read_csv("./classes.csv")
labelnames = classes["LabelName"].tolist()
classnames = classes["DisplayName"].tolist()
__imageids = []
__imageids_and_bbox = {}
imageids = []
xmins = []
ymins = []
xmaxs = []
ymaxs = []
file_names = []
imageurls = []
imageurls_original = []
type_of_data = []
image_id = 0

imageid_and_labelname = pd.read_csv(
    "./open_images_data/oidv6-train-annotations-human-imagelabels.csv")
imageid_and_labelname.append(
    pd.read_csv(
        "./open_images_data/test-annotations-human-imagelabels-boxable.csv"))
imageid_and_labelname.append(
    pd.read_csv("./open_images_data/test-annotations-machine-imagelabels.csv"))
imageid_and_labelname.append(
    pd.read_csv(
        "./open_images_data/train-annotations-human-imagelabels-boxable.csv"))
imageid_and_labelname.append(
    pd.read_csv(
        "./open_images_data/train-annotations-machine-imagelabels.csv"))
imageid_and_labelname.append(
    pd.read_csv(
        "./open_images_data/validation-annotations-human-imagelabels-boxable.csv"
    ))
imageid_and_labelname.append(
    pd.read_csv(
        "./open_images_data/validation-annotations-machine-imagelabels.csv"))
tqdm_iter = tqdm(imageid_and_labelname["ImageID"])
for imageid, labelname in zip(tqdm_iter, imageid_and_labelname["LabelName"]):
    if labelname in labelnames:
        tqdm_iter.set_description(f"{imageid}-{labelname}")
        __imageids.append(imageid)

del imageid_and_labelname

xmin_ymin_xmax_ymax = pd.read_csv(
    "./open_images_data/oidv6-train-annotations-bbox.csv")
xmin_ymin_xmax_ymax.append(
    pd.read_csv("./open_images_data/test-annotations-bbox.csv"))
xmin_ymin_xmax_ymax.append(
    pd.read_csv("./open_images_data/validation-annotations-bbox.csv"))
for i in tqdm(range(len(xmin_ymin_xmax_ymax))):
    info = xmin_ymin_xmax_ymax.iloc[i]
    if info["ImageID"] in __imageids:
        __imageids_and_bbox[info["ImageID"]] = [
            info["XMin"],
            info["YMin"],
            info["XMax"],
            info["YMax"],
        ]
del xmin_ymin_xmax_ymax

urls = pd.read_csv(
    "./open_images_data/oidv6-train-images-with-labels-with-rotation.csv")
urls.append(pd.read_csv("./open_images_data/test-images-with-rotation.csv"))
urls.append(
    pd.read_csv("./open_images_data/train-images-boxable-with-rotation.csv"))
urls.append(
    pd.read_csv("./open_images_data/validation-images-with-rotation.csv"))
for i in tqdm(range(len(urls))):
    url = urls.iloc[i]
    if url["ImageID"] in __imageids:
        urlretrieve(url["OriginalURL"], f"./data/{image_id}.png")
        xmin, ymin, xmax, ymax = __imageids_and_bbox[url["ImageID"]]
        file_names.append(f"./data/{image_id}.png")
        type_of_data.append(url["Subset"])
        imageurls.append(url["OriginalURL"])
        imageurls_original.append(url["OriginalLandingURL"])
        imageids.append(url["ImageID"])
        xmins.append(xmin)
        ymins.append(ymin)
        xmaxs.append(xmax)
        ymaxs.append(ymax)
        image_id += 1

data = pd.DataFrame({
    "ImageIds": imageids,
    "XMin": xmins,
    "YMin": ymins,
    "XMax": xmaxs,
    "YMax": ymaxs,
    "File Name": file_names,
    "ImageUrls": imageurls,
    "Og_ImageUrls": imageurls_original,
    "Type of Data": type_of_data,
})
data.to_csv("./data.csv")
