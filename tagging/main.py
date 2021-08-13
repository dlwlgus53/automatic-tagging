import pororo
import argparse
import json
import random
import numpy as np
from dataset import Dataset
from pororo import Pororo
from soylemma import Lemmatizer
from cluster import cluster_root
from tqdm import tqdm
import pdb;
import re
parser = argparse.ArgumentParser()

parser.add_argument('--data_path', type=str, default='../data/wos/dev_data_small.json')
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--domain', type=str, default='식당')

args = parser.parse_args()

random.seed(args.seed)
np.random.seed(args.seed)
# torch.manual_seed(config.seed)
# torch.cuda.manual_seed(config.seed)
# torch.cuda.manual_seed_all(config.seed)
# torch.backends.cudnn.deterministic = True
# torch.backends.cudnn.benchmark = False

lemmatizer = Lemmatizer()
def find_nearest_leamma_vp(index, parsed_text):
    while True:
        if parsed_text[index-1][3] == "VP" or parsed_text[index-1][2] == -1: #tag
            lem = lemmatizer.lemmatize(parsed_text[index-1][1])
            if len(lem)>0:
                return lem[0][0]
            else:
                return parsed_text[index-1][1] # lemmanize fail
        else:
            index = parsed_text[index-1][2]#dom



if __name__ == "__main__":
    CR = cluster_root()

    with open(args.data_path, 'r') as input_file:
        raw_data = json.load(input_file)
        klue = Dataset(raw_data)
    
    # read the data


    dp = Pororo(task="dep_parse", lang="ko") # Dependency Parsing

    ## Make Cluster List
    for dial in klue.parse_dialogues():
        for turn in dial:
            if len(turn['user_actions'])>0 and args.domain in turn['user_actions'][0]:
                parsed_text = dp(turn['user'].replace(".","").replace(",", ""))#TODO
                for index, word, dom, tag in parsed_text:
                    if tag == "VP":
                        continue
                    nearest_leamma_vp = find_nearest_leamma_vp(index, parsed_text)
                    tag_name =nearest_leamma_vp + "_" + tag
                    CR.clusters[tag_name].append_item(word)
    

    ## MERGE!
    slot_nums = 
    import pdb; pdb.set_trace()

    

# lemmanize 성능이 영..


