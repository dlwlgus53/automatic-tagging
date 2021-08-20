
# import fasttext
# import fasttext.util
import re
import json

# fasttext.util.download_model('ko', if_exists='ignore')  # Korean
# ft = fasttext.load_model('cc.ko.300.bin')

# def embedding(word):
#     return ft.get_word_vector(word)


punctuation = ["'", '"', ',', '?', '!', ':', ';', '(', ')'] # '(', ')' not `()`
def preprocess(sentence):
    sentence = re.sub('|'.join(map(re.escape, punctuation)), '', sentence) # remove punctuation
    sentence =  re.sub(r'([가-힣])(\.)', r'\1', sentence) # remove . only after hangul
    sentence = re.sub('\d{4}', '', sentence)
    sentence = re.sub(r'([0-9]+명)' , r'\1 ', sentence)
    sentence = sentence.strip()
    return sentence

# def delexicalize(sentence):
#     with open("../data/wos/ontology.json") as ontology_file:
#         ontology = json.load(ontology_file)
    
#     for item in ontology['식당-이름']:
#         sentence.replace(item, '[식당이름]')
        
    
#     return sentence

