import json
import requests

class Yahoo_keyphrase():
    pageurl = 'https://jlp.yahooapis.jp/KeyphraseService/V1/extract'
    def __init__(self):
        pass
    def get_keyphrase(self, sentence, id):
        payload = {'appid': id, 'sentence': sentence, 'output': 'json'}
        r = requests.get(Yahoo_keyphrase.pageurl, params=payload)
        
        