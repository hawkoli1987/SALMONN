"""
This script processes the VoxCeleb dataset to generate JSON files for speaker similarity evaluation,
converting raw similarity scores into structured annotations.

Input Directory Structure:
    /path/to/voxceleb_dataset/
    ├── dev/wav/
    │   └── [wav files]
    ├── test/wav/
    │   └── [wav files]
    ├── voxsim_train_list_average.txt
    └── voxsim_test_list.txt

    The voxsim_*_list*.txt files contain entries in format:
    "wav1_path,wav2_path,similarity_score"
    where wav1_path and wav2_path are relative paths to audio files in dev/wav or test/wav

Output Directory Structure:
    /path/to/result_dir/
    ├── voxsim_train_onlyscore.json
    └── voxsim_test_onlyscore.json

    JSON files contain entries:
    {
        "path": "/path/to/first/audio",
        "expand_wav": ["/path/to/second/audio"],
        "task": "spk_evaluation_onlyscore",
        "text": "The score is X" (where X is the similarity score)
    }
"""

import os
import random
import json

subsets = ["train","test"]
score_template = ["The score is {}.","The score of speaker similarity is {}.", "{}."]
dataset_dir = "/path/to/voxceleb_dataset"
result_dir = "/path/to/result_dir" # path to save the results

for subset in subsets:
    if subset == "train":
        data_txt = open(os.path.join(dataset_dir,"voxsim_{}_list_average.txt".format(subset)),"r")
    else:
        data_txt = open(os.path.join(dataset_dir,"voxsim_{}_list.txt".format(subset)),"r")
    data_json = {"annotation":[]}

    while True:
        item = {}
        line = data_txt.readline()[:-1]
        if not line:
            break
        onepiece_data = line.split(',')
        if os.path.exists(os.path.join(dataset_dir,"dev/wav",onepiece_data[0])):
            item.update({"path":os.path.join(dataset_dir,"dev/wav",onepiece_data[0])})
        else:
            item.update({"path":os.path.join(dataset_dir,"test/wav",onepiece_data[0])})
        if os.path.exists(os.path.join(dataset_dir,"dev/wav",onepiece_data[1])):
            item.update({"expand_wav":[os.path.join(dataset_dir,"dev/wav",onepiece_data[1])]})
        else:
            item.update({"expand_wav":[os.path.join(dataset_dir,"test/wav",onepiece_data[1])]})
        item.update({"task":"spk_evaluation_onlyscore"})
        text = random.choice(score_template).format(float(onepiece_data[-1]))
        item.update({"text":text})
        data_json["annotation"].append(item)

    with open(os.path.join(result_dir,"voxsim_{}_onlyscore.json".format(subset)), "w") as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)