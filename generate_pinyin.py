import requests

class Generate_Pinyin:
    def __init__(self, hanzi):
        print("generating this hanzi:", hanzi)
        pinyin_payload = {"text": hanzi, 
                "type": "2", 
                "letter_type": "0", 
                "letter_blank": "1",
                }
        pinyin_url = "https://www.iamwawa.cn/home/pinyin/ajax"
        pinyin_res = requests.post(pinyin_url, data=pinyin_payload)
        pinyin_res = pinyin_res.json()
        print(pinyin_res)
        pinyin = pinyin_res["data"]
        self.pinyin = pinyin
