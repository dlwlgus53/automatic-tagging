
#-*- coding:utf-8 -*-
import urllib3
import json
 
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"
 
accessKey = "e1e7c71e-e556-4ad2-b211-2895efd5b082"
analysisCode = "ner"


def etri_ner(text):
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode
        }
    }
    
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )

    print(str(response.data, "utf-8"))

    NER_response = eval(str(response.data, "utf-8"))["return_object"]["sentence"][0]["NE"]
    # dparse_response = eval(str(response.data, "utf-8"))["return_object"]["sentence"][0]["dparse"]
    return [[n['text'],n['type']] for n in NER_response]

if __name__ == "__main__":
    print(etri_ner("안녕하세요"))