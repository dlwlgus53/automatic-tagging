from pororo import Pororo
import re

JOSA_tag = ['JKS','JKC','JKG','JKO','JKB','JKV','JKQ','JX','JC']
request_V = ['하','맞','드리','말씀','필요','여쭈','되','송금','알리','부탁']
inform_V = ['이']
send_V = ['송금']


pos = Pororo(task="pos", lang="ko") # pos tagging

def _remove_josa(raw_word):
    possed = pos(raw_word)
    word = ""
    for p in possed:
        if p[1] not in JOSA_tag:
            word+=p[0]
    return word



def name(state, i):
    word = ""
    if state['NER'][i] == 'PERSON_S' and\
        state['DP'][i].split("_")[0] in inform_V:
        while True:
            word += state['raw_word'][i]
            i+=1
            if state['NER'][i].split("_")[0] != 'PERSON':
                break
    
    return word

def organization(state, i):
    word = ""
    if state['NER'][i] == 'ORGANIZATION_S' and\
        state['DP'][i].split("_")[0] in inform_V:
        while True:
            word += state['raw_word'][i]
            i+=1
            if state['NER'][i].split("_")[0] != 'ORGANIZATION':
                break
    return word

def bank(state,i):
    word = ""
    if state['NER'][i] == 'ORGANIZATION_S' and\
        state['DP'][i].split("_")[0] in send_V:
        while True:
            word += state['raw_word'][i]
            i+=1
            if state['NER'][i].split("_")[0] != 'ORGANIZATION':
                break
    return word

def IP(state,i):
    word = ""
    if state['NER'][i] == 'QUANTITY_S':
        while True:
            word += state['raw_word'][i]
            i+=1
            if state['NER'][i].split("_")[0] != 'QUANTITY':
                break
    # this code is from https://stackoverflow.com/questions/10086572/ip-address-validation-in-python-using-regex
    ip = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    match = ip.match(word)

    if match:
        return word
    else:
        return ""



def make_belief(turn, state):
    # import pdb;
    # pdb.set_trace()
    assert len(state['raw_word']) == len(state['DP']) == len(state['SRL']) == len(state['NER'])
    for i, w in enumerate(state['raw_word']):
        word = ""

        word = organization(state, i)
        if word !="":
            turn["user_actions"].append(f'inform= 사기꾼_기관 = {word}')
        
        word = ""
        word = name(state, i)
        if word !="":
            turn["user_actions"].append(f'inform= 사기꾼_이름 = {word}')

        word = ""
        word = bank(state, i)
        if word !="":
            turn["user_actions"].append(f'inform= 사기꾼_은행 = {word}')
        
        word = ""
        word = IP(state, i)
        if word !="":
            turn["user_actions"].append(f'inform= 사기꾼_아이피 = {word}')


    # for W, D, S in zip(state['raw_word'], state['DP'], state['SRL']):
    #     W = _remove_josa(W)

    #     action = ""
    #     if D in ["VP","AP","DP"]:
    #         continue
    
    # for W, N in state['NER']:
    #     if N == 'PERSON':
    #         action =  f'inform= 사기꾼_이름 = {W}'

    #     elif N == "ORGANIZATION":
                
    #         action =  f'inform= 사기꾼_기관 = {W}'
        

    #     turn["user_actions"].append(action)
