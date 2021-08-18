from re import sub
from utils import embedding
from collections import defaultdict
import math
from scipy import spatial

class cluster_root:
    def __init__(self):
        self.clusters = defaultdict(cluster)

    def combine(self, dom_name, sub_name):
        dom = self.clusters[dom_name]
        sub = self.clusters[sub_name]

        dom.vector =  (dom.vector * len(dom.entity) + sub.vector * len(sub.entity))\
             / (len(dom.entity) + len(sub.entity))

        dom.entity.extend(sub.entity)
        dom.sub_cluster.append(sub.sub_cluster)

        del self.clusters[sub_name]

    def similar(self, c1, c2):
        # code from here https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
        def calculate_cosine_distance(a, b):
            cosine_distance = float(spatial.distance.cosine(a, b))
            return cosine_distance
        cosine_similarity = 1 - calculate_cosine_distance(c1, c2)
        return cosine_similarity
    
class cluster:
    def __init__(self):
        self.sub_cluster = []
        self.entity = []
        self.vector = 0

    def append_item(self, item):
        self.entity.append(item)
        item_vector = embedding(item) 
        self.vector = ((len(self.entity)-1) * self.vector + item_vector)/len(self.entity)



