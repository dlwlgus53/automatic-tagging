import pdb;
import json
from tqdm import tqdm
class Dataset:
    def __init__(self, data):
        self.data = data

    def parse_dialogues(self):
        for key in tqdm(self.data):
            dial = self.data[key]
           
            yield dial
    
    def to_json(self,filename):
        with open(filename, 'w') as fp:
            json.dump(self.data,fp,  indent=4,ensure_ascii=False)


