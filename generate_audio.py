import urllib.request
import requests

class Generate_Audio:
    def __init__(self, hanzi):
        tts_payload =   {"language": "中文（普通话，简体）",
                    "voice":	"zh-CN-XiaochenNeural",
                    "text":	hanzi,
                    "role":	"0",
                    "style":	"livecommercial",
                    "rate":	"30",
                    "pitch":	"0",
                    "kbitrate": "audio-16khz-32kbitrate-mono-mp3",
                    "silence": "",
                    "styledegree": "1",
                    "volume": "75",
                    "predict": "0",
                    "user_id": "",
                    "yzm": "202410170001",
                    "replice": "1",
                    "token": "qetJnrr6jkB3TtgtcuPYyQrv:f4901c8708445b848b649e33589b043d"
                    }
        tts_url = "https://www.text-to-speech.cn/getSpeek.php"
        tts_res = requests.post(tts_url, data=tts_payload) 
        tts_res = tts_res.json()
        # print(tts_res)
        print("download link:", tts_res["download"])
        download_url_parts = tts_res["download"].split("/")
        filename = download_url_parts[-1]
        # tts_file, header = urllib.request.urlretrieve(tts_res["download"], f"./mp3_file/{file_name}") 
        self.url = tts_res["download"]
        self.filename = filename
        