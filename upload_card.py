import json
import urllib.request

class Upload_Card:
    def __init__(self, defn, hanzi, pinyin, url, filename, deck_name):
        upload(defn, hanzi, pinyin, url, filename, deck_name)

createModelParams = {
    "modelName":"AnkiSentenceGen",
    # "inOrderFields": ["Simp_Hanzi", "Trad_Hanzi", "Pinyin", "Definition"],
    # Instead, used card_creator to create the html for the front and the back
    "inOrderFields": ["English", "Pinyin", "Hanzi", "Audio"],
    "isCloze": False,
    "cardTemplates": [
        {
            "Front": "{{Audio}}",
            "Back": "{{English}}<br>{{Pinyin}}<br>{{Hanzi}}<br>{{Audio}}"
        }
    ]
}

def get_deckname(deck_name):
    res = ""

    try:
        with open("deck_cache.txt", "x") as file:
            pass
    except Exception as e:
        print("deck_cache error:", e)
        print("Hopefully error is just file already exists")

    # Try to find deckname in the cache
    with open("deck_cache.txt", "r") as read_file:
        for line in read_file:
            if deck_name in line:
                res = line
                break
    # If it wasn't in the cache, then get all decknames, then find the deckname, then add it
    if not res:
        deckNames = invoke("deckNames")
        for name in deckNames:
            if deck_name in name:
                res = name
                with open("deck_cache.txt", "w") as write_file:
                    write_file.write(f"{name}\n")
                break
    return res
        

def upload(defn, hanzi, pinyin, url, filename, deck_name):
    # I actually first want to check if the deck name is within an subdecks or something, so search for the deck_name a subarray of all the decks
    # should cache this too
    real_filename = get_deckname(deck_name)
    print("res of real_filename:", real_filename)
    if not real_filename:
        # create the deck with name deck_name if deck_name doesn't exist with correct model, otherwise add to the deck deck_name
        createDeck = invoke("createDeck", deck=f"{deck_name}")
        real_filename = deck_name
        print("createDeck res:", createDeck)
    try:
        createModel = invoke('createModel', **createModelParams)
        print("createModel res:", createModel)
    except Exception as e:
        print("this error occured when making model:", e)
        print("don't need to do anything if we already have model")
        pass
    # Should be able to then garuantee that the deck_name exists

    storeAudioFileParams = {
        "filename": filename,
        "url": url,
    }

    # Now, we need to download and store it in media folder
    storeAudioFile = invoke("storeMediaFile", **storeAudioFileParams)
    print(storeAudioFile)

    addCard = {
                "deckName":real_filename,
                "modelName":"AnkiSentenceGen",
                "fields": {
                    "English": defn,
                    "Pinyin": pinyin,
                    "Hanzi": hanzi,
                    "Audio": f"[sound:{filename}]"
                },
            }
    canAdd = invoke("canAddNotesWithErrorDetail", notes=[addCard])

    if(canAdd[0]['canAdd']):
        invoke('addNote', note=addCard)
        print("added sentence:", hanzi)

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']