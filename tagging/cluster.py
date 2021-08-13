from re import sub
from utils import embedding
from collections import defaultdict

class cluster_root:
    def __init__(self):
        self.clusters = defaultdict(cluster)

    def combine(self, dom_cluster, sub_cluster):
        dom_cluster.vector =  (dom_cluster.vector * len(dom_cluster) + sub_cluster.vector * len(sub_cluster))\
             / (len(dom_cluster) + len(sub_cluster))
        dom_cluster.entity.extend(sub_cluster)
        del sub_cluster

    
class cluster:
    def __init__(self):
        self.entity = []
        self.vector = 0

    def append_item(self, item):
        self.entity.append(item)
        item_vector = embedding(item) 
        self.vector = ((len(self.entity)-1) * self.vector + item_vector)/len(self.entity)



