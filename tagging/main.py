import argparse
import json
import random
import numpy as np
from dataset import Dataset
from pororo import Pororo
from tqdm import tqdm
import pdb;
import json
import datetime
from utils import  preprocess
from ner import etri_ner
from rule import make_belief

parser = argparse.ArgumentParser()
# parser.add_argument('--data_path', type=str, default='../data/wos/dev_data.json')
parser.add_argument('--data_path', type=str, default='../data/voice.json')
parser.add_argument('--slot_num', type=int, default=10)

parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--domain', type=str, default='식당')

args = parser.parse_args()

random.seed(args.seed)
np.random.seed(args.seed)


print("Load the weak-supervising tool")
ner = Pororo(task="ner", lang="ko") # named entity recognistion
dp = Pororo(task="dep_parse", lang="ko") # Dependency Parsing
srl = Pororo(task="srl", lang="ko") # sementic role labeling
pos = Pororo(task="pos", lang="ko") # pos tagging


now = datetime.datetime.now()
now = now.strftime('%Y-%m-%d_%H:%M:%S')

def find_nearest_leamma_vp(index, parsed_text):
    while True:
        if parsed_text[index-1][3] in ["VP","VNP"] or parsed_text[index-1][2] == -1: #tag
            lem = pos(parsed_text[index-1][1])
            poses = [l[1] for l in lem] # only pos
            if len(lem)>0:
                for L in lem:
                    if L[1][0] == 'V' : # find verb first
                        return L[0]
                for L in lem:
                    if L[1] == "NNG": # find NNG
                        return L[0]
                return parsed_text[index-1][1] # lemmanize fail
            else:
                return parsed_text[index-1][1] # lemmanize fail
        else:
            index = parsed_text[index-1][2]#dom
        



    

# or L[1] == 'NNG'


if __name__ == "__main__":
    # read the data
    with open(args.data_path, 'r') as input_file:
        raw_data = json.load(input_file)
        data = Dataset(raw_data)
    
    ## Make Cluster List
    for dial in data.parse_dialogues():
        for turn in dial:

            state = {
                "raw_word" : list(preprocess(turn['user'])),
                "DP" : [],
                "NER" : [],
                "SRL" : []
            }

            # Dependency Labeling
            dp_parsed_text = dp(preprocess(turn['user']))
            for index, word, dom, tag in dp_parsed_text:
                nearest_leamma_vp = find_nearest_leamma_vp(index, dp_parsed_text)
                tag_name =nearest_leamma_vp + "_" + tag
                for i in range(len(word)):
                    if i==0:
                        state["DP"].append(tag_name+'_S')
                    elif i==len(word)-1:
                        state["DP"].append(tag_name+'_E')
                    else:
                        state["DP"].append(tag_name+ '_I')
                state["DP"].append("SPACE")
                
            del state["DP"][-1] # last space


                

            # Ner 
            ner_parsed_word = ner(preprocess(turn['user']))
            for word, tag_name in ner_parsed_word:
                for i in range(len(word)):
                    if i==0:
                        state["NER"].append(tag_name+'_S')
                    elif i==len(word)-1:
                        state["NER"].append(tag_name+'_E')
                    else:
                        state["NER"].append(tag_name+ '_I')


            #SRL
            srl_parsed_word = srl(preprocess(turn['user']))
            for word, tag_name in srl_parsed_word[0]:
                for i in range(len(word)):
                    if i==0:
                        state["SRL"].append(tag_name+'_S')
                    elif i==len(word)-1:
                        state["SRL"].append(tag_name+'_E')
                    else:
                        state["SRL"].append(tag_name+ '_I')
                state["SRL"].append("SPACE")
            
            del state["SRL"][-1] # Last space

            make_belief(turn,state)

    data.to_json(f'../log/{now}user_action.json')
