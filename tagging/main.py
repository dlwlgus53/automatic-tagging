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
import itertools
import json
import datetime
from utils import delexicalize, preprocess
from ner import etri_ner
from phishing_analysis import request_V

parser = argparse.ArgumentParser()
# parser.add_argument('--data_path', type=str, default='../data/wos/dev_data.json')
parser.add_argument('--data_path', type=str, default='../data/voice.json')
parser.add_argument('--slot_num', type=int, default=10)

parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--domain', type=str, default='식당')

args = parser.parse_args()

random.seed(args.seed)
np.random.seed(args.seed)

pos = Pororo(task="pos", lang="ko")
ner = Pororo(task="ner", lang="ko")
now = datetime.datetime.now()
now = now.strftime('%Y-%m-%d_%H:%M:%S')

def find_nearest_leamma_vp(index, parsed_text):
    while True:
        if parsed_text[index-1][3] == "VP" or parsed_text[index-1][2] == -1: #tag
            lem = pos(parsed_text[index-1][1])
            if len(lem)>0:
                for L in lem:
                    if L[1] == 'V': # verb
                        return lem[0]
                return parsed_text[index-1][1] # lemmanize fail
            else:
                return parsed_text[index-1][1] # lemmanize fail
        else:
            index = parsed_text[index-1][2]#dom
        


def write_to_user_actions(tagname, raw_word):

    def remove_josa(raw_word):
        JOSA = ['JKS','JKC','JKG','JKO','JKB','JKV','JKQ','JX','JC']
        possed = pos(raw_word)
        word = ""
        for p in possed:
            if p[1] not in JOSA:
                word+=p[0]
        return word

    word = remove_josa(raw_word)
    for V in request_V:
        if V+"_NP" in tagname:
            return f'request= {word}'

    if tagname in 'PERSON':
        return f'inform= 사기꾼_이름 = {word}'

    if tagname == "ORGANIZATION":
        return f'inform= 사기꾼_기관 = {word}'


    




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
            # if len(turn['user_actions'])>0 and args.domain in turn['user_actions'][0]:


            dp_parsed_text = dp(delexicalize(preprocess(turn['user'])))#TODO
            for index, word, dom, tag in dp_parsed_text:
                if tag in ["VP","AP","DP"]:
                    continue
                nearest_leamma_vp = find_nearest_leamma_vp(index, dp_parsed_text)
                tag_name =nearest_leamma_vp + "_" + tag
                CR.clusters[tag_name].append_item(word)
                action = write_to_user_actions(tag_name, word)
                if action:
                    turn["user_actions"].append(action)


            ner_parsed_word = ner(delexicalize(preprocess(turn['user'])))
            for word, tag_name in ner_parsed_word:
                if tag_name != 'O':
                    CR.clusters[tag_name].append_item(word)
                    action = write_to_user_actions(tag_name, word)
                    if action:
                        turn["user_actions"].append(action)

            #SRL

    
    klue.to_json(f'../log/{now}user_action.json')

    ## MERGE!
    # slot_nums = args.slot_num # optional\    
    # log_dict = {}
    # for name in CR.clusters.keys():
    #     log_dict[name] = CR.clusters[name].entity

    # with open(f'../log/{now}before.json', 'w') as fp:
    #     json.dump(log_dict, fp, indent=4,ensure_ascii=False)

    # print(f'Cluster numbers : {len(CR.clusters.keys())}')
    # while len(CR.clusters.keys()) > slot_nums:
    #     max_similar_score = 0
    #     most_similar =()
    #     for key_pair in  list(itertools.permutations(CR.clusters.keys(), 2)):
    #         c1 = CR.clusters[key_pair[0]]
    #         c2 = CR.clusters[key_pair[1]]

    #         similar_score = CR.similar(c1.vector,c2.vector)
    #         if max_similar_score<similar_score:
    #             most_similar = key_pair
    #             max_similar_score = similar_score
            
    #     CR.combine( most_similar[0],  most_similar[1])
    #     print(f'Left slot number : {len(CR.clusters.keys())}')
    #     log_dict = {}
        
    # for name in CR.clusters.keys():
    #     log_dict[name] = CR.clusters[name].entity

    # with open(f'../log/{now}after.json', 'w') as fp:
    #     json.dump(log_dict, fp, indent=4,ensure_ascii=False)

    

