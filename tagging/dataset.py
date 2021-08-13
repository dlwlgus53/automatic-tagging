import pdb;
from tqdm import tqdm
class Dataset:
    def __init__(self, data):
        self.data = data

    def parse_dialogues(self):
        for key in tqdm(self.data):
            dial = self.data[key]
            dial_info = {"user":[],
                        "system" : [],
                        "user_actions" : [],
                        "belief" : []
                        }
            for turn in dial:
                dial_info["user"].append(turn["user"])
                dial_info["system"].append(turn["system"])
                dial_info["user_actions"].append(turn["user_actions"]) #"inform= 식당_주류 판매 =yes"
                dial_info["belief"].append(turn["belief"])

            yield dial
    


