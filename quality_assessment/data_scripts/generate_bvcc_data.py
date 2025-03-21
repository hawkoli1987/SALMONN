import os
import random
import json

"""
This script processes the BVCC (Blizzard Voice Conversion Challenge) dataset to generate JSON files
containing speech quality assessment annotations.

Input Directory Structure:
    /path/to/bvcc_dataset/
    └── main/
        └── DATA/
            ├── sets/
            │   ├── train_mos_list.txt
            │   ├── val_mos_list.txt
            │   └── test_mos_list.txt
            └── wav/
                └── [wav files]

    The *_mos_list.txt files contain entries in format: "wavfile_name,score"

Output Directory Structure:
    /path/to/result_dir/
    ├── bvcc_train_onlyscore.json
    ├── bvcc_val_onlyscore.json
    └── bvcc_test_onlyscore.json

    Each JSON file contains an "annotation" list with entries:
    {
        "path": "/path/to/wav/file",
        "task": "mos_evaluation_onlyscore_bvcc",
        "text": "The score is X" (where X is the MOS score)
    }
"""

subsets = ["train","val","test"]
score_template = ["The score is {}.","The score of the quality of the speech sample is {}.", "{}."]
dataset_dir = "/path/to/bvcc_dataset"
result_dir = "/path/to/result_dir" # path to save the results

for subset in subsets:
    data = open(os.path.join(dataset_dir,"main/DATA/sets/{}_mos_list.txt".format(subset)),"r")
    data_json = {"annotation":[]}

    while True:
        line = data.readline()[:-1]
        if not line:
            break
        item = {}
        split = line.find(',')
        wav = line[:split]
        score = line[split+1:]
        item.update({"path":os.path.join(dataset_dir,"main/DATA/wav",wav)})
        item.update({"task":"mos_evaluation_onlyscore_bvcc"})
        text = random.choice(score_template).format(score)
        item.update({"text":text})
        data_json["annotation"].append(item)

    with open(os.path.join(result_dir,"bvcc_{}_onlyscore.json".format(subset)), "w") as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)